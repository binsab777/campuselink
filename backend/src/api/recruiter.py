from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
import datetime

from src.core.database import get_db
from src.api.dependencies import get_current_user, require_role
from src.models.all_models import (
    User, Recruiter, Company, Job, JobRequirement, 
    PlacementDrive, DriveCandidate, Skill, Student, Application
)
from src.models.enums import UserRole, JobStatus, DriveStatus, ApplicationStatus
from src.schemas.recruiter import (
    RecruiterProfileOut, CompanyUpdate, CompanyOut,
    JobCreate, JobUpdate, JobOut,
    JobRequirementCreate, JobRequirementOut,
    PlacementDriveCreate, PlacementDriveUpdate, PlacementDriveOut,
    DriveCandidateCreate, DriveCandidateOut,
    EligibilityResponse
)
from src.services.eligibility import check_hard_eligibility

router = APIRouter(prefix="/api/v1/recruiters", tags=["Recruiters"])
jobs_router = APIRouter(prefix="/api/v1/jobs", tags=["Jobs"])
drives_router = APIRouter(prefix="/api/v1/drives", tags=["Drives"])

def get_current_recruiter(user: User = Depends(require_role(UserRole.RECRUITER)), db: Session = Depends(get_db)) -> Recruiter:
    recruiter = db.query(Recruiter).filter(Recruiter.user_id == user.id).first()
    if not recruiter:
        raise HTTPException(status_code=404, detail="Recruiter profile not found")
    return recruiter

# --- COMPANY & RECRUITER ---

@router.get("/me", response_model=RecruiterProfileOut)
def get_recruiter_profile(recruiter: Recruiter = Depends(get_current_recruiter)):
    return recruiter

@router.put("/me/company", response_model=CompanyOut)
def update_company(
    update_data: CompanyUpdate, 
    recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    company = recruiter.company
    for k, v in update_data.model_dump(exclude_unset=True).items():
        setattr(company, k, v)
    db.commit()
    db.refresh(company)
    return company

# --- JOBS ---

@router.get("/me/jobs", response_model=List[JobOut])
def get_recruiter_jobs(recruiter: Recruiter = Depends(get_current_recruiter), db: Session = Depends(get_db)):
    # Jobs for this recruiter's company
    jobs = db.query(Job).filter(Job.company_id == recruiter.company_id).all()
    return jobs

@router.post("/me/jobs", response_model=JobOut)
def create_job(
    job_data: JobCreate,
    recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    job = Job(**job_data.model_dump(), company_id=recruiter.company_id, recruiter_id=recruiter.id)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

@router.get("/me/jobs/{job_id}", response_model=JobOut)
def get_job(job_id: int, recruiter: Recruiter = Depends(get_current_recruiter), db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id, Job.company_id == recruiter.company_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.put("/me/jobs/{job_id}", response_model=JobOut)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id, Job.company_id == recruiter.company_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    update_dict = job_data.model_dump(exclude_unset=True)
    if "status" in update_dict and update_dict["status"] != job.status:
        new_status = update_dict["status"]
        if job.status in ["CLOSED", "CANCELLED"] and new_status == "DRAFT":
            raise HTTPException(status_code=400, detail="Cannot revert a closed or cancelled job to draft.")

    for k, v in update_dict.items():
        setattr(job, k, v)
    db.commit()
    db.refresh(job)
    return job

@router.delete("/me/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, recruiter: Recruiter = Depends(get_current_recruiter), db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id, Job.company_id == recruiter.company_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()

# --- JOB REQUIREMENTS ---

@jobs_router.get("/skills/all")
def get_all_skills(db: Session = Depends(get_db)):
    skills = db.query(Skill).order_by(Skill.name).all()
    return [{"id": s.id, "name": s.name, "category": s.category} for s in skills]

@jobs_router.get("/{job_id}/requirements", response_model=List[JobRequirementOut])
def get_job_requirements(job_id: int, db: Session = Depends(get_db)):
    return db.query(JobRequirement).filter(JobRequirement.job_id == job_id).all()

@jobs_router.post("/{job_id}/requirements", response_model=JobRequirementOut)
def add_job_requirement(
    job_id: int,
    req_data: JobRequirementCreate,
    recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id, Job.company_id == recruiter.company_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Verify skill exists
    skill = db.query(Skill).filter(Skill.id == req_data.skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    # Check for duplicate
    existing = db.query(JobRequirement).filter(JobRequirement.job_id == job_id, JobRequirement.skill_id == req_data.skill_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Requirement for this skill already exists")

    req = JobRequirement(**req_data.model_dump(), job_id=job_id)
    db.add(req)
    db.commit()
    db.refresh(req)
    return req

@jobs_router.delete("/{job_id}/requirements/{req_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_requirement(
    job_id: int, req_id: int,
    recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id, Job.company_id == recruiter.company_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    req = db.query(JobRequirement).filter(JobRequirement.id == req_id, JobRequirement.job_id == job_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Requirement not found")
    
    db.delete(req)
    db.commit()

@jobs_router.post("/{job_id}/eligibility/check", response_model=EligibilityResponse)
def check_eligibility(
    job_id: int,
    student_id: int,
    recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id, Job.company_id == recruiter.company_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    is_eligible, reasons, failed_rules = check_hard_eligibility(db, student_id, job_id)
    return EligibilityResponse(
        eligible=is_eligible,
        reasons=reasons,
        failed_rules=failed_rules
    )

# --- PLACEMENT DRIVES ---

@router.get("/me/drives", response_model=List[PlacementDriveOut])
def get_recruiter_drives(recruiter: Recruiter = Depends(get_current_recruiter), db: Session = Depends(get_db)):
    return db.query(PlacementDrive).filter(PlacementDrive.company_id == recruiter.company_id).all()

@router.post("/me/drives", response_model=PlacementDriveOut)
def create_drive(
    drive_data: PlacementDriveCreate,
    recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    # Verify job belongs to company
    job = db.query(Job).filter(Job.id == drive_data.job_id, Job.company_id == recruiter.company_id).first()
    if not job:
        raise HTTPException(status_code=400, detail="Invalid job ID: Job does not exist or does not belong to your company")
            
    if drive_data.end_time <= drive_data.start_time:
        raise HTTPException(status_code=400, detail="End time must be after start time")

    drive = PlacementDrive(**drive_data.model_dump(), company_id=recruiter.company_id)
    db.add(drive)
    db.commit()
    db.refresh(drive)
    return drive

@router.put("/me/drives/{drive_id}", response_model=PlacementDriveOut)
def update_drive(
    drive_id: int,
    drive_data: PlacementDriveUpdate,
    recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    drive = db.query(PlacementDrive).filter(PlacementDrive.id == drive_id, PlacementDrive.company_id == recruiter.company_id).first()
    if not drive:
        raise HTTPException(status_code=404, detail="Drive not found")
        
    update_dict = drive_data.model_dump(exclude_unset=True)
    if "status" in update_dict and update_dict["status"] != drive.status:
        new_status = update_dict["status"]
        if drive.status in ["COMPLETED", "CANCELLED"] and new_status in ["DRAFT", "PUBLISHED", "REGISTRATION_OPEN"]:
            raise HTTPException(status_code=400, detail="Cannot reopen a completed or cancelled drive.")

    if "job_id" in update_dict and update_dict["job_id"] is not None:
        job = db.query(Job).filter(Job.id == update_dict["job_id"], Job.company_id == recruiter.company_id).first()
        if not job:
            raise HTTPException(status_code=400, detail="Invalid job ID: Job does not exist or does not belong to your company")

    for k, v in update_dict.items():
        setattr(drive, k, v)
        
    if drive.end_time <= drive.start_time:
        raise HTTPException(status_code=400, detail="End time must be after start time")
        
    db.commit()
    db.refresh(drive)
    return drive

# --- CANDIDATES ---

@drives_router.post("/{drive_id}/candidates", response_model=DriveCandidateOut)
def register_candidate(
    drive_id: int,
    candidate_data: DriveCandidateCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # This endpoint can be used by the student to register, or by a recruiter to manually add.
    # We will enforce logic that if a student is calling it, they can only register themselves.
    student = None
    if user.role == UserRole.STUDENT:
        student = db.query(Student).filter(Student.user_id == user.id).first()
        if not student or student.id != candidate_data.student_id:
            raise HTTPException(status_code=403, detail="You can only register yourself")
    elif user.role == UserRole.RECRUITER:
        # Check recruiter owns the drive
        recruiter = db.query(Recruiter).filter(Recruiter.user_id == user.id).first()
        drive = db.query(PlacementDrive).filter(PlacementDrive.id == drive_id, PlacementDrive.company_id == recruiter.company_id).first()
        if not drive:
             raise HTTPException(status_code=403, detail="You don't own this drive")
        student = db.query(Student).filter(Student.id == candidate_data.student_id).first()
    else:
        student = db.query(Student).filter(Student.id == candidate_data.student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    drive = db.query(PlacementDrive).filter(PlacementDrive.id == drive_id).first()
    if not drive:
        raise HTTPException(status_code=404, detail="Drive not found")

    # Date validation
    now = datetime.datetime.now()
    if drive.registration_deadline and now > drive.registration_deadline:
        raise HTTPException(status_code=400, detail="Registration deadline has passed")

    # Duplicate check
    existing = db.query(DriveCandidate).filter(DriveCandidate.drive_id == drive_id, DriveCandidate.student_id == student.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Student already registered for this drive")

    # Eligibility Check
    is_eligible = True
    reasons = []
    if drive.job_id:
        is_eligible, reasons, _ = check_hard_eligibility(db, student.id, drive.job_id)
        if not is_eligible:
            raise HTTPException(status_code=400, detail=f"Ineligible: {', '.join(reasons)}")

    candidate = DriveCandidate(
        drive_id=drive_id,
        student_id=student.id,
        eligibility_status=is_eligible,
        registration_timestamp=now,
        registration_status="REGISTERED"
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate

# --- RECRUITER DASHBOARD METRICS ---

@router.get("/me/dashboard")
def get_recruiter_dashboard_metrics(
    recruiter: Recruiter = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    now = datetime.datetime.now()
    active_jobs = db.query(Job).filter(
        Job.company_id == recruiter.company_id,
        Job.status == JobStatus.PUBLISHED
    ).count()
    
    upcoming_drives = db.query(PlacementDrive).filter(
        PlacementDrive.company_id == recruiter.company_id,
        PlacementDrive.status != DriveStatus.CANCELLED,
        PlacementDrive.date >= now.date()
    ).count()

    drive_ids = [d.id for d in db.query(PlacementDrive.id).filter(PlacementDrive.company_id == recruiter.company_id).all()]
    
    total_candidates = 0
    shortlisted_candidates = 0
    if drive_ids:
        total_candidates = db.query(DriveCandidate).filter(DriveCandidate.drive_id.in_(drive_ids)).count()
        shortlisted_candidates = db.query(DriveCandidate).filter(
            DriveCandidate.drive_id.in_(drive_ids),
            DriveCandidate.shortlist_status == True
        ).count()

    return {
        "active_jobs_count": active_jobs,
        "upcoming_drives_count": upcoming_drives,
        "total_candidates_count": total_candidates,
        "shortlisted_candidates_count": shortlisted_candidates
    }

# --- PUBLIC / STUDENT OPPORTUNITIES DISCOVERY ---

@jobs_router.get("/available")
def get_available_jobs(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    jobs = db.query(Job).filter(Job.status == JobStatus.PUBLISHED).order_by(Job.created_at.desc()).all()
    results = []
    for j in jobs:
        reqs = []
        for r in j.requirements:
            reqs.append({
                "id": r.id,
                "skill_id": r.skill_id,
                "skill_name": r.skill.name if r.skill else f"Skill #{r.skill_id}",
                "required_proficiency": r.required_proficiency,
                "weight": r.weight,
                "is_mandatory": r.is_mandatory,
                "minimum_experience": r.minimum_experience
            })
        results.append({
            "id": j.id,
            "company_id": j.company_id,
            "company_name": j.company.name if j.company else "Unknown Company",
            "title": j.title,
            "description": j.description,
            "employment_type": j.employment_type,
            "location": j.location,
            "remote_type": j.remote_type,
            "salary_range": j.salary_range,
            "openings": j.openings,
            "application_deadline": j.application_deadline.isoformat() if j.application_deadline else None,
            "eligibility_config": j.eligibility_config,
            "status": j.status,
            "requirements": reqs
        })
    return results

@jobs_router.get("/{job_id}/my-eligibility")
def get_my_job_eligibility(
    job_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.STUDENT))
):
    student = db.query(Student).filter(Student.user_id == user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
        
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    is_eligible, reasons, failed_rules = check_hard_eligibility(db, student.id, job_id)
    return {
        "eligible": is_eligible,
        "reasons": reasons,
        "failed_rules": failed_rules,
        "job_id": job_id,
        "job_title": job.title,
        "student_cgpa": student.cgpa,
        "student_backlogs": student.backlogs_current,
        "student_branch": student.branch,
        "student_graduation_year": student.graduation_year
    }

@drives_router.get("/available")
def get_available_drives(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    drives = db.query(PlacementDrive).filter(
        PlacementDrive.status.in_([DriveStatus.PUBLISHED, DriveStatus.REGISTRATION_OPEN, DriveStatus.IN_PROGRESS])
    ).order_by(PlacementDrive.date.asc()).all()
    results = []
    for d in drives:
        results.append({
            "id": d.id,
            "company_id": d.company_id,
            "company_name": d.company.name if d.company else "Unknown Company",
            "job_id": d.job_id,
            "job_title": d.job.title if d.job else None,
            "name": d.name,
            "description": d.description,
            "date": d.date.isoformat() if d.date else None,
            "start_time": d.start_time.isoformat() if d.start_time else None,
            "end_time": d.end_time.isoformat() if d.end_time else None,
            "registration_deadline": d.registration_deadline.isoformat() if d.registration_deadline else None,
            "mode": d.mode,
            "venue": d.venue,
            "capacity": d.capacity,
            "status": d.status,
            "registered_count": len(d.candidates)
        })
    return results

# --- CANDIDATE MANAGEMENT FOR RECRUITERS ---

@drives_router.get("/{drive_id}/candidates")
def get_drive_candidates(
    drive_id: int,
    db: Session = Depends(get_db),
    recruiter: Recruiter = Depends(get_current_recruiter)
):
    drive = db.query(PlacementDrive).filter(
        PlacementDrive.id == drive_id, 
        PlacementDrive.company_id == recruiter.company_id
    ).first()
    if not drive:
        raise HTTPException(status_code=404, detail="Drive not found or access denied")

    candidates = db.query(DriveCandidate).filter(DriveCandidate.drive_id == drive_id).all()
    results = []
    for c in candidates:
        student = c.student
        results.append({
            "id": c.id,
            "drive_id": c.drive_id,
            "student_id": c.student_id,
            "student_name": f"{student.first_name} {student.last_name}" if student else "Unknown",
            "student_identifier": student.student_identifier if student else "—",
            "branch": student.branch if student else "—",
            "cgpa": student.cgpa if student else 0.0,
            "graduation_year": student.graduation_year if student else None,
            "phone": student.phone if student else None,
            "email": student.user.email if student and student.user else None,
            "eligibility_status": c.eligibility_status,
            "registration_status": c.registration_status,
            "shortlist_status": c.shortlist_status,
            "candidate_notes": c.candidate_notes,
            "registration_timestamp": c.registration_timestamp.isoformat() if c.registration_timestamp else None
        })
    return results

@drives_router.patch("/{drive_id}/candidates/{candidate_id}")
def update_drive_candidate(
    drive_id: int,
    candidate_id: int,
    update_data: dict,
    db: Session = Depends(get_db),
    recruiter: Recruiter = Depends(get_current_recruiter)
):
    drive = db.query(PlacementDrive).filter(
        PlacementDrive.id == drive_id, 
        PlacementDrive.company_id == recruiter.company_id
    ).first()
    if not drive:
        raise HTTPException(status_code=404, detail="Drive not found or access denied")

    candidate = db.query(DriveCandidate).filter(
        DriveCandidate.id == candidate_id,
        DriveCandidate.drive_id == drive_id
    ).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate record not found")

    if "shortlist_status" in update_data:
        candidate.shortlist_status = bool(update_data["shortlist_status"])
        if candidate.shortlist_status:
            candidate.registration_status = "SHORTLISTED"
    if "registration_status" in update_data:
        candidate.registration_status = str(update_data["registration_status"])
    if "candidate_notes" in update_data:
        candidate.candidate_notes = update_data["candidate_notes"]

    db.commit()
    db.refresh(candidate)
    return {
        "id": candidate.id,
        "shortlist_status": candidate.shortlist_status,
        "registration_status": candidate.registration_status,
        "candidate_notes": candidate.candidate_notes
    }

@drives_router.post("/{drive_id}/evaluate-eligibility")
def evaluate_drive_candidates_bulk(
    drive_id: int,
    db: Session = Depends(get_db),
    recruiter: Recruiter = Depends(get_current_recruiter)
):
    drive = db.query(PlacementDrive).filter(
        PlacementDrive.id == drive_id, 
        PlacementDrive.company_id == recruiter.company_id
    ).first()
    if not drive:
        raise HTTPException(status_code=404, detail="Drive not found or access denied")

    if not drive.job_id:
        raise HTTPException(status_code=400, detail="Drive has no associated job posting to evaluate against")

    candidates = db.query(DriveCandidate).filter(DriveCandidate.drive_id == drive_id).all()
    eligible_count = 0
    ineligible_count = 0
    failure_breakdown = {}

    for c in candidates:
        is_eligible, reasons, failed_rules = check_hard_eligibility(db, c.student_id, drive.job_id)
        c.eligibility_status = is_eligible
        if is_eligible:
            eligible_count += 1
        else:
            ineligible_count += 1
            for rule in failed_rules:
                failure_breakdown[rule] = failure_breakdown.get(rule, 0) + 1

    db.commit()

    return {
        "drive_id": drive_id,
        "drive_name": drive.name,
        "total_candidates": len(candidates),
        "eligible_count": eligible_count,
        "ineligible_count": ineligible_count,
        "failure_breakdown": failure_breakdown
    }

@router.get("/candidates/{student_id}")
def get_recruiter_candidate_profile(
    student_id: int,
    db: Session = Depends(get_db),
    recruiter: Recruiter = Depends(get_current_recruiter)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Candidate not found")

    skills = [{
        "id": s.id,
        "skill_name": s.skill.name if s.skill else "Skill",
        "proficiency_level": s.proficiency_level,
        "months_experience": s.months_experience
    } for s in student.skills]

    projects = [{
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "technologies": p.technologies,
        "project_url": p.project_url
    } for p in student.projects]

    certifications = [{
        "id": c.id,
        "name": c.name,
        "issuing_org": c.issuing_org,
        "issue_date": c.issue_date.isoformat() if c.issue_date else None,
        "expiry_date": c.expiry_date.isoformat() if c.expiry_date else None,
        "credential_id": c.credential_id
    } for c in student.certifications]

    academic = [{
        "id": a.id,
        "qualification": a.qualification,
        "institution": a.institution,
        "specialization": a.specialization,
        "start_year": a.start_year,
        "end_year": a.end_year,
        "score_type": a.score_type,
        "score_value": a.score_value
    } for a in student.academic_history]

    assessments = [{
        "id": a.id,
        "assessment_type": a.assessment_type,
        "score": a.score,
        "max_score": a.max_score,
        "assessment_date": a.assessment_date.isoformat() if a.assessment_date else None
    } for a in student.assessments]

    return {
        "id": student.id,
        "student_identifier": student.student_identifier,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "branch": student.branch,
        "graduation_year": student.graduation_year,
        "cgpa": student.cgpa,
        "backlogs_current": student.backlogs_current,
        "backlogs_history": student.backlogs_history,
        "phone": student.phone,
        "email": student.user.email if student.user else None,
        "resume_url": student.resume_url,
        "profile_metadata": student.profile_metadata,
        "skills": skills,
        "projects": projects,
        "certifications": certifications,
        "academic_history": academic,
        "assessments": assessments
    }


@jobs_router.post("/{job_id}/apply")
def apply_to_job(
    job_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    if not user.student_profile:
        raise HTTPException(status_code=403, detail="Only students can apply to jobs")
    job = db.query(Job).filter(Job.id == job_id, Job.status == JobStatus.PUBLISHED).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job opening not found or not published")
    
    existing = db.query(Application).filter(
        Application.job_id == job_id,
        Application.student_id == user.student_profile.id
    ).first()
    if existing:
        return {"message": "Already applied to this job", "application_id": existing.id, "status": existing.status}
    
    app_record = Application(
        student_id=user.student_profile.id,
        job_id=job_id,
        status=ApplicationStatus.APPLIED
    )
    db.add(app_record)
    db.commit()
    db.refresh(app_record)
    return {"message": "Application submitted successfully", "application_id": app_record.id, "status": app_record.status}


@drives_router.post("/{drive_id}/withdraw")
def withdraw_drive_registration(
    drive_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    if not user.student_profile:
        raise HTTPException(status_code=403, detail="Only students can withdraw registrations")
    candidate = db.query(DriveCandidate).filter(
        DriveCandidate.drive_id == drive_id,
        DriveCandidate.student_id == user.student_profile.id
    ).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="You are not registered for this drive")
    
    candidate.registration_status = "WITHDRAWN"
    db.commit()
    return {"message": "Registration withdrawn successfully", "drive_id": drive_id}
