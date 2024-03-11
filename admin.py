# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
Created on: 2024/3/7 17:06
@file: admin.py
@author: DH
"""
from flask import Blueprint, redirect, render_template, session, url_for

from sql.sql import search_admin

admin_page = Blueprint("admin", __name__, static_folder="static", template_folder="templates")


@admin_page.route("/")
def root():
    return redirect("/home")


@admin_page.route('/profile')
def profile():
    if 'logged_in' in session:
        results = search_admin(session['id'])
        print('result:', results)
        return render_template('admin_profile.html', results=results)
    return redirect(url_for('login'))


@admin_page.route('/manage')
def manage():
    if 'logged_in' in session:
        return render_template('admin_manage.html')
    return redirect(url_for('login'))
