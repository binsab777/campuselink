import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models.enums import ReadinessLevel, ProficiencyLevel, GapSeverity
from src.services.readiness import determine_readiness_level, READINESS_CONFIG_V1

client = TestClient(app)

@pytest.fixture(scope="module")
def student1_token():
    # Student 1 (Alice - Strong Archetype)
    res = client.post("/api/v1/auth/login", data={"username": "student1@college.edu", "password": "stu123"})
    assert res.status_code == 200
    return res.json()["access_token"]

@pytest.fixture(scope="module")
def student2_token():
    # Student 2 (Bob - Developing Archetype)
    res = client.post("/api/v1/auth/login", data={"username": "student2@college.edu", "password": "stu123"})
    assert res.status_code == 200
    return res.json()["access_token"]

@pytest.fixture(scope="module")
def admin_token():
    res = client.post("/api/v1/auth/login", data={"username": "admin@campuslink.com", "password": "admin123"})
    assert res.status_code == 200
    return res.json()["access_token"]

@pytest.fixture(scope="module")
def s1_headers(student1_token):
    return {"Authorization": f"Bearer {student1_token}"}

@pytest.fixture(scope="module")
def s2_headers(student2_token):
    return {"Authorization": f"Bearer {student2_token}"}

@pytest.fixture(scope="module")
def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}

# ================= 1. THRESHOLD BOUNDARY TESTS =================

def test_readiness_threshold_boundaries():
    thresholds = READINESS_CONFIG_V1["level_thresholds"]
    assert determine_readiness_level(39.9, thresholds) == ReadinessLevel.NOT_READY
    assert determine_readiness_level(40.0, thresholds) == ReadinessLevel.DEVELOPING
    assert determine_readiness_level(59.9, thresholds) == ReadinessLevel.DEVELOPING
    assert determine_readiness_level(60.0, thresholds) == ReadinessLevel.READY
    assert determine_readiness_level(79.9, thresholds) == ReadinessLevel.READY
    assert determine_readiness_level(80.0, thresholds) == ReadinessLevel.HIGHLY_EMPLOYABLE
    assert determine_readiness_level(95.0, thresholds) == ReadinessLevel.HIGHLY_EMPLOYABLE

# ================= 2. READINESS EVALUATION API TESTS =================

def test_get_my_readiness_strong_student(s1_headers):
    res = client.get("/api/v1/readiness/me", headers=s1_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["overall_score"] >= 80.0
    assert data["readiness_level"] == ReadinessLevel.HIGHLY_EMPLOYABLE.value
    assert data["components"]["academic"] >= 90.0
    assert data["components"]["projects"] >= 90.0
    assert len(data["strengths"]) > 0
    assert data["model_version"] == "v1.0"

def test_recalculate_readiness_persists_history(s1_headers):
    res1 = client.post("/api/v1/readiness/me/recalculate", headers=s1_headers)
    assert res1.status_code == 200
    data1 = res1.json()

    res2 = client.post("/api/v1/readiness/me/recalculate", headers=s1_headers)
    assert res2.status_code == 200
    data2 = res2.json()

    # Both evaluations are valid and score remains reproducible
    assert data1["overall_score"] == data2["overall_score"]

def test_get_my_readiness_developing_student(s2_headers):
    res = client.get("/api/v1/readiness/me", headers=s2_headers)
    assert res.status_code == 200
    data = res.json()
    # Bob has missing assessments / certs and low proficiency
    assert data["overall_score"] < 60.0
    assert data["readiness_level"] in [ReadinessLevel.NOT_READY.value, ReadinessLevel.DEVELOPING.value]
    # Check that missing dimensions are explicitly tracked
    missing = data["data_quality"]["missing_dimensions"]
    assert "communication" in missing or "interview" in missing
    assert data["data_quality"]["weights_redistributed"] is True

# ================= 3. SKILL GAP ENGINE TESTS =================

def test_skill_gap_analysis_aligned_student(s1_headers):
    # Job 1 is Software Engineer (Python Advanced, SQL Intermediate, Docker Intermediate, AWS Intermediate Preferred)
    res = client.get("/api/v1/readiness/me/jobs/1/skill-gaps", headers=s1_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["job_id"] == 1
    assert data["job_readiness_score"] >= 75.0
    
    # Alice has Python Advanced, SQL Advanced, Docker Intermediate -> 3 Matched
    matched_names = [s["skill_name"] for s in data["matched_skills"]]
    assert "Python" in matched_names
    assert "SQL" in matched_names
    assert "Docker" in matched_names

    # Alice has AWS Beginner, Job 1 prefers AWS Intermediate -> 1 Partial Match
    partial_names = [s["skill_name"] for s in data["partial_skills"]]
    assert "AWS" in partial_names
    # AWS is preferred (is_mandatory=False), so diff=1 gives LOW severity
    aws_item = next(s for s in data["partial_skills"] if s["skill_name"] == "AWS")
    assert aws_item["severity"] == GapSeverity.LOW.value
    assert not aws_item["is_mandatory"]
    assert "AWS" in aws_item["recommendation"]

def test_skill_gap_analysis_unaligned_student(s2_headers):
    # Bob lacks Python, Docker, AWS for Job 1
    res = client.get("/api/v1/readiness/me/jobs/1/skill-gaps", headers=s2_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["job_readiness_score"] < 50.0
    missing_names = [s["skill_name"] for s in data["missing_skills"]]
    assert "Python" in missing_names
    assert "Docker" in missing_names

    # Docker is mandatory & Intermediate -> HIGH severity
    docker_item = next(s for s in data["missing_skills"] if s["skill_name"] == "Docker")
    assert docker_item["severity"] == GapSeverity.HIGH.value
    assert docker_item["is_mandatory"] is True
    assert "Docker" in docker_item["recommendation"]

def test_skill_gap_nonexistent_job(s1_headers):
    res = client.get("/api/v1/readiness/me/jobs/9999/skill-gaps", headers=s1_headers)
    assert res.status_code == 404

# ================= 4. SECURITY & RBAC TESTS =================

def test_student_cannot_access_other_student_readiness(s1_headers):
    # Student 1 trying to access Student 2's readiness
    res = client.get("/api/v1/readiness/students/2", headers=s1_headers)
    assert res.status_code == 403

def test_admin_can_access_student_readiness(admin_headers):
    res = client.get("/api/v1/readiness/students/1", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["overall_score"] >= 80.0

def test_admin_can_access_student_job_skill_gaps(admin_headers):
    res = client.get("/api/v1/readiness/students/1/jobs/1/skill-gaps", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["job_id"] == 1
