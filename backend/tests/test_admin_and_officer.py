import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import uuid
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


@pytest.fixture(scope="module")
def admin_token():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@campuslink.com", "password": "admin123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(scope="module")
def officer_token():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "po@campuslink.com", "password": "po123"},
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
def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture(scope="module")
def officer_headers(officer_token):
    return {"Authorization": f"Bearer {officer_token}"}


@pytest.fixture(scope="module")
def student_headers(student_token):
    return {"Authorization": f"Bearer {student_token}"}


def test_admin_list_and_search_users(admin_headers, student_headers):
    # Admin can list users
    res = client.get("/api/v1/admin/users", headers=admin_headers)
    assert res.status_code == 200
    data = res.json()
    assert "total" in data
    assert "users" in data
    assert data["total"] > 0

    # Search by email
    search_res = client.get("/api/v1/admin/users?query=student1", headers=admin_headers)
    assert search_res.status_code == 200
    assert any("student1" in u["email"] for u in search_res.json()["users"])

    # Filter by role
    role_res = client.get("/api/v1/admin/users?role=RECRUITER", headers=admin_headers)
    assert role_res.status_code == 200
    assert all(u["role"] == "RECRUITER" for u in role_res.json()["users"])

    # Non-admin/officer cannot access admin users
    unauth_res = client.get("/api/v1/admin/users", headers=student_headers)
    assert unauth_res.status_code == 403


def test_admin_toggle_user_status(admin_headers):
    # Toggle student 10 active status
    # First get a non-admin user
    users_res = client.get("/api/v1/admin/users?role=STUDENT", headers=admin_headers)
    assert users_res.status_code == 200
    target_user = users_res.json()["users"][0]
    target_id = target_user["id"]

    # Deactivate
    deact_res = client.patch(
        f"/api/v1/admin/users/{target_id}/status",
        headers=admin_headers,
        json={"is_active": False},
    )
    assert deact_res.status_code == 200
    assert deact_res.json()["is_active"] is False

    # Reactivate
    react_res = client.patch(
        f"/api/v1/admin/users/{target_id}/status",
        headers=admin_headers,
        json={"is_active": True},
    )
    assert react_res.status_code == 200
    assert react_res.json()["is_active"] is True


def test_admin_change_user_role(admin_headers, officer_headers):
    # Find a test user to change role
    users_res = client.get("/api/v1/admin/users?role=STUDENT", headers=admin_headers)
    target_id = users_res.json()["users"][0]["id"]

    # Officer cannot change role (only Super Admin)
    officer_attempt = client.patch(
        f"/api/v1/admin/users/{target_id}/role",
        headers=officer_headers,
        json={"role": "MENTOR"},
    )
    assert officer_attempt.status_code == 403

    # Super Admin can change role
    admin_change = client.patch(
        f"/api/v1/admin/users/{target_id}/role",
        headers=admin_headers,
        json={"role": "MENTOR"},
    )
    assert admin_change.status_code == 200
    assert admin_change.json()["role"] == "MENTOR"

    # Revert back to STUDENT
    revert_res = client.patch(
        f"/api/v1/admin/users/{target_id}/role",
        headers=admin_headers,
        json={"role": "STUDENT"},
    )
    assert revert_res.status_code == 200
    assert revert_res.json()["role"] == "STUDENT"


def test_master_skills_catalog_crud(officer_headers, student_headers):
    unique_skill_name = f"Skill_{uuid.uuid4().hex[:6]}"

    # Student cannot create master skill
    student_create = client.post(
        "/api/v1/skills",
        headers=student_headers,
        json={"name": unique_skill_name, "category": "Testing"},
    )
    assert student_create.status_code == 403

    # Officer can create master skill
    create_res = client.post(
        "/api/v1/skills",
        headers=officer_headers,
        json={
            "name": unique_skill_name,
            "category": "Testing & QA",
            "description": "Comprehensive automated testing techniques",
        },
    )
    assert create_res.status_code == 200
    skill_id = create_res.json()["id"]

    # Duplicate skill name rejected
    dup_res = client.post(
        "/api/v1/skills",
        headers=officer_headers,
        json={"name": unique_skill_name, "category": "Testing"},
    )
    assert dup_res.status_code == 400

    # Update skill
    update_res = client.put(
        f"/api/v1/skills/{skill_id}",
        headers=officer_headers,
        json={"description": "Updated QA description"},
    )
    assert update_res.status_code == 200
    assert update_res.json()["description"] == "Updated QA description"

    # Delete skill
    delete_res = client.delete(f"/api/v1/skills/{skill_id}", headers=officer_headers)
    assert delete_res.status_code == 200


def test_officer_student_directory_and_profile(officer_headers, student_headers):
    # List students
    res = client.get("/api/v1/officer/students", headers=officer_headers)
    assert res.status_code == 200
    data = res.json()
    assert "total" in data
    assert "students" in data
    assert data["total"] > 0

    first_student_id = data["students"][0]["id"]

    # Student detail inspection
    detail_res = client.get(
        f"/api/v1/officer/students/{first_student_id}",
        headers=officer_headers,
    )
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert "first_name" in detail
    assert "cgpa" in detail
    assert "skills" in detail
    assert "projects" in detail

    # Non-officer cannot access officer students endpoint
    unauth = client.get("/api/v1/officer/students", headers=student_headers)
    assert unauth.status_code == 403


def test_officer_corporate_partners(officer_headers):
    # List companies
    res = client.get("/api/v1/officer/companies", headers=officer_headers)
    assert res.status_code == 200
    companies = res.json()
    assert isinstance(companies, list)
    assert len(companies) > 0

    # Create new corporate partner
    unique_comp_name = f"Enterprise Partner {uuid.uuid4().hex[:6]}"
    create_res = client.post(
        "/api/v1/officer/companies",
        headers=officer_headers,
        json={
            "name": unique_comp_name,
            "industry": "FinTech",
            "size": "500-1000",
            "website": "https://fintechpartner.com",
            "headquarters": "Mumbai",
        },
    )
    assert create_res.status_code == 200
    assert create_res.json()["name"] == unique_comp_name


def test_student_job_apply_and_drive_withdraw(student_headers):
    # Get available jobs
    jobs_res = client.get("/api/v1/jobs/available", headers=student_headers)
    assert jobs_res.status_code == 200
    jobs = jobs_res.json()

    if len(jobs) > 0:
        job_id = jobs[0]["id"]
        # Apply to job
        apply_res = client.post(f"/api/v1/jobs/{job_id}/apply", headers=student_headers)
        assert apply_res.status_code == 200
        assert "application_id" in apply_res.json()

    # Get available drives
    drives_res = client.get("/api/v1/drives/available", headers=student_headers)
    assert drives_res.status_code == 200
    drives = drives_res.json()

    if len(drives) > 0:
        drive_id = drives[0]["id"]
        # Register for drive first if not already
        client.post(
            f"/api/v1/drives/{drive_id}/candidates",
            headers=student_headers,
            json={"student_id": 1},
        )
        # Withdraw from drive
        withdraw_res = client.post(
            f"/api/v1/drives/{drive_id}/withdraw", headers=student_headers
        )
        assert withdraw_res.status_code == 200
        assert withdraw_res.json()["message"] == "Registration withdrawn successfully"
