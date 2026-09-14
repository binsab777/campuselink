from pydantic import BaseModel, HttpUrl, Field, field_validator, model_validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from src.models.enums import ProficiencyLevel, SkillSource

# === Basic Profile ===

class ProfileMetadata(BaseModel):
    bio: Optional[str] = Field(None, max_length=1000)
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    preferred_job_roles: Optional[List[str]] = []
    career_interests: Optional[List[str]] = []

    @field_validator("linkedin_url", "github_url", "portfolio_url")
    @classmethod
    def validate_url(cls, v: Optional[str]) -> Optional[str]:
        if not v or not v.strip():
            return None
        v = v.strip()
        if not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        return v

class StudentUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    branch: Optional[str] = Field(None, min_length=1, max_length=100)
    graduation_year: Optional[int] = Field(None, ge=2000, le=2100)
    cgpa: Optional[float] = Field(None, ge=0.0, le=10.0)
    backlogs_current: Optional[int] = Field(None, ge=0)
    backlogs_history: Optional[int] = Field(None, ge=0)
    phone: Optional[str] = None
    dob: Optional[datetime] = None
    gender: Optional[str] = None
    profile_metadata: Optional[ProfileMetadata] = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if not v or not v.strip():
            return None
        v = v.strip()
        digits = [c for c in v if c.isdigit()]
        if len(digits) < 7 or len(digits) > 15:
            raise ValueError("Phone number must contain between 7 and 15 digits.")
        return v

    @field_validator("dob")
    @classmethod
    def validate_dob(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is not None:
            now = datetime.now()
            check_v = v.replace(tzinfo=None) if v.tzinfo else v
            if check_v > now:
                raise ValueError("Date of birth cannot be in the future.")
            if (now - check_v).days < 15 * 365:
                raise ValueError("Student must be at least 15 years of age.")
        return v

class StudentOut(StudentUpdate):
    id: int
    user_id: int
    student_identifier: str
    resume_url: Optional[str]
    profile_picture_url: Optional[str]

    class Config:
        from_attributes = True

# === Academic History ===

class AcademicHistoryCreate(BaseModel):
    qualification: str = Field(..., min_length=1, max_length=100)
    institution: str = Field(..., min_length=1, max_length=200)
    specialization: Optional[str] = Field(None, max_length=100)
    start_year: Optional[int] = Field(None, ge=1900, le=2100)
    end_year: Optional[int] = Field(None, ge=1900, le=2100)
    score_value: float = Field(..., ge=0.0)
    score_type: str # CGPA or PERCENTAGE

    @model_validator(mode="after")
    def validate_academic_record(self):
        st = (self.score_type or "").upper()
        if st not in ["CGPA", "PERCENTAGE"]:
            raise ValueError("score_type must be either 'CGPA' or 'PERCENTAGE'.")
        if st == "CGPA" and self.score_value > 10.0:
            raise ValueError("CGPA score cannot exceed 10.0.")
        if st == "PERCENTAGE" and self.score_value > 100.0:
            raise ValueError("Percentage score cannot exceed 100.0.")
        if self.start_year and self.end_year and self.end_year < self.start_year:
            raise ValueError("End year cannot precede start year.")
        return self

class AcademicHistoryUpdate(BaseModel):
    qualification: Optional[str] = Field(None, min_length=1, max_length=100)
    institution: Optional[str] = Field(None, min_length=1, max_length=200)
    specialization: Optional[str] = Field(None, max_length=100)
    start_year: Optional[int] = Field(None, ge=1900, le=2100)
    end_year: Optional[int] = Field(None, ge=1900, le=2100)
    score_value: Optional[float] = Field(None, ge=0.0)
    score_type: Optional[str] = None # CGPA or PERCENTAGE

    @model_validator(mode="after")
    def validate_update(self):
        if self.score_type:
            st = self.score_type.upper()
            if st not in ["CGPA", "PERCENTAGE"]:
                raise ValueError("score_type must be either 'CGPA' or 'PERCENTAGE'.")
            if st == "CGPA" and self.score_value is not None and self.score_value > 10.0:
                raise ValueError("CGPA score cannot exceed 10.0.")
            if st == "PERCENTAGE" and self.score_value is not None and self.score_value > 100.0:
                raise ValueError("Percentage score cannot exceed 100.0.")
        elif self.score_value is not None and self.score_value > 100.0:
            raise ValueError("Score value cannot exceed 100.0.")
        if self.start_year and self.end_year and self.end_year < self.start_year:
            raise ValueError("End year cannot precede start year.")
        return self

class AcademicHistoryOut(AcademicHistoryCreate):
    id: int

    class Config:
        from_attributes = True

# === Skills ===

class StudentSkillCreate(BaseModel):
    skill_name: str = Field(..., min_length=1, max_length=100)
    proficiency_level: ProficiencyLevel
    months_experience: Optional[int] = Field(0, ge=0, le=600)
    source: Optional[SkillSource] = SkillSource.STUDENT

class StudentSkillUpdate(BaseModel):
    proficiency_level: Optional[ProficiencyLevel] = None
    months_experience: Optional[int] = Field(None, ge=0, le=600)
    source: Optional[SkillSource] = None

class StudentSkillOut(BaseModel):
    id: int
    skill_id: int
    skill_name: str
    proficiency_level: ProficiencyLevel
    months_experience: int
    source: Optional[SkillSource]

    class Config:
        from_attributes = True

# === Projects ===

class StudentProjectCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=5, max_length=2000)
    technologies: Optional[str] = Field(None, max_length=500)
    project_url: Optional[str] = None

    @field_validator("project_url")
    @classmethod
    def validate_url(cls, v: Optional[str]) -> Optional[str]:
        if not v or not v.strip():
            return None
        v = v.strip()
        if not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError("Project URL must start with http:// or https://")
        return v

class StudentProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=5, max_length=2000)
    technologies: Optional[str] = Field(None, max_length=500)
    project_url: Optional[str] = None

    @field_validator("project_url")
    @classmethod
    def validate_url(cls, v: Optional[str]) -> Optional[str]:
        if not v or not v.strip():
            return None
        v = v.strip()
        if not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError("Project URL must start with http:// or https://")
        return v

class StudentProjectOut(StudentProjectCreate):
    id: int

    class Config:
        from_attributes = True

# === Certifications ===

class StudentCertificationCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    issuing_org: str = Field(..., min_length=1, max_length=200)
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    credential_id: Optional[str] = Field(None, max_length=100)

    @model_validator(mode="after")
    def validate_dates(self):
        now = datetime.now()
        issue = self.issue_date
        expiry = self.expiry_date
        if issue is not None:
            check_issue = issue.replace(tzinfo=None) if issue.tzinfo else issue
            if check_issue > now:
                raise ValueError("Certification issue date cannot be in the future.")
        if issue is not None and expiry is not None:
            check_expiry = expiry.replace(tzinfo=None) if expiry.tzinfo else expiry
            check_issue = issue.replace(tzinfo=None) if issue.tzinfo else issue
            if check_expiry < check_issue:
                raise ValueError("Certification expiry date cannot precede issue date.")
        return self

class StudentCertificationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    issuing_org: Optional[str] = Field(None, min_length=1, max_length=200)
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    credential_id: Optional[str] = Field(None, max_length=100)

    @model_validator(mode="after")
    def validate_dates(self):
        now = datetime.now()
        issue = self.issue_date
        expiry = self.expiry_date
        if issue is not None:
            check_issue = issue.replace(tzinfo=None) if issue.tzinfo else issue
            if check_issue > now:
                raise ValueError("Certification issue date cannot be in the future.")
        if issue is not None and expiry is not None:
            check_expiry = expiry.replace(tzinfo=None) if expiry.tzinfo else expiry
            check_issue = issue.replace(tzinfo=None) if issue.tzinfo else issue
            if check_expiry < check_issue:
                raise ValueError("Certification expiry date cannot precede issue date.")
        return self

class StudentCertificationOut(StudentCertificationCreate):
    id: int

    class Config:
        from_attributes = True

# === Assessments ===

class StudentAssessmentOut(BaseModel):
    id: int
    assessment_type: str
    score: float
    max_score: float
    assessment_date: datetime
    metadata_json: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

# === Profile Completeness ===

class ProfileCompletenessOut(BaseModel):
    percentage: int
    completed_sections: List[str]
    missing_sections: List[str]

# === Comprehensive Profile ===

class StudentProfileResponse(BaseModel):
    basic_info: StudentOut
    academic_history: List[AcademicHistoryOut]
    skills: List[StudentSkillOut]
    projects: List[StudentProjectOut]
    certifications: List[StudentCertificationOut]
    assessments: List[StudentAssessmentOut]
    completeness: ProfileCompletenessOut

