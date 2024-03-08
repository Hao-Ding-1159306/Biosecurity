# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
Created on: 2024/3/7 17:06
@file: admin.py
@author: DH
"""
from flask import (Blueprint, Flask, redirect, render_template, request,
                   session, url_for)

from sql.sql import search_admin

admin_page = Blueprint("admin", __name__, static_folder="static", template_folder="templates")


@admin_page.route("/")
def root():
    return redirect("/home")


@admin_page.route('/home')
def home():
    if 'logged_in' in session:
        return render_template('admin_home.html', username=session['username'], role=session['role'])
    return redirect(url_for('login'))


@admin_page.route('/profile')
def profile():
    if 'logged_in' in session:
        results = search_admin(session['id'])
        print('result:', results)
        return render_template('admin_profile.html', results=results)
    return redirect(url_for('login'))

@admin_page.route('/edit_profile')
def edit_profile():
    if 'logged_in' in session:
        results = search_admin(session['id'])
        print('result:', results)
        return render_template('admin_edit_profile.html', results=results)
    return redirect(url_for('login'))
