import datetime
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session
from src.models.all_models import (
    Student, StudentSkill, StudentProject, StudentCertification, 
    StudentAssessment, StudentScore
)
from src.models.enums import ReadinessLevel, ProficiencyLevel

READINESS_CONFIG_V1 = {
    "version": "v1.0",
    "weights": {
        "academic": 0.20,
        "technical": 0.30,
        "projects": 0.15,
        "certifications": 0.10,
        "assessments": 0.10,
        "communication": 0.10,
        "interview": 0.05
    },
    "level_thresholds": {
        ReadinessLevel.HIGHLY_EMPLOYABLE: 80.0,
        ReadinessLevel.READY: 60.0,
        ReadinessLevel.DEVELOPING: 40.0,
        ReadinessLevel.NOT_READY: 0.0
    }
}

PROFICIENCY_SCORES = {
    ProficiencyLevel.BEGINNER: 25.0,
    ProficiencyLevel.INTERMEDIATE: 50.0,
    ProficiencyLevel.ADVANCED: 75.0,
    ProficiencyLevel.EXPERT: 100.0,
}

def determine_readiness_level(score: float, thresholds: Dict[ReadinessLevel, float]) -> ReadinessLevel:
    if score >= thresholds[ReadinessLevel.HIGHLY_EMPLOYABLE]:
        return ReadinessLevel.HIGHLY_EMPLOYABLE
    elif score >= thresholds[ReadinessLevel.READY]:
        return ReadinessLevel.READY
    elif score >= thresholds[ReadinessLevel.DEVELOPING]:
        return ReadinessLevel.DEVELOPING
    else:
        return ReadinessLevel.NOT_READY

def normalize_academic(student: Student) -> Tuple[float, List[str], List[str]]:
    strengths, weaknesses = [], []
    if student.cgpa is None:
        weaknesses.append("Academic CGPA record is missing.")
        return 0.0, strengths, weaknesses
    
    # Base CGPA score (0-100)
    base = min(100.0, max(0.0, (student.cgpa / 10.0) * 100.0))
    
    # Backlog penalties
    active_backlogs = student.backlogs_current or 0
    hist_backlogs = student.backlogs_history or 0
    if student.profile_metadata:
        active_backlogs = student.profile_metadata.get("active_backlogs", active_backlogs)
        hist_backlogs = student.profile_metadata.get("backlogs_history", hist_backlogs)
        
    penalty = (active_backlogs * 15.0) + (hist_backlogs * 5.0)
    final_score = max(0.0, min(100.0, base - penalty))
    
    if student.cgpa >= 8.5 and active_backlogs == 0:
        strengths.append(f"Outstanding academic record (CGPA {student.cgpa:.2f}) with zero backlogs.")
    elif student.cgpa >= 7.5 and active_backlogs == 0:
        strengths.append(f"Consistent academic performance (CGPA {student.cgpa:.2f}) with clear record.")
        
    if active_backlogs > 0:
        weaknesses.append(f"{active_backlogs} active backlog(s) negatively impact placement eligibility.")
    if student.cgpa < 6.5:
        weaknesses.append(f"CGPA {student.cgpa:.2f} is below standard competitive placement thresholds.")
        
    return final_score, strengths, weaknesses

def normalize_technical_skills(student: Student) -> Tuple[float, List[str], List[str]]:
    strengths, weaknesses = [], []
    tech_skills = [
        s for s in student.skills 
        if not (s.skill and s.skill.category == "Soft Skill")
    ]
    
    if not tech_skills:
        weaknesses.append("No technical skills registered on profile.")
        return 0.0, strengths, weaknesses
        
    skill_scores = []
    for ss in tech_skills:
        score = PROFICIENCY_SCORES.get(ss.proficiency_level, 25.0)
        # Bonus for verified or assessment source
        if ss.source and ss.source.value in ["ASSESSMENT", "CERTIFICATION", "VERIFIED"]:
            score = min(100.0, score + 10.0)
        skill_scores.append(score)
        
    avg_score = sum(skill_scores) / len(skill_scores)
    # Breadth factor: 1 skill -> 0.6, 2 -> 0.75, 3 -> 0.9, 4+ -> 1.0
    breadth = min(1.0, 0.45 + (0.15 * len(tech_skills)))
    final_score = max(0.0, min(100.0, avg_score * breadth))
    
    advanced_skills = [s.skill.name for s in tech_skills if s.skill and s.proficiency_level in [ProficiencyLevel.ADVANCED, ProficiencyLevel.EXPERT]]
    if advanced_skills:
        strengths.append(f"Advanced proficiency demonstrated in: {', '.join(advanced_skills[:3])}.")
    if len(tech_skills) >= 4:
        strengths.append(f"Solid technical skill breadth with {len(tech_skills)} skills registered.")
    elif len(tech_skills) <= 2:
        weaknesses.append(f"Limited technical skill breadth (only {len(tech_skills)} registered).")
        
    return final_score, strengths, weaknesses

def normalize_projects(student: Student) -> Tuple[float, List[str], List[str]]:
    strengths, weaknesses = [], []
    projects = student.projects or []
    if not projects:
        weaknesses.append("No technical projects listed. Practical implementation evidence is critical.")
        return 0.0, strengths, weaknesses
        
    score_acc = 0.0
    for p in projects:
        p_val = 20.0 # base existence
        if p.description and len(p.description.strip()) > 20:
            p_val += 7.0
        if p.technologies:
            p_val += 5.0
        if p.project_url:
            p_val += 5.0
        score_acc += p_val
        
    final_score = max(0.0, min(100.0, score_acc))
    if len(projects) >= 2 and final_score >= 70.0:
        strengths.append(f"Demonstrated practical software development across {len(projects)} projects.")
    elif len(projects) == 1:
        weaknesses.append("Only 1 project documented; adding diverse domain projects will improve portfolio strength.")
        
    return final_score, strengths, weaknesses

def normalize_certifications(student: Student) -> Tuple[float, List[str], List[str]]:
    strengths, weaknesses = [], []
    certs = student.certifications or []
    if not certs:
        weaknesses.append("No professional certifications added to profile.")
        return 0.0, strengths, weaknesses
        
    score_acc = 0.0
    for c in certs:
        c_val = 50.0
        if c.issuing_org:
            c_val += 15.0
        if c.credential_id:
            c_val += 15.0
        score_acc += c_val
        
    final_score = max(0.0, min(100.0, score_acc / len(certs) if len(certs) == 1 else min(100.0, 50.0 + 25.0 * len(certs))))
    strengths.append(f"{len(certs)} industry certification(s) verifying specialized knowledge.")
    return final_score, strengths, weaknesses

def normalize_assessments(student: Student) -> Tuple[Optional[float], List[str], List[str]]:
    strengths, weaknesses = [], []
    assessments = [
        a for a in (student.assessments or [])
        if any(k in a.assessment_type.lower() for k in ["coding", "technical", "aptitude", "cognitive", "quant"])
    ]
    
    if not assessments:
        return None, strengths, weaknesses
        
    pct_scores = [(a.score / a.max_score) * 100.0 for a in assessments if a.max_score > 0]
    if not pct_scores:
        return None, strengths, weaknesses
        
    avg_score = max(0.0, min(100.0, sum(pct_scores) / len(pct_scores)))
    if avg_score >= 75.0:
        strengths.append(f"Strong performance in standardized technical/aptitude assessments ({avg_score:.1f}%).")
    elif avg_score < 50.0:
        weaknesses.append(f"Assessment average ({avg_score:.1f}%) is below expected placement benchmarks.")
        
    return avg_score, strengths, weaknesses

def normalize_communication(student: Student) -> Tuple[Optional[float], List[str], List[str]]:
    strengths, weaknesses = [], []
    # 1. Check assessments
    comm_assessments = [
        a for a in (student.assessments or [])
        if any(k in a.assessment_type.lower() for k in ["communication", "soft skill", "verbal", "english"])
    ]
    if comm_assessments:
        pct_scores = [(a.score / a.max_score) * 100.0 for a in comm_assessments if a.max_score > 0]
        if pct_scores:
            avg_score = max(0.0, min(100.0, sum(pct_scores) / len(pct_scores)))
            if avg_score >= 75.0:
                strengths.append("High verbal and communication assessment scores.")
            return avg_score, strengths, weaknesses

    # 2. Check student soft skills
    soft_skills = [
        s for s in (student.skills or [])
        if s.skill and (s.skill.category == "Soft Skill" or "communication" in s.skill.name.lower())
    ]
    if soft_skills:
        best_level = max(PROFICIENCY_SCORES.get(s.proficiency_level, 25.0) for s in soft_skills)
        return best_level, strengths, weaknesses
        
    return None, strengths, weaknesses

def normalize_interview(student: Student) -> Tuple[Optional[float], List[str], List[str]]:
    strengths, weaknesses = [], []
    interview_assessments = [
        a for a in (student.assessments or [])
        if any(k in a.assessment_type.lower() for k in ["interview", "mock"])
    ]
    if interview_assessments:
        pct_scores = [(a.score / a.max_score) * 100.0 for a in interview_assessments if a.max_score > 0]
        if pct_scores:
            avg_score = max(0.0, min(100.0, sum(pct_scores) / len(pct_scores)))
            if avg_score >= 75.0:
                strengths.append(f"Strong mock interview performance ({avg_score:.1f}%).")
            elif avg_score < 60.0:
                weaknesses.append("Mock interview scores indicate room for communication and problem-solving polish.")
            return avg_score, strengths, weaknesses
            
    if student.profile_metadata and "mock_interview_score" in student.profile_metadata:
        score = float(student.profile_metadata["mock_interview_score"])
        return max(0.0, min(100.0, score)), strengths, weaknesses
        
    return None, strengths, weaknesses

def calculate_readiness(
    db: Session, 
    student_id: int, 
    config: Dict[str, Any] = READINESS_CONFIG_V1, 
    persist: bool = True
) -> Dict[str, Any]:
    """
    Deterministically computes global student readiness score (0-100),
    evaluates strengths/weaknesses, handles missing data via re-weighting,
    and optionally persists the result into student_scores.
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise ValueError(f"Student with ID {student_id} not found.")

    weights = config["weights"]
    thresholds = config["level_thresholds"]

    # Calculate components
    acad_score, acad_str, acad_weak = normalize_academic(student)
    tech_score, tech_str, tech_weak = normalize_technical_skills(student)
    proj_score, proj_str, proj_weak = normalize_projects(student)
    cert_score, cert_str, cert_weak = normalize_certifications(student)
    asmt_score, asmt_str, asmt_weak = normalize_assessments(student)
    comm_score, comm_str, comm_weak = normalize_communication(student)
    intv_score, intv_str, intv_weak = normalize_interview(student)

    raw_components: Dict[str, Optional[float]] = {
        "academic": acad_score,
        "technical": tech_score,
        "projects": proj_score,
        "certifications": cert_score,
        "assessments": asmt_score,
        "communication": comm_score,
        "interview": intv_score
    }

    available_dimensions = []
    missing_dimensions = []
    active_weights = {}

    for dim, score in raw_components.items():
        if score is not None:
            available_dimensions.append(dim)
            active_weights[dim] = weights[dim]
        else:
            missing_dimensions.append(dim)

    # Re-normalize weights across available dimensions
    total_active_weight = sum(active_weights.values())
    if total_active_weight > 0:
        normalized_weights = {
            dim: active_weights[dim] / total_active_weight 
            for dim in active_weights
        }
    else:
        normalized_weights = {}

    # Calculate overall weighted score
    overall_score = 0.0
    final_components: Dict[str, float] = {}
    for dim, score in raw_components.items():
        if score is not None:
            overall_score += score * normalized_weights[dim]
            final_components[dim] = round(score, 1)
        else:
            final_components[dim] = 0.0

    overall_score = round(max(0.0, min(100.0, overall_score)), 1)
    readiness_level = determine_readiness_level(overall_score, thresholds)

    # Aggregate strengths and weaknesses
    all_strengths = acad_str + tech_str + proj_str + cert_str + asmt_str + comm_str + intv_str
    all_weaknesses = acad_weak + tech_weak + proj_weak + cert_weak + asmt_weak + comm_weak + intv_weak

    if missing_dimensions:
        all_weaknesses.append(
            f"Unassessed institutional components ({', '.join(missing_dimensions)}). "
            "Completing institutional tests will provide further verification."
        )

    explanation_data = {
        "overall_score": overall_score,
        "readiness_level": readiness_level.value,
        "components": final_components,
        "configured_weights": weights,
        "effective_weights": {k: round(v, 4) for k, v in normalized_weights.items()},
        "strengths": all_strengths,
        "weaknesses": all_weaknesses,
        "data_quality": {
            "completeness_ratio": round(len(available_dimensions) / len(raw_components), 2),
            "available_dimensions": available_dimensions,
            "missing_dimensions": missing_dimensions,
            "weights_redistributed": len(missing_dimensions) > 0
        },
        "model_version": config["version"],
        "calculated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    if persist:
        # Create a historical record in student_scores
        score_record = StudentScore(
            student_id=student.id,
            score_type="READINESS",
            score_value=overall_score,
            model_version=config["version"],
            explanation_data=explanation_data
        )
        db.add(score_record)
        db.commit()
        db.refresh(score_record)

    return explanation_data
