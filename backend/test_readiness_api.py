import sqlite3
import requests
import json

db_path = '../campuslink_test.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Get a student user
c.execute('SELECT email FROM users WHERE role="STUDENT" LIMIT 1')
res = c.fetchone()
if not res:
    print("No student found in DB")
    exit(1)

student_email = res[0]
print(f"Testing with student: {student_email}")

# Login
login_url = "http://localhost:8000/api/v1/auth/login"
resp = requests.post(login_url, data={"username": student_email, "password": "password"})
if resp.status_code != 200:
    print("Login failed:", resp.status_code, resp.text)
    exit(1)

token = resp.json()['access_token']
headers = {"Authorization": f"Bearer {token}"}

# 1. Recalculate Readiness
print("\n--- Testing POST /api/v1/readiness/me/recalculate ---")
r_recalc = requests.post("http://localhost:8000/api/v1/readiness/me/recalculate", headers=headers)
print("Status:", r_recalc.status_code)
if r_recalc.status_code == 200:
    data = r_recalc.json()
    print("Overall Score:", data.get("overall_score"))
    print("Readiness Level:", data.get("readiness_level"))
else:
    print("Error:", r_recalc.text)

# 2. Get Available Jobs
print("\n--- Testing GET /api/v1/jobs/available ---")
r_jobs = requests.get("http://localhost:8000/api/v1/jobs/available", headers=headers)
print("Status:", r_jobs.status_code)
jobs = []
if r_jobs.status_code == 200:
    jobs = r_jobs.json()
    print(f"Found {len(jobs)} jobs.")
else:
    print("Error:", r_jobs.text)

# 3. Get Skill Gap for a Job
if jobs:
    job_id = jobs[0]['id']
    job_title = jobs[0]['title']
    print(f"\n--- Testing GET /api/v1/readiness/me/jobs/{job_id}/skill-gaps ({job_title}) ---")
    r_gap = requests.get(f"http://localhost:8000/api/v1/readiness/me/jobs/{job_id}/skill-gaps", headers=headers)
    print("Status:", r_gap.status_code)
    if r_gap.status_code == 200:
        gap_data = r_gap.json()
        print("Match Score:", gap_data.get("match_score"))
        print("Missing Skills:", [s['name'] for s in gap_data.get('missing_skills', [])])
    else:
        print("Error:", r_gap.text)
else:
    print("No jobs found to test skill gaps.")
