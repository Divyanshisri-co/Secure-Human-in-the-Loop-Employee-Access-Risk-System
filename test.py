from db import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("SELECT username, role, password, employee_id FROM users")
for row in cur.fetchall():
    print(row)

conn.close()