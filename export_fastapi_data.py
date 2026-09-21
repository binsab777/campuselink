import sqlite3
import json
import os

db_path = r'D:\xampp\htdocs\campuslink\campuslink_test.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def fetch_all(table):
    cursor.execute(f'SELECT * FROM {table}')
    return [dict(row) for row in cursor.fetchall()]

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [r[0] for r in cursor.fetchall()]

data = {}
for table in tables:
    data[table] = fetch_all(table)

with open('fastapi_data_snapshot.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, default=str)

print('Exported tables:', tables)
