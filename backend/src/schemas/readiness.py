from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from src.models.enums import ReadinessLevel, GapSeverity

class ReadinessBreakdownOut(BaseModel):
    overall_score: float
    readiness_level: str
    components: Dict[str, float]
    configured_weights: Dict[str, float]
    effective_weights: Dict[str, float]
    strengths: List[str]
    weaknesses: List[str]
    data_quality: Dict[str, Any]
    model_version: str
    calculated_at: str

class SkillGapItemOut(BaseModel):
    skill_id: int
    skill_name: str
    required_proficiency: str
    student_proficiency: Optional[str] = None
    severity: str
    is_mandatory: bool
    recommendation: str

class JobSkillGapAnalysisOut(BaseModel):
    job_id: int
    job_title: str
    company_id: int
    company_name: Optional[str] = None
    job_readiness_score: float
    global_readiness_score: float
    mandatory_skills_score: float
    preferred_skills_score: float
    total_requirements: int
    matched_count: int
    partial_count: int
    missing_count: int
    matched_skills: List[Dict[str, Any]]
    partial_skills: List[Dict[str, Any]]
    missing_skills: List[Dict[str, Any]]
    gaps: List[Dict[str, Any]]
    analysis_version: str
    analyzed_at: str
