import requests
import json

base_url = "http://localhost:8000/api/v1"

# 1. Register a new student
print("--- Registering new student ---")
reg_data = {
    "email": "teststudent99@test.com",
    "password": "mypassword123",
    "role": "STUDENT"
}
requests.post(f"{base_url}/auth/register", json=reg_data)

# 2. Login
print("--- Logging in ---")
resp = requests.post(f"{base_url}/auth/login", data={"username": "teststudent99@test.com", "password": "mypassword123"})
if resp.status_code != 200:
    print("Login failed:", resp.status_code, resp.text)
    exit(1)

token = resp.json()['access_token']
headers = {"Authorization": f"Bearer {token}"}

# 3. Create profile to avoid 404 on readiness recalculate
print("--- Creating Profile ---")
profile_data = {
    "first_name": "Test",
    "last_name": "Student",
    "dob": "2000-01-01",
    "phone": "1234567890",
    "branch": "Computer Science",
    "graduation_year": 2026,
    "cgpa": 8.5
}
r_prof = requests.put(f"{base_url}/students/me", headers=headers, json=profile_data)
print("Profile Status:", r_prof.status_code)

# Add a skill so skill gap doesn't complain
skill_data = {
    "skill_name": "Python",
    "proficiency_level": "ADVANCED"
}
requests.post(f"{base_url}/students/me/skills", headers=headers, json=skill_data)

# 1. Recalculate Readiness
print("\n--- Testing POST /readiness/me/recalculate ---")
r_recalc = requests.post(f"{base_url}/readiness/me/recalculate", headers=headers)
print("Status:", r_recalc.status_code)
if r_recalc.status_code == 200:
    data = r_recalc.json()
    print("Overall Score:", data.get("overall_score"))
    print("Readiness Level:", data.get("readiness_level"))
else:
    print("Error:", r_recalc.text)

# 2. Get Available Jobs
print("\n--- Testing GET /jobs/available ---")
r_jobs = requests.get(f"{base_url}/jobs/available", headers=headers)
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
    print(f"\n--- Testing GET /readiness/me/jobs/{job_id}/skill-gaps ({job_title}) ---")
    r_gap = requests.get(f"{base_url}/readiness/me/jobs/{job_id}/skill-gaps", headers=headers)
    print("Status:", r_gap.status_code)
    if r_gap.status_code == 200:
        gap_data = r_gap.json()
        print("Match Score:", gap_data.get("match_score"))
        print("Missing Skills:", [s['name'] for s in gap_data.get('missing_skills', [])])
    else:
        print("Error:", r_gap.text)
else:
    print("No jobs found to test skill gaps.")
