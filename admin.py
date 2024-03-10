# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
Created on: 2024/3/7 17:06
@file: admin.py
@author: DH
"""
from flask import (Blueprint, Flask, redirect, render_template, request,
                   session, url_for)

from sql.sql import search_admin, get_cursor

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

@admin_page.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        results = search_admin(session['id'])
        print('result:', results)
        form_data = request.form
        cursor = get_cursor()

        # 构建更新语句
        sql = "UPDATE admin SET "
        update_values = []
        for key, value in form_data.items():
            if key != 'admin_id':
                sql += f"{key} = %s, "
                update_values.append(value)
        sql = sql.rstrip(', ')
        # 添加 WHERE 条件
        sql += " WHERE admin_id = %s"
        update_values.append(session['id'])

        # 执行更新语句
        cursor.execute(sql, update_values)
        cursor.close()
        results = search_admin(session['id'])
        print('new result:', results)
        return render_template('admin_edit_profile.html', results=results)
    results = search_admin(session['id'])
    print('result:', results)
    return render_template('admin_edit_profile.html', results=results)
