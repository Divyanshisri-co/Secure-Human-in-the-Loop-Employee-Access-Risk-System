import sqlite3
import os
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db.sqlite")

def get_connection():
    return sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )


def save_request(data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO access_requests (
            employee_id, department, role, requested_access,
            access_sensitivity, tenure_years, past_violations,
            risk_level, model_confidence, top_risk_factors,
            status, reviewed_by, reviewed_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)

    conn.commit()



def log_action(cur, request_id, action, performed_by):
    cur.execute("""
        INSERT INTO audit_logs (request_id, action, performed_by)
        VALUES (?, ?, ?)
    """, (request_id, action, performed_by))
  
    
