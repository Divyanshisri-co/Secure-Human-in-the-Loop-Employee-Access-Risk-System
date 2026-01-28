import sqlite3
from db import get_connection

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT,
        employee_id TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS access_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        department TEXT,
        role TEXT,
        requested_access TEXT,
        access_sensitivity INTEGER,
        tenure_years INTEGER,
        past_violations INTEGER,
        risk_level TEXT,
        model_confidence REAL,
        top_risk_factors TEXT,
        status TEXT,
        reviewed_by TEXT,
        reviewed_at DATETIME
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_id INTEGER,
        action TEXT,
        performed_by TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
if __name__ == "__main__":
    init_db()
    
print("Database initialized")
