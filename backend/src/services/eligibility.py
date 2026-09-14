from sqlalchemy.orm import Session
from src.models.all_models import Student, Job
from typing import Dict, Any, List, Tuple

def check_hard_eligibility(db: Session, student_id: int, job_id: int) -> Tuple[bool, List[str], List[str]]:
    """
    Evaluates deterministic hard eligibility rules for a student against a job.
    Returns: (is_eligible, reasons, failed_rules)
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    job = db.query(Job).filter(Job.id == job_id).first()

    if not student or not job:
        return False, ["Student or Job not found."], ["not_found"]

    eligibility_config = job.eligibility_config or {}
    
    is_eligible = True
    reasons = []
    failed_rules = []

    # Check CGPA
    min_cgpa = eligibility_config.get("min_cgpa")
    if min_cgpa is not None:
        if student.cgpa is None:
            is_eligible = False
            reasons.append(f"Student CGPA is missing (Minimum required: {min_cgpa}).")
            failed_rules.append("cgpa_missing")
        elif student.cgpa < min_cgpa:
            is_eligible = False
            reasons.append(f"CGPA {student.cgpa} is below the required minimum of {min_cgpa}.")
            failed_rules.append("cgpa_below_minimum")

    # Check allowed branches
    allowed_branches = eligibility_config.get("allowed_branches")
    if allowed_branches:
        # assume branches are listed in a string or list
        if not student.branch:
            is_eligible = False
            reasons.append("Student branch is missing.")
            failed_rules.append("branch_missing")
        elif student.branch not in allowed_branches:
            is_eligible = False
            reasons.append(f"Branch '{student.branch}' is not eligible. Allowed: {', '.join(allowed_branches)}.")
            failed_rules.append("branch_not_allowed")

    # Check backlogs
    max_backlogs = eligibility_config.get("max_backlogs")
    if max_backlogs is not None:
        # If student has backlogs stored in profile_metadata
        # For simplicity, if not stored, assume 0
        student_backlogs = 0
        if student.profile_metadata and "active_backlogs" in student.profile_metadata:
            student_backlogs = student.profile_metadata.get("active_backlogs", 0)
        
        if student_backlogs > max_backlogs:
            is_eligible = False
            reasons.append(f"Active backlogs ({student_backlogs}) exceed maximum allowed ({max_backlogs}).")
            failed_rules.append("backlogs_exceeded")

    # Check graduation year
    req_grad_year = eligibility_config.get("graduation_year")
    if req_grad_year is not None:
        if student.graduation_year != req_grad_year:
            is_eligible = False
            reasons.append(f"Graduation year {student.graduation_year} does not match required {req_grad_year}.")
            failed_rules.append("graduation_year_mismatch")

    if is_eligible:
        reasons.append("Student meets all hard eligibility criteria.")

    return is_eligible, reasons, failed_rules
