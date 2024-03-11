# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
Created on: 2024/3/7 17:09
@file: staff.py
@author: DH
"""
from flask import Blueprint, redirect, render_template, session, url_for

from sql.sql import search_staff

staff_page = Blueprint("staff", __name__, static_folder="static", template_folder="templates")


@staff_page.route("/")
def root():
    return redirect("/home")


@staff_page.route('/profile')
def profile():
    if 'logged_in' in session:
        results = search_staff(session['id'])
        print('result:', results)
        return render_template('staff_profile.html', results=results)
    return redirect(url_for('login'))
