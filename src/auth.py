import sqlite3
from db import get_connection
DB = "db.sqlite"

def authenticate(username, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT role, employee_id
        FROM users
        WHERE username=? AND password=?
    """, (username, password))

    row = cur.fetchone()
    return row if row else None
