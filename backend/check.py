import sqlite3
c = sqlite3.connect('../campuslink_test.db').cursor()
user_id = c.execute("SELECT id FROM users WHERE email='teststudent99@test.com'").fetchone()[0]
student = c.execute("SELECT * FROM students WHERE user_id=?", (user_id,)).fetchone()
print(f"User ID: {user_id}")
print(f"Student Record: {student}")
