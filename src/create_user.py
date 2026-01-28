import sqlite3

conn = sqlite3.connect("db.sqlite")
cur = conn.cursor()

users = [
    ("emp01", "pass101", "employee", "E001"),
    ("emp02", "pass202", "employee", "E002"),
    ("emp03", "pass303", "employee", "E003"),
    ("emp04", "pass404", "employee", "E004"),
    ("emp05", "pass505", "employee", "E005"),
    ("emp06", "pass606", "employee", "E006"),
    ("emp07", "pass707", "employee", "E007"),
    ("emp08", "pass808", "employee", "E008"),
    ("emp09", "pass909", "employee", "E009"),
    ("emp10", "pass100", "employee", "E010"),
    ("reviewer", "review123", "reviewer", None),
    ("admin", "admin123", "admin", None),
]

cur.executemany("""
INSERT OR IGNORE INTO users (username, password, role, employee_id)
VALUES (?, ?, ?, ?)
""", users)

conn.commit()
conn.close()
print("user inserted successfully")