import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@pytest.fixture(scope="module")
def recruiter_token():
    # Login as Recruiter 1
    response = client.post("/api/v1/auth/login", data={"username": "recruiter1@comp1.com", "password": "rec123"})
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture(scope="module")
def student_token():
    # Login as Student 1
    response = client.post("/api/v1/auth/login", data={"username": "student1@college.edu", "password": "stu123"})
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture(scope="module")
def r_headers(recruiter_token):
    return {"Authorization": f"Bearer {recruiter_token}"}

@pytest.fixture(scope="module")
def s_headers(student_token):
    return {"Authorization": f"Bearer {student_token}"}

def test_get_company(r_headers):
    response = client.get("/api/v1/recruiters/me", headers=r_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["company"]["name"] in ["TechCorp", "TechCorp Updated"]

def test_update_company(r_headers):
    response = client.put(
        "/api/v1/recruiters/me/company",
        headers=r_headers,
        json={"name": "TechCorp Updated", "industry": "AI Solutions", "size": "100-500"}
    )
    assert response.status_code == 200
    assert response.json()["industry"] == "AI Solutions"

def test_create_and_get_job(r_headers):
    response = client.post(
        "/api/v1/recruiters/me/jobs",
        headers=r_headers,
        json={
            "title": "Machine Learning Engineer",
            "description": "Build ML models",
            "employment_type": "Full-time",
            "remote_type": "Hybrid",
            "eligibility_config": {"min_cgpa": 8.0, "allowed_branches": ["CSE"]},
            "status": "PUBLISHED"
        }
    )
    assert response.status_code == 200
    job_id = response.json()["id"]

    # Get job
    res = client.get(f"/api/v1/recruiters/me/jobs/{job_id}", headers=r_headers)
    assert res.status_code == 200
    assert res.json()["title"] == "Machine Learning Engineer"

def test_check_eligibility(r_headers):
    # Student 1 is STU001: Alice, Branch "Computer Science", CGPA 9.2
    # Seed job 1 requires min_cgpa 8.0, allowed branches "Computer Science", "CSE", "IT"
    # Seed job 1 id should be 1
    response = client.post(
        "/api/v1/jobs/1/eligibility/check?student_id=1",
        headers=r_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["eligible"] is True

def test_check_ineligibility(r_headers):
    # Job 1 requires min_cgpa 8.0
    # Student 2 is STU002: Bob, Branch "Information Technology", CGPA 7.5
    # So Bob is ineligible because 7.5 < 8.0
    response = client.post(
        "/api/v1/jobs/1/eligibility/check?student_id=2",
        headers=r_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["eligible"] is False
    assert "cgpa_below_minimum" in data["failed_rules"]

def test_student_register_drive(s_headers):
    # Student 1 registers for Drive 2 (Innovate Intern Drive)
    response = client.post(
        "/api/v1/drives/2/candidates",
        headers=s_headers,
        json={"student_id": 1}
    )
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        assert response.json()["eligibility_status"] is True

def test_student_register_duplicate(s_headers):
    response = client.post(
        "/api/v1/drives/2/candidates",
        headers=s_headers,
        json={"student_id": 1}
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]
