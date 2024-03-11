# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
Created on: 2024/3/8 14:43
@file: sql.py
@author: DH
"""
import mysql.connector

import connect


def get_cursor():
    global db_cursor
    global connection
    connection = mysql.connector.connect(user=connect.dbuser,
                                         password=connect.dbpass, host=connect.dbhost,
                                         auth_plugin='mysql_native_password',
                                         database=connect.dbname, autocommit=True)
    db_cursor = connection.cursor()
    return db_cursor


def search_admin(id: int):
    cursor = get_cursor()
    cursor.execute(f"SELECT * FROM admin WHERE id = {id}")
    columns = [col[0] for col in cursor.description]
    result = cursor.fetchone()
    cursor.close()
    if result:
        result_dict = dict(zip(columns, result))
        return result_dict
    return {}


def search_staff(id: int):
    cursor = get_cursor()
    cursor.execute(f"SELECT * FROM staff WHERE id = {id}")
    columns = [col[0] for col in cursor.description]
    result = cursor.fetchone()
    cursor.close()
    if result:
        result_dict = dict(zip(columns, result))
        print(result_dict)
    return result


def search_agronomists(id: int):
    cursor = get_cursor()
    cursor.execute(f"SELECT * FROM agronomists WHERE id = {id}")
    columns = [col[0] for col in cursor.description]
    result = cursor.fetchone()
    cursor.close()
    if result:
        result_dict = dict(zip(columns, result))
        print(result_dict)
    return result


def get_info(id: int, role: str):
    if role == 'admin':
        return search_admin(id)
    elif role == 'staff':
        return search_staff(id)
    elif role == 'agronomist':
        return search_agronomists(id)
    raise ValueError

def get_agronomists_list():
    cursor = get_cursor()
    cursor.execute(f"SELECT * FROM agronomists")
    columns = [col[0] for col in cursor.description]
    results = cursor.fetchall()
    cursor.close()
    return_results = list()
    for result in results:
        result_dict = dict(zip(columns, result))
        print(result_dict)
        return_results.append(result_dict)
    return return_results