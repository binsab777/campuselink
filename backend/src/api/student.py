import os
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.models.all_models import (
    User, Student, StudentAcademicHistory, Skill, StudentSkill, 
    StudentProject, StudentCertification, StudentAssessment,
    DriveCandidate, PlacementDrive
)
from src.models.enums import UserRole
from src.api.dependencies import require_role
from src.schemas.student import (
    StudentUpdate, StudentOut, AcademicHistoryCreate, AcademicHistoryUpdate, AcademicHistoryOut,
    StudentSkillCreate, StudentSkillUpdate, StudentSkillOut,
    StudentProjectCreate, StudentProjectUpdate, StudentProjectOut,
    StudentCertificationCreate, StudentCertificationUpdate, StudentCertificationOut,
    StudentAssessmentOut, ProfileCompletenessOut, StudentProfileResponse
)

router = APIRouter()

def get_current_student(current_user: User = Depends(require_role(UserRole.STUDENT))) -> Student:
    if not current_user.student_profile:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return current_user.student_profile

def calculate_completeness(student: Student) -> ProfileCompletenessOut:
    sections = {
        "Basic Info": bool(student.first_name and student.last_name and student.dob),
        "Contact Info": bool(student.phone),
        "Academics": bool(student.branch and student.graduation_year),
        "Resume": bool(student.resume_url),
        "Skills": len(student.skills) > 0,
        "Projects": len(student.projects) > 0,
    }
    
    if student.profile_metadata:
        pm = student.profile_metadata
        sections["Bio"] = bool(pm.get("bio"))
        sections["LinkedIn"] = bool(pm.get("linkedin_url"))
    else:
        sections["Bio"] = False
        sections["LinkedIn"] = False

    completed = [k for k, v in sections.items() if v]
    missing = [k for k, v in sections.items() if not v]
    percentage = int((len(completed) / len(sections)) * 100)

    return ProfileCompletenessOut(
        percentage=percentage,
        completed_sections=completed,
        missing_sections=missing
    )

# === Profile ===

@router.get("/me", response_model=StudentOut)
def get_profile(student: Student = Depends(get_current_student)):
    return student

@router.put("/me", response_model=StudentOut)
def update_profile(
    student_in: StudentUpdate,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student)
):
    update_data = student_in.model_dump(exclude_unset=True)
    
    if "profile_metadata" in update_data and update_data["profile_metadata"] is not None:
        # Merge dictionaries if exists
        existing_meta = dict(student.profile_metadata or {})
        existing_meta.update(update_data["profile_metadata"])
        update_data["profile_metadata"] = existing_meta

    for field, value in update_data.items():
        setattr(student, field, value)
        
    db.commit()
    db.refresh(student)
    return student

@router.get("/me/completeness", response_model=ProfileCompletenessOut)
def get_completeness(student: Student = Depends(get_current_student)):
    return calculate_completeness(student)

@router.get("/me/full", response_model=StudentProfileResponse)
def get_full_profile(student: Student = Depends(get_current_student)):
    # Map StudentSkill to StudentSkillOut including skill_name
    skills_out = []
    for ss in student.skills:
        skills_out.append(StudentSkillOut(
            id=ss.id,
            skill_id=ss.skill_id,
            skill_name=ss.skill.name,
            proficiency_level=ss.proficiency_level,
            months_experience=ss.months_experience,
            source=ss.source
        ))

    return StudentProfileResponse(
        basic_info=StudentOut.model_validate(student),
        academic_history=[AcademicHistoryOut.model_validate(ah) for ah in student.academic_history],
        skills=skills_out,
        projects=[StudentProjectOut.model_validate(sp) for sp in student.projects],
        certifications=[StudentCertificationOut.model_validate(sc) for sc in student.certifications],
        assessments=[StudentAssessmentOut.model_validate(sa) for sa in student.assessments],
        completeness=calculate_completeness(student)
    )

# === Academic History ===

@router.get("/me/academic", response_model=List[AcademicHistoryOut])
def get_academic_history(student: Student = Depends(get_current_student)):
    return student.academic_history

@router.post("/me/academic", response_model=AcademicHistoryOut)
def add_academic_history(
    hist_in: AcademicHistoryCreate,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student)
):
    new_hist = StudentAcademicHistory(**hist_in.model_dump(), student_id=student.id)
    db.add(new_hist)
    db.commit()
    db.refresh(new_hist)
    return new_hist

@router.put("/me/academic/{hist_id}", response_model=AcademicHistoryOut)
def update_academic_history(
    hist_id: int,
    hist_in: AcademicHistoryUpdate,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student)
):
    hist = db.query(StudentAcademicHistory).filter(
        StudentAcademicHistory.id == hist_id, 
        StudentAcademicHistory.student_id == student.id
    ).first()
    if not hist:
        raise HTTPException(status_code=404, detail="Academic history not found")
        
    update_data = hist_in.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(hist, k, v)
    db.commit()
    db.refresh(hist)
    return hist

@router.delete("/me/academic/{hist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_academic_history(
    hist_id: int,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student)
):
    hist = db.query(StudentAcademicHistory).filter(
        StudentAcademicHistory.id == hist_id, 
        StudentAcademicHistory.student_id == student.id
    ).first()
    if not hist:
        raise HTTPException(status_code=404, detail="Academic history not found")
    db.delete(hist)
    db.commit()
    return None

# === Skills ===

@router.get("/me/skills", response_model=List[StudentSkillOut])
def get_skills(student: Student = Depends(get_current_student)):
    skills_out = []
    for ss in student.skills:
        skills_out.append(StudentSkillOut(
            id=ss.id,
            skill_id=ss.skill_id,
            skill_name=ss.skill.name,
            proficiency_level=ss.proficiency_level,
            months_experience=ss.months_experience,
            source=ss.source
        ))
    return skills_out

@router.post("/me/skills", response_model=StudentSkillOut)
def add_skill(
    skill_in: StudentSkillCreate,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student)
):
    # Find or create skill globally
    skill_name = skill_in.skill_name.strip().upper()
    skill = db.query(Skill).filter(Skill.name == skill_name).first()
    if not skill:
        skill = Skill(name=skill_name, category="GENERAL")
        db.add(skill)
        db.commit()
        db.refresh(skill)
        
    # Check duplicate
    existing = db.query(StudentSkill).filter(
        StudentSkill.student_id == student.id, 
        StudentSkill.skill_id == skill.id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Skill already added")
        
    new_ss = StudentSkill(
        student_id=student.id,
        skill_id=skill.id,
        proficiency_level=skill_in.proficiency_level,
        months_experience=skill_in.months_experience,
        source=skill_in.source
    )
    db.add(new_ss)
    db.commit()
    db.refresh(new_ss)
    
    return StudentSkillOut(
        id=new_ss.id,
        skill_id=new_ss.skill_id,
        skill_name=skill.name,
        proficiency_level=new_ss.proficiency_level,
        months_experience=new_ss.months_experience,
        source=new_ss.source
    )

@router.put("/me/skills/{skill_id}", response_model=StudentSkillOut)
def update_skill(
    skill_id: int,
    skill_in: StudentSkillUpdate,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student)
):
    ss = db.query(StudentSkill).filter(
        StudentSkill.id == skill_id, 
        StudentSkill.student_id == student.id
    ).first()
    if not ss:
        raise HTTPException(status_code=404, detail="Skill not found")
        
    update_data = skill_in.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(ss, k, v)
    db.commit()
    db.refresh(ss)
    
    return StudentSkillOut(
        id=ss.id,
        skill_id=ss.skill_id,
        skill_name=ss.skill.name,
        proficiency_level=ss.proficiency_level,
        months_experience=ss.months_experience,
        source=ss.source
    )

@router.delete("/me/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student)
):
    ss = db.query(StudentSkill).filter(
        StudentSkill.id == skill_id, 
        StudentSkill.student_id == student.id
    ).first()
    if not ss:
        raise HTTPException(status_code=404, detail="Skill not found")
    db.delete(ss)
    db.commit()
    return None

# === Projects ===

@router.get("/me/projects", response_model=List[StudentProjectOut])
def get_projects(student: Student = Depends(get_current_student)):
    return student.projects

@router.post("/me/projects", response_model=StudentProjectOut)
def add_project(
    project_in: StudentProjectCreate,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student)
):
    new_proj = StudentProject(**project_in.model_dump(), student_id=student.id)
    db.add(new_proj)
    db.commit()
    db.refresh(new_proj)
    return new_proj

@router.put("/me/projects/{project_id}", response_model=StudentProjectOut)
def update_project(
    project_id: int,
    project_in: StudentProjectUpdate,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student)
):
    proj = db.query(StudentProject).filter(
        StudentProject.id == project_id, 
        StudentProject.student_id == student.id
    ).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
        
    update_data = project_in.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(proj, k, v)
    db.commit()
    db.refresh(proj)
    return proj

@router.delete("/me/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student)
):
    proj = db.query(StudentProject).filter(
        StudentProject.id == project_id, 
        StudentProject.student_id == student.id
    ).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(proj)
    db.commit()
    return None

# === Certifications ===

@router.get("/me/certifications", response_model=List[StudentCertificationOut])
def get_certifications(student: Student = Depends(get_current_student)):
    return student.certifications

@router.post("/me/certifications", response_model=StudentCertificationOut)
def add_certification(
    cert_in: StudentCertificationCreate,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student)
):
    if cert_in.expiry_date and cert_in.issue_date and cert_in.expiry_date < cert_in.issue_date:
        raise HTTPException(status_code=400, detail="Expiry date cannot be before issue date")
        
    new_cert = StudentCertification(**cert_in.model_dump(), student_id=student.id)
    db.add(new_cert)
    db.commit()
    db.refresh(new_cert)
    return new_cert

@router.put("/me/certifications/{cert_id}", response_model=StudentCertificationOut)
def update_certification(
    cert_id: int,
    cert_in: StudentCertificationUpdate,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student)
):
    cert = db.query(StudentCertification).filter(
        StudentCertification.id == cert_id, 
        StudentCertification.student_id == student.id
    ).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")
        
    update_data = cert_in.model_dump(exclude_unset=True)
    new_issue = update_data.get("issue_date", cert.issue_date)
    new_expiry = update_data.get("expiry_date", cert.expiry_date)
    if new_issue and new_expiry and new_expiry < new_issue:
        raise HTTPException(status_code=400, detail="Expiry date cannot be before issue date")

    for k, v in update_data.items():
        setattr(cert, k, v)
    db.commit()
    db.refresh(cert)
    return cert

@router.delete("/me/certifications/{cert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_certification(
    cert_id: int,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student)
):
    cert = db.query(StudentCertification).filter(
        StudentCertification.id == cert_id, 
        StudentCertification.student_id == student.id
    ).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")
    db.delete(cert)
    db.commit()
    return None

# === Resume ===

import shutil

RESUME_UPLOAD_DIR = "./uploads/resumes"

@router.post("/me/resume")
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student)
):
    if file.content_type not in ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX are allowed.")
        
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    if file_size > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds maximum allowed limit of 5MB.")

    os.makedirs(RESUME_UPLOAD_DIR, exist_ok=True)
    
    file_ext = file.filename.split(".")[-1]
    file_path = f"{RESUME_UPLOAD_DIR}/student_{student.id}_resume.{file_ext}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    student.resume_url = f"/static/resumes/student_{student.id}_resume.{file_ext}"
    db.commit()
    db.refresh(student)
    
    return {"message": "Resume uploaded successfully", "resume_url": student.resume_url}

@router.delete("/me/resume", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student)
):
    if not student.resume_url:
        raise HTTPException(status_code=400, detail="No resume found to delete")
        
    # Attempt physical deletion if possible
    try:
        file_name = student.resume_url.split("/")[-1]
        file_path = f"{RESUME_UPLOAD_DIR}/{file_name}"
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Failed to delete resume file: {e}")
        
    student.resume_url = None
    db.commit()
    return None

@router.get("/me/drives")
def get_my_drives(
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student)
):
    candidates = db.query(DriveCandidate).filter(DriveCandidate.student_id == student.id).all()
    results = []
    for c in candidates:
        drive = c.drive
        if not drive:
            continue
        results.append({
            "candidate_id": c.id,
            "drive_id": drive.id,
            "drive_name": drive.name,
            "company_name": drive.company.name if drive.company else "Unknown Company",
            "job_title": drive.job.title if drive.job else "Placement Drive",
            "date": drive.date.isoformat() if drive.date else None,
            "start_time": drive.start_time.isoformat() if drive.start_time else None,
            "end_time": drive.end_time.isoformat() if drive.end_time else None,
            "mode": drive.mode,
            "venue": drive.venue,
            "drive_status": drive.status,
            "eligibility_status": c.eligibility_status,
            "registration_status": c.registration_status,
            "shortlist_status": c.shortlist_status,
            "registration_timestamp": c.registration_timestamp.isoformat() if c.registration_timestamp else None
        })
    return results
