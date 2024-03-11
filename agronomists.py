# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
Created on: 2024/3/7 17:10
@file: agronomists.py
@author: DH
"""
from flask import Blueprint, redirect, render_template, session, url_for

from sql.sql import search_agronomists

agronomists_page = Blueprint("agronomists", __name__, static_folder="static", template_folder="templates")

@agronomists_page.route("/")
def root():
    return redirect("/home")


@agronomists_page.route('/profile')
def profile():
    if 'logged_in' in session:
        results = search_agronomists(session['id'])
        print('result:', results)
        return render_template('agronomists_profile.html', results=results)
    return redirect(url_for('login'))