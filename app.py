# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
Created on: 2024/3/6 14:34
@file: app.py
@author: DH
"""
import os
import binascii
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect
from flask_hashing import Hashing

app = Flask(__name__)
hashing = Hashing(app)  # create an instance of hashing

app.secret_key = binascii.hexlify(os.urandom(24)).decode('utf-8')

db_cursor = None
connection = None


def get_cursor():
    global db_cursor
    global connection
    connection = mysql.connector.connect(user=connect.dbuser,
                                         password=connect.dbpass, host=connect.dbhost,
                                         auth_plugin='mysql_native_password',
                                         database=connect.dbname, autocommit=True)
    db_cursor = connection.cursor()
    return db_cursor


@app.route("/")
def root():
    return redirect("/home")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'role' in request.form:
        print(request.form)
        # Create variables for easy access
        username = request.form['username']
        user_password = request.form['password']
        role = request.form['role']
        # Check if account exists using MySQL
        cursor = get_cursor()
        print(f'SELECT * FROM {role} WHERE username = {username}')
        cursor.execute(f"SELECT * FROM {role} WHERE username = '{username}'")
        # Fetch one record and return result
        account = cursor.fetchone()
        if account is not None:
            password = account[2]
            if hashing.check_value(password, user_password, salt='abcd'):
                # If account exists in accounts table
                # Create session data, we can access this data in other routes
                print(session, type(session))
                session['logged_in'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                session['role'] = role
                return redirect(url_for('home'))
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
        return render_template('home.html', username=session['username'], role=session['role'])
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    print(session)
    if 'logged_in' in session:
        cursor = get_cursor()
        cursor.execute(f"SELECT * FROM {session['role']} WHERE username = '{session['username']}'")
        account = cursor.fetchone()
        if session['role'] == 'agronomists':
            results = {'id': account[0], 'username': account[1], 'first_name': account[3], 'last_name': account[4],
                       'address': account[5], 'email': account[6], 'phone': account[7], 'date_joined': account[8],
                       'state': account[9]}
        elif session['role'] == 'staff' or session['role'] == 'admin':
            results = {'id': account[0], 'username': account[1], 'first_name': account[3], 'last_name': account[4],
                       'position': account[5], 'email': account[6], 'phone': account[7], 'date_hired': account[8],
                       'department': account[9], 'state': account[10]}
        print(results)
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
