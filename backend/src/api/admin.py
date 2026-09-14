from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.core.database import get_db
from src.api.dependencies import get_current_user, require_role, require_any_role
from src.models.all_models import (
    User, Student, Recruiter, Company, Skill, StudentSkill,
    JobRequirement, Job, PlacementDrive, DriveCandidate, Application, StudentScore
)
from src.models.enums import UserRole, JobStatus, DriveStatus
from src.services.readiness import calculate_readiness

router = APIRouter(tags=["Administration & Placement Officer Operations"])


# ================= SCHEMAS =================

class UserStatusUpdate(BaseModel):
    is_active: bool

class UserRoleUpdate(BaseModel):
    role: UserRole

class SkillCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class SkillUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class CompanyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    industry: Optional[str] = Field(None, max_length=100)
    size: Optional[str] = Field(None, max_length=50)
    website: Optional[str] = Field(None, max_length=255)
    headquarters: Optional[str] = Field(None, max_length=150)
    description: Optional[str] = Field(None, max_length=2000)


# ================= 1. USER MANAGEMENT =================

@router.get("/api/v1/admin/users")
def list_users(
    query: Optional[str] = None,
    role: Optional[UserRole] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(require_any_role(UserRole.SUPER_ADMIN, UserRole.PLACEMENT_OFFICER)),
    db: Session = Depends(get_db)
):
    q = db.query(User)
    if role:
        q = q.filter(User.role == role)
    if query:
        search = f"%{query.strip().lower()}%"
        q = q.filter(func.lower(User.email).like(search))
    
    total = q.count()
    users = q.order_by(User.created_at.desc()).offset(offset).limit(limit).all()

    result = []
    for u in users:
        item = {
            "id": u.id,
            "email": u.email,
            "role": u.role.value if hasattr(u.role, 'value') else str(u.role),
            "is_active": u.is_active,
            "created_at": u.created_at.isoformat() if u.created_at else None,
            "student_profile": None,
            "recruiter_profile": None,
        }
        if u.student_profile:
            item["student_profile"] = {
                "id": u.student_profile.id,
                "first_name": u.student_profile.first_name,
                "last_name": u.student_profile.last_name,
                "student_identifier": u.student_profile.student_identifier,
                "branch": u.student_profile.branch,
                "cgpa": u.student_profile.cgpa,
            }
        if u.recruiter_profile:
            item["recruiter_profile"] = {
                "id": u.recruiter_profile.id,
                "company_id": u.recruiter_profile.company_id,
                "company_name": u.recruiter_profile.company.name if u.recruiter_profile.company else None,
            }
        result.append(item)

    return {"total": total, "users": result}


@router.patch("/api/v1/admin/users/{user_id}/status")
def toggle_user_status(
    user_id: int,
    payload: UserStatusUpdate,
    current_user: User = Depends(require_any_role(UserRole.SUPER_ADMIN, UserRole.PLACEMENT_OFFICER)),
    db: Session = Depends(get_db)
):
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if target_user.id == current_user.id and not payload.is_active:
        raise HTTPException(status_code=400, detail="Cannot deactivate your own active session")
    
    target_user.is_active = payload.is_active
    db.commit()
    db.refresh(target_user)
    return {"id": target_user.id, "email": target_user.email, "is_active": target_user.is_active}


@router.patch("/api/v1/admin/users/{user_id}/role")
def change_user_role(
    user_id: int,
    payload: UserRoleUpdate,
    current_user: User = Depends(require_role(UserRole.SUPER_ADMIN)),
    db: Session = Depends(get_db)
):
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if target_user.id == current_user.id and payload.role != UserRole.SUPER_ADMIN:
        raise HTTPException(status_code=400, detail="Cannot revoke your own super administrator role")
    
    target_user.role = payload.role
    db.commit()
    db.refresh(target_user)
    return {"id": target_user.id, "email": target_user.email, "role": target_user.role}


# ================= 2. MASTER SKILLS MANAGEMENT =================

@router.get("/api/v1/skills")
def list_master_skills(
    query: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Skill)
    if category:
        q = q.filter(Skill.category == category)
    if query:
        search = f"%{query.strip().lower()}%"
        q = q.filter(func.lower(Skill.name).like(search))
    
    skills = q.order_by(Skill.category.asc(), Skill.name.asc()).all()

    # Aggregate counts
    result = []
    for s in skills:
        student_usage = db.query(StudentSkill).filter(StudentSkill.skill_id == s.id).count()
        job_usage = db.query(JobRequirement).filter(JobRequirement.skill_id == s.id).count()
        result.append({
            "id": s.id,
            "name": s.name,
            "category": s.category,
            "description": s.description,
            "student_count": student_usage,
            "job_count": job_usage
        })
    return result


@router.post("/api/v1/skills")
def create_master_skill(
    payload: SkillCreate,
    current_user: User = Depends(require_any_role(UserRole.SUPER_ADMIN, UserRole.PLACEMENT_OFFICER)),
    db: Session = Depends(get_db)
):
    normalized_name = payload.name.strip()
    existing = db.query(Skill).filter(func.lower(Skill.name) == normalized_name.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Skill '{normalized_name}' already exists in catalog")
    
    skill = Skill(
        name=normalized_name,
        category=payload.category.strip() if payload.category else None,
        description=payload.description.strip() if payload.description else None
    )
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return {"id": skill.id, "name": skill.name, "category": skill.category, "description": skill.description}


@router.put("/api/v1/skills/{skill_id}")
def update_master_skill(
    skill_id: int,
    payload: SkillUpdate,
    current_user: User = Depends(require_any_role(UserRole.SUPER_ADMIN, UserRole.PLACEMENT_OFFICER)),
    db: Session = Depends(get_db)
):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    if payload.name:
        normalized_name = payload.name.strip()
        existing = db.query(Skill).filter(
            func.lower(Skill.name) == normalized_name.lower(),
            Skill.id != skill_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Skill '{normalized_name}' already exists")
        skill.name = normalized_name

    if payload.category is not None:
        skill.category = payload.category.strip() if payload.category else None
    if payload.description is not None:
        skill.description = payload.description.strip() if payload.description else None

    db.commit()
    db.refresh(skill)
    return {"id": skill.id, "name": skill.name, "category": skill.category, "description": skill.description}


@router.delete("/api/v1/skills/{skill_id}")
def delete_master_skill(
    skill_id: int,
    current_user: User = Depends(require_any_role(UserRole.SUPER_ADMIN, UserRole.PLACEMENT_OFFICER)),
    db: Session = Depends(get_db)
):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    student_usage = db.query(StudentSkill).filter(StudentSkill.skill_id == skill_id).count()
    job_usage = db.query(JobRequirement).filter(JobRequirement.skill_id == skill_id).count()

    if student_usage > 0 or job_usage > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete skill '{skill.name}' because it is actively used in {student_usage} student profile(s) and {job_usage} job requirement(s)"
        )

    db.delete(skill)
    db.commit()
    return {"message": f"Skill '{skill.name}' deleted successfully"}


# ================= 3. PLACEMENT OFFICER: STUDENT DIRECTORY =================

@router.get("/api/v1/officer/students")
def list_officer_students(
    query: Optional[str] = None,
    branch: Optional[str] = None,
    graduation_year: Optional[int] = None,
    min_cgpa: Optional[float] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(require_any_role(UserRole.SUPER_ADMIN, UserRole.PLACEMENT_OFFICER)),
    db: Session = Depends(get_db)
):
    q = db.query(Student)
    if branch:
        q = q.filter(Student.branch == branch)
    if graduation_year:
        q = q.filter(Student.graduation_year == graduation_year)
    if min_cgpa is not None:
        q = q.filter(Student.cgpa >= min_cgpa)
    if query:
        search = f"%{query.strip().lower()}%"
        q = q.filter(
            func.lower(Student.first_name).like(search) |
            func.lower(Student.last_name).like(search) |
            func.lower(Student.student_identifier).like(search)
        )

    total = q.count()
    students = q.order_by(Student.cgpa.desc()).offset(offset).limit(limit).all()

    items = []
    for s in students:
        # Check latest readiness score
        score_rec = db.query(StudentScore).filter(
            StudentScore.student_id == s.id,
            StudentScore.score_type == "READINESS"
        ).order_by(StudentScore.calculated_at.desc()).first()
        
        readiness_val = score_rec.score_value if score_rec else None

        items.append({
            "id": s.id,
            "user_id": s.user_id,
            "student_identifier": s.student_identifier,
            "first_name": s.first_name,
            "last_name": s.last_name,
            "branch": s.branch,
            "graduation_year": s.graduation_year,
            "cgpa": s.cgpa,
            "backlogs_current": s.backlogs_current,
            "backlogs_history": s.backlogs_history,
            "phone": s.phone,
            "email": s.user.email if s.user else None,
            "skills_count": len(s.skills) if s.skills else 0,
            "projects_count": len(s.projects) if s.projects else 0,
            "certifications_count": len(s.certifications) if s.certifications else 0,
            "resume_url": s.resume_url,
            "readiness_score": readiness_val
        })

    return {"total": total, "students": items}


@router.get("/api/v1/officer/students/{student_id}")
def get_officer_student_details(
    student_id: int,
    current_user: User = Depends(require_any_role(UserRole.SUPER_ADMIN, UserRole.PLACEMENT_OFFICER)),
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Evaluate readiness
    readiness_data = None
    try:
        readiness_data = calculate_readiness(db, student.id, persist=False)
    except Exception:
        pass

    return {
        "id": student.id,
        "user_id": student.user_id,
        "student_identifier": student.student_identifier,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "branch": student.branch,
        "graduation_year": student.graduation_year,
        "cgpa": student.cgpa,
        "backlogs_current": student.backlogs_current,
        "backlogs_history": student.backlogs_history,
        "phone": student.phone,
        "dob": student.dob.isoformat() if student.dob else None,
        "email": student.user.email if student.user else None,
        "profile_picture_url": student.profile_picture_url,
        "resume_url": student.resume_url,
        "profile_metadata": student.profile_metadata,
        "academic_history": [
            {
                "id": a.id,
                "qualification": a.qualification,
                "institution": a.institution,
                "specialization": a.specialization,
                "score_value": a.score_value,
                "score_type": a.score_type,
                "start_year": a.start_year,
                "end_year": a.end_year,
            }
            for a in (student.academic_history or [])
        ],
        "skills": [
            {
                "id": sk.id,
                "skill_id": sk.skill_id,
                "name": sk.skill.name if sk.skill else "",
                "category": sk.skill.category if sk.skill else "",
                "proficiency_level": sk.proficiency_level,
                "months_experience": sk.months_experience,
            }
            for sk in (student.skills or [])
        ],
        "projects": [
            {
                "id": p.id,
                "title": p.title,
                "description": p.description,
                "technologies": p.technologies,
                "project_url": p.project_url,
            }
            for p in (student.projects or [])
        ],
        "certifications": [
            {
                "id": c.id,
                "name": c.name,
                "issuing_org": c.issuing_org,
                "issue_date": c.issue_date.isoformat() if c.issue_date else None,
                "credential_id": c.credential_id,
            }
            for c in (student.certifications or [])
        ],
        "readiness": readiness_data
    }


# ================= 4. PLACEMENT OFFICER: CORPORATE PARTNERS =================

@router.get("/api/v1/officer/companies")
def list_officer_companies(
    query: Optional[str] = None,
    industry: Optional[str] = None,
    current_user: User = Depends(require_any_role(UserRole.SUPER_ADMIN, UserRole.PLACEMENT_OFFICER)),
    db: Session = Depends(get_db)
):
    q = db.query(Company)
    if industry:
        q = q.filter(Company.industry == industry)
    if query:
        search = f"%{query.strip().lower()}%"
        q = q.filter(func.lower(Company.name).like(search))
    
    companies = q.order_by(Company.name.asc()).all()

    result = []
    for c in companies:
        recruiters = [
            {
                "id": r.id,
                "contact_name": r.contact_name,
                "contact_email": r.contact_email,
                "contact_phone": r.contact_phone,
            }
            for r in (c.recruiters or [])
        ]
        active_jobs = db.query(Job).filter(Job.company_id == c.id, Job.status == JobStatus.PUBLISHED).count()
        drives_count = db.query(PlacementDrive).filter(PlacementDrive.company_id == c.id).count()

        result.append({
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "industry": c.industry,
            "size": c.size,
            "website": c.website,
            "headquarters": c.headquarters,
            "recruiters_count": len(recruiters),
            "recruiters": recruiters,
            "active_jobs_count": active_jobs,
            "drives_count": drives_count,
        })

    return result


@router.post("/api/v1/officer/companies")
def create_officer_company(
    payload: CompanyCreate,
    current_user: User = Depends(require_any_role(UserRole.SUPER_ADMIN, UserRole.PLACEMENT_OFFICER)),
    db: Session = Depends(get_db)
):
    normalized_name = payload.name.strip()
    existing = db.query(Company).filter(func.lower(Company.name) == normalized_name.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Company '{normalized_name}' is already registered")

    company = Company(
        name=normalized_name,
        industry=payload.industry.strip() if payload.industry else None,
        size=payload.size.strip() if payload.size else None,
        website=payload.website.strip() if payload.website else None,
        headquarters=payload.headquarters.strip() if payload.headquarters else None,
        description=payload.description.strip() if payload.description else None,
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company
