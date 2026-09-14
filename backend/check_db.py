import sqlite3
import os

db_path = 'campuslink_test.db'
if not os.path.exists(db_path):
    print("No test db, checking default")
    db_path = 'campuslink.db'

if not os.path.exists(db_path):
    print("No DB found")
else:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT email FROM users WHERE role="STUDENT" LIMIT 1')
    res = c.fetchone()
    print("Student email:", res[0] if res else "None")
