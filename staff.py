# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
Created on: 2024/3/7 17:09
@file: staff.py
@author: DH
"""
import mysql.connector
from flask import (Blueprint, Flask, redirect, render_template, request,
                   session, url_for)

staff_page = Blueprint("staff", __name__, static_folder="static", template_folder="templates")
@staff_page.route("/")
def root():
    return redirect("/home")


@staff_page.route('/home')
def home():
    if 'logged_in' in session:
        return render_template('home.html', username=session['username'], role=session['role'])
    return redirect(url_for('login'))