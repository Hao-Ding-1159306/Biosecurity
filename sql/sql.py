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
        return result_dict
    return {}


def search_agronomists(id: int):
    cursor = get_cursor()
    cursor.execute(f"SELECT * FROM agronomists WHERE id = {id}")
    columns = [col[0] for col in cursor.description]
    result = cursor.fetchone()
    cursor.close()
    if result:
        result_dict = dict(zip(columns, result))
        return result_dict
    return {}


def get_info(id: int, role: str):
    if role == 'admin':
        return search_admin(id)
    elif role == 'staff':
        return search_staff(id)
    elif role == 'agronomists':
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


def get_staff_list():
    cursor = get_cursor()
    cursor.execute(f"SELECT * FROM staff")
    columns = [col[0] for col in cursor.description]
    results = cursor.fetchall()
    cursor.close()
    return_results = list()
    for result in results:
        result_dict = dict(zip(columns, result))
        print(result_dict)
        return_results.append(result_dict)
    return return_results


def search_pests_dict():
    cursor = get_cursor()
    cursor.execute(f"SELECT agriculture_id, common_name FROM agriculture WHERE agriculture_item_type = 'pest'")
    columns = [col[0] for col in cursor.description]
    results = cursor.fetchall()
    cursor.close()
    return_results = list()
    for result in results:
        result_dict = dict(zip(columns, result))
        photo_url = get_primary_picture(result_dict["agriculture_id"])
        result_dict['primary_photos'] = photo_url
        return_results.append(result_dict)
    return return_results


def search_weeds_dict():
    cursor = get_cursor()
    cursor.execute(f"SELECT agriculture_id, common_name FROM agriculture WHERE agriculture_item_type = 'weed'")
    columns = [col[0] for col in cursor.description]
    results = cursor.fetchall()
    cursor.close()
    return_results = list()
    for result in results:
        result_dict = dict(zip(columns, result))
        photo_url = get_primary_picture(result_dict["agriculture_id"])
        result_dict['primary_photos'] = photo_url
        return_results.append(result_dict)
    return return_results

def search_agriculture(agriculture_id):
    cursor = get_cursor()
    cursor.execute(f"SELECT * FROM agriculture WHERE agriculture_id = {agriculture_id}")
    columns = [col[0] for col in cursor.description]
    result = cursor.fetchone()
    cursor.close()
    if result:
        result_dict = dict(zip(columns, result))
        photo_dict = get_pictures(result_dict["agriculture_id"])
        result_dict['photos'] = photo_dict
        return result_dict
    else:
        return None


def get_pictures(agriculture_id):
    cursor = get_cursor()
    cursor.execute("""
            SELECT p.photo_id, p.photo_url, ap.is_primary
            FROM photos p
            JOIN agriculture_photos ap ON p.photo_id = ap.photo_id
            WHERE ap.agriculture_id = %s
        """, (agriculture_id,))
    columns = [col[0] for col in cursor.description]
    results = cursor.fetchall()
    connection.close()
    return_results = list()
    for result in results:
        result_dict = dict(zip(columns, result))
        return_results.append(result_dict)
    print(return_results)
    return return_results

def get_primary_picture(agriculture_id):
    cursor = get_cursor()
    cursor.execute("""
                SELECT p.photo_url
                FROM photos p
                JOIN agriculture_photos ap ON p.photo_id = ap.photo_id
                WHERE ap.is_primary = 1 AND ap.agriculture_id = %s
            """, (agriculture_id,))
    result = cursor.fetchone()
    connection.close()
    if result is not None:
        return result[0]
    return None