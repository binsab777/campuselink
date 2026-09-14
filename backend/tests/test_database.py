import sys
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.database import Base
from src.models.all_models import User, Student
from src.models.enums import UserRole

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_create_user(db):
    user = User(email="test@example.com", password_hash="hash", role=UserRole.STUDENT)
    db.add(user)
    db.commit()
    db.refresh(user)
    assert user.id is not None
    assert user.email == "test@example.com"

def test_create_student(db):
    user = User(email="student@example.com", password_hash="hash", role=UserRole.STUDENT)
    db.add(user)
    db.commit()
    db.refresh(user)

    student = Student(
        user_id=user.id,
        student_identifier="ROLL123",
        first_name="John",
        last_name="Doe",
        branch="CSE",
        graduation_year=2026,
        cgpa=8.5
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    
    assert student.id is not None
    assert student.user.email == "student@example.com"

def test_unique_constraint(db):
    user1 = User(email="unique@example.com", password_hash="hash", role=UserRole.STUDENT)
    db.add(user1)
    db.commit()
    
    user2 = User(email="unique@example.com", password_hash="hash", role=UserRole.STUDENT)
    db.add(user2)
    with pytest.raises(Exception):
        db.commit()
