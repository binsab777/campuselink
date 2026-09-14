from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.models.all_models import User, Student, StudentScore, Job
from src.models.enums import UserRole
from src.api.dependencies import get_current_user, require_role, require_any_role
from src.schemas.readiness import ReadinessBreakdownOut, JobSkillGapAnalysisOut
from src.services.readiness import calculate_readiness
from src.services.skill_gap import analyze_skill_gaps

router = APIRouter(prefix="/api/v1/readiness", tags=["Readiness & Skill Gaps"])

def get_current_student(current_user: User = Depends(require_role(UserRole.STUDENT))) -> Student:
    if not current_user.student_profile:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return current_user.student_profile

@router.get("/me", response_model=ReadinessBreakdownOut)
def get_my_readiness(
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student)
):
    """
    Returns the current student's readiness breakdown.
    Fetches the latest persisted score if available, or calculates and persists on-the-fly.
    """
    latest_score = db.query(StudentScore).filter(
        StudentScore.student_id == student.id,
        StudentScore.score_type == "READINESS"
    ).order_by(StudentScore.calculated_at.desc()).first()

    if latest_score and latest_score.explanation_data:
        return latest_score.explanation_data

    # Calculate and persist
    result = calculate_readiness(db, student.id, persist=True)
    return result

@router.post("/me/recalculate", response_model=ReadinessBreakdownOut)
def recalculate_my_readiness(
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student)
):
    """
    Forces recalculation of readiness score and persists a new historical evaluation in student_scores.
    """
    return calculate_readiness(db, student.id, persist=True)

@router.get("/me/jobs/{job_id}/skill-gaps", response_model=JobSkillGapAnalysisOut)
def get_my_job_skill_gaps(
    job_id: int,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student)
):
    """
    Performs deterministic skill gap analysis for the logged-in student against a target job.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail=f"Job with ID {job_id} not found.")

    return analyze_skill_gaps(db, student.id, job_id, persist=True)

@router.post("/me/jobs/{job_id}/skill-gaps/analyze", response_model=JobSkillGapAnalysisOut)
def analyze_my_job_skill_gaps(
    job_id: int,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student)
):
    """
    Forces a fresh skill gap analysis against a target job and updates persisted skill_gaps records.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail=f"Job with ID {job_id} not found.")

    return analyze_skill_gaps(db, student.id, job_id, persist=True)

@router.get("/students/{student_id}", response_model=ReadinessBreakdownOut)
def get_student_readiness_admin(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Allows Placement Officers, Admins, and Recruiters to view any student's readiness.
    Students can only view their own profile.
    """
    if current_user.role == UserRole.STUDENT:
        if not current_user.student_profile or current_user.student_profile.id != student_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden: cannot view other students' readiness")

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found.")

    latest_score = db.query(StudentScore).filter(
        StudentScore.student_id == student.id,
        StudentScore.score_type == "READINESS"
    ).order_by(StudentScore.calculated_at.desc()).first()

    if latest_score and latest_score.explanation_data:
        return latest_score.explanation_data

    return calculate_readiness(db, student.id, persist=True)

@router.get("/students/{student_id}/jobs/{job_id}/skill-gaps", response_model=JobSkillGapAnalysisOut)
def get_student_job_skill_gaps_admin(
    student_id: int,
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Allows Placement Officers, Admins, and Recruiters to inspect skill gap analysis for a student.
    Students can only view their own.
    """
    if current_user.role == UserRole.STUDENT:
        if not current_user.student_profile or current_user.student_profile.id != student_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden: cannot view other students' skill gaps")

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found.")

    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail=f"Job with ID {job_id} not found.")

    return analyze_skill_gaps(db, student.id, job_id, persist=True)
