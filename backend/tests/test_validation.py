import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from src.main import app
from src.core.database import SessionLocal
from src.models.all_models import Student, Job, JobRequirement, PlacementDrive

client = TestClient(app)

@pytest.fixture(scope="module")
def student_headers():
    response = client.post("/api/v1/auth/login", data={"username": "student1@college.edu", "password": "stu123"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="module")
def recruiter_headers():
    response = client.post("/api/v1/auth/login", data={"username": "recruiter1@comp1.com", "password": "rec123"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# ==========================================
# 1. STUDENT VALIDATION TESTS
# ==========================================

def test_student_profile_cgpa_out_of_bounds(student_headers):
    # CGPA > 10 rejected
    res = client.put("/api/v1/students/me", headers=student_headers, json={"cgpa": 11.5})
    assert res.status_code == 422

    # CGPA < 0 rejected
    res = client.put("/api/v1/students/me", headers=student_headers, json={"cgpa": -1.0})
    assert res.status_code == 422

def test_student_profile_negative_backlogs(student_headers):
    res = client.put("/api/v1/students/me", headers=student_headers, json={"backlogs_current": -2})
    assert res.status_code == 422

def test_student_profile_dob_future_rejected(student_headers):
    future_dob = (datetime.now() + timedelta(days=365)).isoformat()
    res = client.put("/api/v1/students/me", headers=student_headers, json={"dob": future_dob})
    assert res.status_code == 422
    assert "future" in res.text.lower()

def test_student_profile_invalid_phone(student_headers):
    res = client.put("/api/v1/students/me", headers=student_headers, json={"phone": "123"})
    assert res.status_code == 422
    assert "digits" in res.text.lower()

def test_student_profile_invalid_urls(student_headers):
    res = client.put(
        "/api/v1/students/me",
        headers=student_headers,
        json={"profile_metadata": {"linkedin_url": "ftp://not-http-url"}}
    )
    assert res.status_code == 422

def test_academic_history_validation(student_headers):
    # Score type CGPA cannot exceed 10.0
    res = client.post(
        "/api/v1/students/me/academic",
        headers=student_headers,
        json={
            "qualification": "B.Tech",
            "institution": "Tech Institute",
            "score_value": 15.0,
            "score_type": "CGPA"
        }
    )
    assert res.status_code == 422
    assert "10.0" in res.text

    # Score type PERCENTAGE cannot exceed 100.0
    res = client.post(
        "/api/v1/students/me/academic",
        headers=student_headers,
        json={
            "qualification": "12th Standard",
            "institution": "High School",
            "score_value": 105.0,
            "score_type": "PERCENTAGE"
        }
    )
    assert res.status_code == 422
    assert "100.0" in res.text

    # Invalid score_type
    res = client.post(
        "/api/v1/students/me/academic",
        headers=student_headers,
        json={
            "qualification": "B.Tech",
            "institution": "Tech Institute",
            "score_value": 8.0,
            "score_type": "INVALID_TYPE"
        }
    )
    assert res.status_code == 422

    # start_year > end_year rejected
    res = client.post(
        "/api/v1/students/me/academic",
        headers=student_headers,
        json={
            "qualification": "B.Tech",
            "institution": "Tech Institute",
            "start_year": 2024,
            "end_year": 2020,
            "score_value": 8.0,
            "score_type": "CGPA"
        }
    )
    assert res.status_code == 422
    assert "precede" in res.text.lower()

def test_skills_validation(student_headers):
    # Negative experience rejected
    res = client.post(
        "/api/v1/students/me/skills",
        headers=student_headers,
        json={
            "skill_name": "Rust",
            "proficiency_level": "BEGINNER",
            "months_experience": -5
        }
    )
    assert res.status_code == 422

    # Empty skill name rejected
    res = client.post(
        "/api/v1/students/me/skills",
        headers=student_headers,
        json={
            "skill_name": "",
            "proficiency_level": "BEGINNER",
            "months_experience": 2
        }
    )
    assert res.status_code == 422

def test_project_validation(student_headers):
    # Description required and min length 5
    res = client.post(
        "/api/v1/students/me/projects",
        headers=student_headers,
        json={
            "title": "My Project",
            "description": "Tiny" # < 5 characters
        }
    )
    assert res.status_code == 422

    # Invalid project URL rejected
    res = client.post(
        "/api/v1/students/me/projects",
        headers=student_headers,
        json={
            "title": "My Project",
            "description": "Full valid project description.",
            "project_url": "ftp://bad-url"
        }
    )
    assert res.status_code == 422

def test_certification_validation(student_headers):
    # Expiry before issue date rejected
    issue = datetime.now().isoformat()
    expiry = (datetime.now() - timedelta(days=30)).isoformat()
    res = client.post(
        "/api/v1/students/me/certifications",
        headers=student_headers,
        json={
            "name": "Cloud Practitioner",
            "issuing_org": "AWS",
            "issue_date": issue,
            "expiry_date": expiry
        }
    )
    assert res.status_code == 422

    # Issue date in the future rejected
    future_issue = (datetime.now() + timedelta(days=10)).isoformat()
    res = client.post(
        "/api/v1/students/me/certifications",
        headers=student_headers,
        json={
            "name": "Cloud Practitioner",
            "issuing_org": "AWS",
            "issue_date": future_issue
        }
    )
    assert res.status_code == 422

def test_resume_upload_size_limit(student_headers):
    # Over 5MB rejected
    huge_content = b"%PDF-1.4 " + b"A" * (5 * 1024 * 1024 + 100)
    files = {"file": ("huge_resume.pdf", huge_content, "application/pdf")}
    res = client.post("/api/v1/students/me/resume", headers=student_headers, files=files)
    assert res.status_code == 400
    assert "5MB" in res.text

# ==========================================
# 2. RECRUITER VALIDATION TESTS
# ==========================================

def test_recruiter_company_validation(recruiter_headers):
    # Company name min length 2
    res = client.put("/api/v1/recruiters/me/company", headers=recruiter_headers, json={"name": "A"})
    assert res.status_code == 422

    # Invalid website URL
    res = client.put("/api/v1/recruiters/me/company", headers=recruiter_headers, json={"name": "Tech Corp", "website": "ftp://corp"})
    assert res.status_code == 422

def test_recruiter_job_validation(recruiter_headers):
    # Openings <= 0 rejected
    res = client.post(
        "/api/v1/recruiters/me/jobs",
        headers=recruiter_headers,
        json={
            "title": "Software Engineer",
            "description": "A comprehensive job description for hiring engineers.",
            "employment_type": "Full-time",
            "openings": 0
        }
    )
    assert res.status_code == 422

    # Application deadline in past rejected
    past_date = (datetime.now() - timedelta(days=1)).isoformat()
    res = client.post(
        "/api/v1/recruiters/me/jobs",
        headers=recruiter_headers,
        json={
            "title": "Software Engineer",
            "description": "A comprehensive job description for hiring engineers.",
            "employment_type": "Full-time",
            "application_deadline": past_date
        }
    )
    assert res.status_code == 422

    # Eligibility min_cgpa > 10 rejected
    res = client.post(
        "/api/v1/recruiters/me/jobs",
        headers=recruiter_headers,
        json={
            "title": "Software Engineer",
            "description": "A comprehensive job description for hiring engineers.",
            "employment_type": "Full-time",
            "eligibility_config": {"min_cgpa": 12.0}
        }
    )
    assert res.status_code == 422

    # Eligibility max_backlogs < 0 rejected
    res = client.post(
        "/api/v1/recruiters/me/jobs",
        headers=recruiter_headers,
        json={
            "title": "Software Engineer",
            "description": "A comprehensive job description for hiring engineers.",
            "employment_type": "Full-time",
            "eligibility_config": {"max_backlogs": -1}
        }
    )
    assert res.status_code == 422

def test_recruiter_job_status_transition(recruiter_headers):
    # Create valid job
    res = client.post(
        "/api/v1/recruiters/me/jobs",
        headers=recruiter_headers,
        json={
            "title": "DevOps Engineer",
            "description": "Responsible for managing CI/CD pipelines and infrastructure.",
            "employment_type": "Full-time",
            "status": "CLOSED"
        }
    )
    assert res.status_code == 200
    job_id = res.json()["id"]

    # Attempt invalid transition CLOSED -> DRAFT
    res_update = client.put(
        f"/api/v1/recruiters/me/jobs/{job_id}",
        headers=recruiter_headers,
        json={"status": "DRAFT"}
    )
    assert res_update.status_code == 400
    assert "cannot revert" in res_update.text.lower()

def test_job_requirement_validation(recruiter_headers):
    # Weight < 0.1 rejected
    res = client.post(
        "/api/v1/jobs/1/requirements",
        headers=recruiter_headers,
        json={
            "skill_id": 1,
            "required_proficiency": "INTERMEDIATE",
            "weight": 0.05
        }
    )
    assert res.status_code == 422

    # Weight > 10.0 rejected
    res = client.post(
        "/api/v1/jobs/1/requirements",
        headers=recruiter_headers,
        json={
            "skill_id": 1,
            "required_proficiency": "INTERMEDIATE",
            "weight": 12.0
        }
    )
    assert res.status_code == 422

    # Non-existent skill rejected
    res = client.post(
        "/api/v1/jobs/1/requirements",
        headers=recruiter_headers,
        json={
            "skill_id": 999999,
            "required_proficiency": "INTERMEDIATE",
            "weight": 1.0
        }
    )
    assert res.status_code == 404

def test_placement_drive_validation(recruiter_headers):
    now = datetime.now()
    start = (now + timedelta(days=5)).isoformat()
    end_before_start = (now + timedelta(days=5, hours=-2)).isoformat()

    # End time <= start time rejected
    res = client.post(
        "/api/v1/recruiters/me/drives",
        headers=recruiter_headers,
        json={
            "name": "Annual Placement Drive 2026",
            "job_id": 1,
            "date": start,
            "start_time": start,
            "end_time": end_before_start
        }
    )
    assert res.status_code == 422

    # Registration deadline after start time rejected
    reg_deadline_after_start = (now + timedelta(days=6)).isoformat()
    valid_end = (now + timedelta(days=5, hours=4)).isoformat()
    res = client.post(
        "/api/v1/recruiters/me/drives",
        headers=recruiter_headers,
        json={
            "name": "Annual Placement Drive 2026",
            "job_id": 1,
            "date": start,
            "start_time": start,
            "end_time": valid_end,
            "registration_deadline": reg_deadline_after_start
        }
    )
    assert res.status_code == 422

    # Invalid job_id rejected
    res = client.post(
        "/api/v1/recruiters/me/drives",
        headers=recruiter_headers,
        json={
            "name": "Annual Placement Drive 2026",
            "job_id": 999999,
            "date": start,
            "start_time": start,
            "end_time": valid_end
        }
    )
    assert res.status_code == 400

    # Capacity <= 0 rejected
    res = client.post(
        "/api/v1/recruiters/me/drives",
        headers=recruiter_headers,
        json={
            "name": "Annual Placement Drive 2026",
            "job_id": 1,
            "date": start,
            "start_time": start,
            "end_time": valid_end,
            "capacity": 0
        }
    )
    assert res.status_code == 422
