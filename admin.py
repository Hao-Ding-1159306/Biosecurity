# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
Created on: 2024/3/7 17:06
@file: admin.py
@author: DH
"""
import mysql.connector
from flask import (Blueprint, Flask, redirect, render_template, request,
                   session, url_for)

admin_page = Blueprint("admin", __name__, static_folder="static", template_folder="templates")


@admin_page.route("/")
def root():
    return redirect("/home")


@admin_page.route('/home')
def home():
    if 'logged_in' in session:
        return render_template('home.html', username=session['username'], role=session['role'])
    return redirect(url_for('login'))
