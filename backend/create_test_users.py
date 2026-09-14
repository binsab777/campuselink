import sqlite3
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db_path = '../campuslink_test.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

def ensure_user(email, password, role):
    c.execute("SELECT id FROM users WHERE email=?", (email,))
    res = c.fetchone()
    if res:
        # Update password just in case
        c.execute("UPDATE users SET password_hash=? WHERE email=?", (pwd_context.hash(password), email))
    else:
        c.execute("INSERT INTO users (email, password_hash, role, is_active) VALUES (?, ?, ?, 1)", 
                  (email, pwd_context.hash(password), role))
    conn.commit()

ensure_user('teststudent99@test.com', 'mypassword123', 'STUDENT')
ensure_user('testrecruiter99@test.com', 'mypassword123', 'RECRUITER')
ensure_user('testadmin99@test.com', 'mypassword123', 'SUPER_ADMIN')

print("Test users ensured.")
