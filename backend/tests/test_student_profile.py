import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.database import Base, engine, SessionLocal
from src.models.all_models import User, Student
from src.models.enums import UserRole

# For tests, we use the SQLite DB setup in config.py. 
# The seed.py was already run, so we can authenticate as the seeded users.
# Student 1: student1@college.edu (password: stu123)

client = TestClient(app)

@pytest.fixture(scope="module")
def student_token():
    # Login as Student 1
    response = client.post("/api/v1/auth/login", data={"username": "student1@college.edu", "password": "stu123"})
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture(scope="module")
def headers(student_token):
    return {"Authorization": f"Bearer {student_token}"}

def test_get_profile(headers):
    response = client.get("/api/v1/students/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["student_identifier"] == "STU001"
    assert data["first_name"] == "Alice"

def test_update_profile(headers):
    response = client.put(
        "/api/v1/students/me", 
        headers=headers,
        json={
            "phone": "999-888-7777",
            "profile_metadata": {"bio": "Updated bio"}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["phone"] == "999-888-7777"
    assert data["profile_metadata"]["bio"] == "Updated bio"

def test_add_update_and_get_academic_history(headers):
    response = client.post(
        "/api/v1/students/me/academic",
        headers=headers,
        json={
            "qualification": "B.Tech",
            "institution": "Engineering College",
            "score_value": 8.5,
            "score_type": "CGPA"
        }
    )
    assert response.status_code == 200
    hist_id = response.json()["id"]

    # Verify it was added
    resp_get = client.get("/api/v1/students/me/academic", headers=headers)
    assert resp_get.status_code == 200
    assert any(h["id"] == hist_id for h in resp_get.json())

    # Update it
    resp_put = client.put(
        f"/api/v1/students/me/academic/{hist_id}",
        headers=headers,
        json={"institution": "Updated Engineering College", "score_value": 8.9}
    )
    assert resp_put.status_code == 200
    assert resp_put.json()["institution"] == "Updated Engineering College"
    assert resp_put.json()["score_value"] == 8.9

    # Delete it
    resp_del = client.delete(f"/api/v1/students/me/academic/{hist_id}", headers=headers)
    assert resp_del.status_code == 204

def test_add_update_and_get_skills(headers):
    # Add a new skill
    response = client.post(
        "/api/v1/students/me/skills",
        headers=headers,
        json={
            "skill_name": "Kubernetes",
            "proficiency_level": "INTERMEDIATE",
            "months_experience": 6,
            "source": "STUDENT"
        }
    )
    assert response.status_code == 200
    skill_id = response.json()["id"]

    # Verify
    resp_get = client.get("/api/v1/students/me/skills", headers=headers)
    assert resp_get.status_code == 200
    skills = resp_get.json()
    assert any(s["id"] == skill_id for s in skills)

    # Update skill
    resp_put = client.put(
        f"/api/v1/students/me/skills/{skill_id}",
        headers=headers,
        json={
            "proficiency_level": "ADVANCED",
            "months_experience": 12
        }
    )
    assert resp_put.status_code == 200
    assert resp_put.json()["proficiency_level"] == "ADVANCED"
    assert resp_put.json()["months_experience"] == 12

    # Delete
    resp_del = client.delete(f"/api/v1/students/me/skills/{skill_id}", headers=headers)
    assert resp_del.status_code == 204

def test_projects_crud(headers):
    # Add project
    resp_post = client.post(
        "/api/v1/students/me/projects",
        headers=headers,
        json={
            "title": "Placement Portal",
            "description": "Full-stack AI placement platform",
            "technologies": "FastAPI, React, PostgreSQL",
            "project_url": "https://github.com/example/portal"
        }
    )
    assert resp_post.status_code == 200
    proj_id = resp_post.json()["id"]

    # Get projects
    resp_get = client.get("/api/v1/students/me/projects", headers=headers)
    assert resp_get.status_code == 200
    assert any(p["id"] == proj_id for p in resp_get.json())

    # Update project
    resp_put = client.put(
        f"/api/v1/students/me/projects/{proj_id}",
        headers=headers,
        json={"title": "Placement Portal Pro"}
    )
    assert resp_put.status_code == 200
    assert resp_put.json()["title"] == "Placement Portal Pro"

    # Delete project
    resp_del = client.delete(f"/api/v1/students/me/projects/{proj_id}", headers=headers)
    assert resp_del.status_code == 204

def test_certifications_crud(headers):
    # Add certification
    resp_post = client.post(
        "/api/v1/students/me/certifications",
        headers=headers,
        json={
            "name": "AWS Certified Solutions Architect",
            "issuing_org": "Amazon Web Services",
            "credential_id": "AWS-12345"
        }
    )
    assert resp_post.status_code == 200
    cert_id = resp_post.json()["id"]

    # Get certifications
    resp_get = client.get("/api/v1/students/me/certifications", headers=headers)
    assert resp_get.status_code == 200
    assert any(c["id"] == cert_id for c in resp_get.json())

    # Update certification
    resp_put = client.put(
        f"/api/v1/students/me/certifications/{cert_id}",
        headers=headers,
        json={"credential_id": "AWS-99999"}
    )
    assert resp_put.status_code == 200
    assert resp_put.json()["credential_id"] == "AWS-99999"

    # Delete certification
    resp_del = client.delete(f"/api/v1/students/me/certifications/{cert_id}", headers=headers)
    assert resp_del.status_code == 204

def test_profile_completeness(headers):
    response = client.get("/api/v1/students/me/completeness", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "percentage" in data
    assert "completed_sections" in data
    assert "missing_sections" in data

def test_get_full_profile(headers):
    response = client.get("/api/v1/students/me/full", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "basic_info" in data
    assert "academic_history" in data
    assert "skills" in data
    assert "projects" in data
    assert "certifications" in data
    assert "assessments" in data
    assert "completeness" in data
