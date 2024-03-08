# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
Created on: 2024/3/6 14:34
@file: app.py
@author: DH
"""
import binascii
import os
import re
from datetime import datetime

from flask import Flask, redirect, render_template, request, session, url_for
from flask_hashing import Hashing

from admin import admin_page
from agronomists import agronomists_page
from sql.sql import get_cursor
from staff import staff_page

app = Flask(__name__)

hashing = Hashing(app)
app.secret_key = binascii.hexlify(os.urandom(24)).decode('utf-8')

app.register_blueprint(admin_page, url_prefix="/admin")
app.register_blueprint(staff_page, url_prefix="/staff")
app.register_blueprint(agronomists_page, url_prefix="/agronomists")

db_cursor = None
connection = None


@app.route("/")
def root():
    return redirect("/home")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'role' in request.form:
        # Create variables for easy access
        username = request.form['username']
        user_password = request.form['password']
        role = request.form['role']
        # Check if account exists using MySQL
        cursor = get_cursor()
        cursor.execute(f"SELECT * FROM {role} WHERE username = '{username}'")
        # Fetch one record and return result
        account = cursor.fetchone()
        if account is not None:
            password = account[2]
            if hashing.check_value(password, user_password, salt='abcd'):
                session['logged_in'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                session['role'] = role
                return redirect(url_for(f"{role}.home"))
            else:
                # password incorrect
                msg = 'Incorrect password!'
        else:
            # Account doesn't exist or username incorrect
            msg = f'Incorrect username in {role}'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'phone' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = get_cursor()
        cursor.execute('SELECT * FROM agronomists WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            hashed = hashing.hash_value(password, salt='abcd')
            today = datetime.today().date()
            cursor.execute(
                'INSERT INTO agronomists (username, password, first_name, last_name, address, email, phone, date_joined) VALUES (%s, %s, first_name, last_name, address, %s, %s, %s)',
                (username, hashed, email, phone, today,))
            cursor.close()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/home')
def home():
    if 'logged_in' in session:
        return redirect(url_for(f"{session['role']}.home"))
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        print(f'password:{old_password},{new_password}, {confirm_password}\n')
        return redirect(url_for(f"{session['role']}.profile"))
    return render_template('change_password.html')


if __name__ == '__main__':
    app.run(debug=True)
