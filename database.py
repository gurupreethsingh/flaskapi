import sqlite3
from flask import g

def connect_to_database():
    sql = sqlite3.connect('H:/flask_applications/flask_member_api/memberapi.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_database():
    if not hasattr(g, 'member_db'):
        g.member_db = connect_to_database()
    return g.member_db