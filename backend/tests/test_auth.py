import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.core.database import Base, get_db
from src.core.security import hash_password
from src.models.all_models import User
from src.models.enums import UserRole
import os
from sqlalchemy.pool import StaticPool

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Create test users
    admin = User(email="admin@test.com", password_hash=hash_password("admin123"), role=UserRole.SUPER_ADMIN, is_active=True)
    student = User(email="student@test.com", password_hash=hash_password("student123"), role=UserRole.STUDENT, is_active=True)
    inactive = User(email="inactive@test.com", password_hash=hash_password("inactive123"), role=UserRole.STUDENT, is_active=False)
    
    db.add_all([admin, student, inactive])
    db.commit()
    yield
    db.close()
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.pop(get_db, None)

def test_login_success():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "student@test.com", "password": "student123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "student@test.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_login_inactive_user():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "inactive@test.com", "password": "inactive123"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Inactive user"

def test_register_student():
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "newstudent@test.com", "password": "newpassword123", "role": "STUDENT"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "newstudent@test.com"
    
def test_register_admin_fails():
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "newadmin@test.com", "password": "admin123", "role": "SUPER_ADMIN"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Cannot register as SUPER_ADMIN"

def test_get_me():
    # Login first
    login_res = client.post(
        "/api/v1/auth/login",
        data={"username": "student@test.com", "password": "student123"}
    )
    token = login_res.json()["access_token"]
    
    # Get me
    me_res = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "student@test.com"

def test_get_me_unauthorized():
    me_res = client.get("/api/v1/auth/me")
    assert me_res.status_code == 401

def test_rbac_admin_endpoint():
    # Login as student
    login_res = client.post(
        '/api/v1/auth/login',
        data={'username': 'student@test.com', 'password': 'student123'}
    )
    token = login_res.json()['access_token']
    
    # Try admin endpoint as student
    res1 = client.get(
        '/api/v1/admin/only',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert res1.status_code == 403
    assert res1.json()['detail'] == 'Not enough permissions'

    # Login as admin
    admin_login = client.post(
        '/api/v1/auth/login',
        data={'username': 'admin@test.com', 'password': 'admin123'}
    )
    admin_token = admin_login.json()['access_token']
    
    # Try admin endpoint as admin
    res2 = client.get(
        '/api/v1/admin/only',
        headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert res2.status_code == 200
    assert res2.json()['message'] == 'Welcome Admin'