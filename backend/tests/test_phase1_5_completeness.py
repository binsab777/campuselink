import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import uuid
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


@pytest.fixture(scope="module")
def recruiter_token():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "recruiter1@comp1.com", "password": "rec123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(scope="module")
def student_token():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "student1@college.edu", "password": "stu123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(scope="module")
def r_headers(recruiter_token):
    return {"Authorization": f"Bearer {recruiter_token}"}


@pytest.fixture(scope="module")
def s_headers(student_token):
    return {"Authorization": f"Bearer {student_token}"}


def test_registration_student_creates_profile():
    unique_email = f"stu_audit_{uuid.uuid4().hex[:6]}@college.edu"
    res = client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "password": "Password123!",
            "full_name": "Audit Student",
            "role": "STUDENT",
        },
    )
    assert res.status_code in [200, 201]
    assert res.json()["email"] == unique_email
    assert res.json()["role"] == "STUDENT"

    # Login and verify student record was initialized
    login_res = client.post(
        "/api/v1/auth/login",
        data={"username": unique_email, "password": "Password123!"},
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    profile_res = client.get("/api/v1/students/me", headers=headers)
    assert profile_res.status_code == 200
    profile_data = profile_res.json()
    assert profile_data["student_identifier"].startswith("STU")


def test_registration_recruiter_creates_company_and_profile():
    unique_email = f"rec_audit_{uuid.uuid4().hex[:6]}@company.com"
    res = client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "password": "Password123!",
            "full_name": "Audit Recruiter",
            "role": "RECRUITER",
        },
    )
    assert res.status_code in [200, 201]
    assert res.json()["email"] == unique_email
    assert res.json()["role"] == "RECRUITER"

    # Login and verify recruiter profile and company were initialized
    login_res = client.post(
        "/api/v1/auth/login",
        data={"username": unique_email, "password": "Password123!"},
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    rec_res = client.get("/api/v1/recruiters/me", headers=headers)
    assert rec_res.status_code == 200
    rec_data = rec_res.json()
    assert rec_data["company"] is not None
    assert "Technologies" in rec_data["company"]["name"]


def test_registration_admin_forbidden():
    res = client.post(
        "/api/v1/auth/register",
        json={
            "email": "hacker_admin@evil.com",
            "password": "Password123!",
            "full_name": "Fake Admin",
            "role": "SUPER_ADMIN",
        },
    )
    assert res.status_code == 403
    assert res.json()["detail"] == "Cannot register as SUPER_ADMIN"


def test_student_available_jobs_and_eligibility(s_headers):
    # Available jobs list for students
    res = client.get("/api/v1/jobs/available", headers=s_headers)
    assert res.status_code == 200
    jobs = res.json()
    assert isinstance(jobs, list)

    if len(jobs) > 0:
        first_job_id = jobs[0]["id"]
        # Live eligibility check
        elig_res = client.get(
            f"/api/v1/jobs/{first_job_id}/my-eligibility", headers=s_headers
        )
        assert elig_res.status_code == 200
        elig_data = elig_res.json()
        assert "eligible" in elig_data
        assert "reasons" in elig_data


def test_student_available_drives_and_registration(s_headers):
    # Available drives list
    res = client.get("/api/v1/drives/available", headers=s_headers)
    assert res.status_code == 200
    drives = res.json()
    assert isinstance(drives, list)

    # Student registered drives
    my_drives_res = client.get("/api/v1/students/me/drives", headers=s_headers)
    assert my_drives_res.status_code == 200
    assert isinstance(my_drives_res.json(), list)


def test_recruiter_dashboard_metrics(r_headers):
    res = client.get("/api/v1/recruiters/me/dashboard", headers=r_headers)
    assert res.status_code == 200
    metrics = res.json()
    assert "active_jobs_count" in metrics
    assert "upcoming_drives_count" in metrics
    assert "total_candidates_count" in metrics
    assert "shortlisted_candidates_count" in metrics
    assert metrics["active_jobs_count"] >= 0


def test_recruiter_candidates_and_bulk_evaluation(r_headers):
    # Drive 1 candidates
    res = client.get("/api/v1/drives/1/candidates", headers=r_headers)
    assert res.status_code == 200
    candidates = res.json()
    assert isinstance(candidates, list)

    # Bulk evaluation
    bulk_res = client.post("/api/v1/drives/1/evaluate-eligibility", headers=r_headers)
    assert bulk_res.status_code == 200
    bulk_data = bulk_res.json()
    assert bulk_data["drive_id"] == 1
    assert "total_candidates" in bulk_data
    assert "eligible_count" in bulk_data

    # Candidate profile view
    cand_profile_res = client.get(
        "/api/v1/recruiters/candidates/1", headers=r_headers
    )
    assert cand_profile_res.status_code == 200
    cand_profile = cand_profile_res.json()
    assert "first_name" in cand_profile
    assert "cgpa" in cand_profile
    assert "skills" in cand_profile
