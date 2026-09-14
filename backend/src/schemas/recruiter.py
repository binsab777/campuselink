from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from src.models.enums import JobStatus, DriveStatus, ProficiencyLevel

# --- COMPANY & RECRUITER ---

class CompanyBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    description: Optional[str] = Field(None, max_length=2000)
    industry: Optional[str] = Field(None, max_length=100)
    website: Optional[str] = None
    size: Optional[str] = Field(None, max_length=50)
    headquarters: Optional[str] = Field(None, max_length=150)
    logo_url: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None

    @field_validator("website")
    @classmethod
    def validate_website(cls, v: Optional[str]) -> Optional[str]:
        if not v or not v.strip():
            return None
        v = v.strip()
        if not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError("Website URL must start with http:// or https://")
        return v

class CompanyUpdate(CompanyBase):
    pass

class CompanyOut(CompanyBase):
    id: int
    class Config:
        from_attributes = True

class RecruiterProfileOut(BaseModel):
    id: int
    user_id: int
    company_id: int
    contact_name: Optional[str]
    contact_email: str
    contact_phone: Optional[str]
    company: CompanyOut

    class Config:
        from_attributes = True

# --- JOB ---

class JobRequirementBase(BaseModel):
    skill_id: int = Field(..., gt=0)
    required_proficiency: ProficiencyLevel
    weight: float = Field(1.0, ge=0.1, le=10.0)
    is_mandatory: bool = True
    minimum_experience: int = Field(0, ge=0)
    notes: Optional[str] = Field(None, max_length=500)

class JobRequirementCreate(JobRequirementBase):
    pass

class JobRequirementOut(JobRequirementBase):
    id: int
    job_id: int
    class Config:
        from_attributes = True

def _validate_eligibility_dict(v: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if v is not None:
        min_cgpa = v.get("min_cgpa")
        if min_cgpa is not None:
            if not isinstance(min_cgpa, (int, float)) or min_cgpa < 0.0 or min_cgpa > 10.0:
                raise ValueError("Eligibility min_cgpa must be between 0.0 and 10.0.")
        max_backlogs = v.get("max_backlogs")
        if max_backlogs is not None:
            if not isinstance(max_backlogs, int) or max_backlogs < 0:
                raise ValueError("Eligibility max_backlogs must be a non-negative integer.")
        grad_year = v.get("graduation_year")
        if grad_year is not None:
            if not isinstance(grad_year, int) or grad_year < 2000 or grad_year > 2100:
                raise ValueError("Eligibility graduation_year must be a valid academic year between 2000 and 2100.")
    return v

def _validate_deadline(v: Optional[datetime]) -> Optional[datetime]:
    if v is not None:
        now = datetime.now()
        check_v = v.replace(tzinfo=None) if v.tzinfo else v
        if check_v <= now:
            raise ValueError("Application deadline must be in the future.")
    return v

class JobBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    description: str = Field(..., min_length=10, max_length=5000)
    employment_type: str = Field(..., min_length=2, max_length=50)
    location: Optional[str] = Field(None, max_length=100)
    remote_type: Optional[str] = Field(None, max_length=50)
    salary_range: Optional[str] = Field(None, max_length=100)
    experience_requirement: Optional[str] = Field(None, max_length=100)
    application_deadline: Optional[datetime] = None
    openings: Optional[int] = Field(None, gt=0)
    job_code: Optional[str] = Field(None, max_length=50)
    job_description_json: Optional[Dict[str, Any]] = None
    eligibility_config: Optional[Dict[str, Any]] = None
    status: JobStatus = JobStatus.DRAFT

    @field_validator("application_deadline")
    @classmethod
    def validate_deadline(cls, v: Optional[datetime]) -> Optional[datetime]:
        return _validate_deadline(v)

    @field_validator("eligibility_config")
    @classmethod
    def validate_eligibility(cls, v: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        return _validate_eligibility_dict(v)

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=150)
    description: Optional[str] = Field(None, min_length=10, max_length=5000)
    employment_type: Optional[str] = Field(None, min_length=2, max_length=50)
    location: Optional[str] = Field(None, max_length=100)
    remote_type: Optional[str] = Field(None, max_length=50)
    salary_range: Optional[str] = Field(None, max_length=100)
    experience_requirement: Optional[str] = Field(None, max_length=100)
    application_deadline: Optional[datetime] = None
    openings: Optional[int] = Field(None, gt=0)
    job_code: Optional[str] = Field(None, max_length=50)
    job_description_json: Optional[Dict[str, Any]] = None
    eligibility_config: Optional[Dict[str, Any]] = None
    status: Optional[JobStatus] = None

    @field_validator("application_deadline")
    @classmethod
    def validate_deadline(cls, v: Optional[datetime]) -> Optional[datetime]:
        return _validate_deadline(v)

    @field_validator("eligibility_config")
    @classmethod
    def validate_eligibility(cls, v: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        return _validate_eligibility_dict(v)

class JobOut(JobBase):
    id: int
    company_id: int
    recruiter_id: Optional[int]
    requirements: List[JobRequirementOut] = []
    
    class Config:
        from_attributes = True

# --- PLACEMENT DRIVE ---

class PlacementDriveBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=150)
    description: Optional[str] = Field(None, max_length=2000)
    job_id: int = Field(..., gt=0)
    date: datetime
    registration_start: Optional[datetime] = None
    registration_deadline: Optional[datetime] = None
    start_time: datetime
    end_time: datetime
    mode: Optional[str] = Field(None, max_length=50)
    venue: Optional[str] = Field(None, max_length=200)
    capacity: Optional[int] = Field(None, gt=0)
    coordinator_info: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = Field(None, max_length=1000)
    status: DriveStatus = DriveStatus.DRAFT

    @model_validator(mode="after")
    def validate_drive_schedule(self):
        st = self.start_time.replace(tzinfo=None) if self.start_time.tzinfo else self.start_time
        et = self.end_time.replace(tzinfo=None) if self.end_time.tzinfo else self.end_time
        
        if et <= st:
            raise ValueError("Drive end time must be strictly after start time.")
        
        if self.registration_deadline is not None:
            rd = self.registration_deadline.replace(tzinfo=None) if self.registration_deadline.tzinfo else self.registration_deadline
            if rd >= st:
                raise ValueError("Registration deadline must be before drive start time.")
            if self.registration_start is not None:
                rs = self.registration_start.replace(tzinfo=None) if self.registration_start.tzinfo else self.registration_start
                if rd < rs:
                    raise ValueError("Registration deadline cannot be earlier than registration start.")
        return self

class PlacementDriveCreate(PlacementDriveBase):
    pass

class PlacementDriveUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=150)
    description: Optional[str] = Field(None, max_length=2000)
    job_id: Optional[int] = Field(None, gt=0)
    date: Optional[datetime] = None
    registration_start: Optional[datetime] = None
    registration_deadline: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    mode: Optional[str] = Field(None, max_length=50)
    venue: Optional[str] = Field(None, max_length=200)
    capacity: Optional[int] = Field(None, gt=0)
    coordinator_info: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = Field(None, max_length=1000)
    status: Optional[DriveStatus] = None

    @model_validator(mode="after")
    def validate_update_schedule(self):
        if self.start_time is not None and self.end_time is not None:
            st = self.start_time.replace(tzinfo=None) if self.start_time.tzinfo else self.start_time
            et = self.end_time.replace(tzinfo=None) if self.end_time.tzinfo else self.end_time
            if et <= st:
                raise ValueError("Drive end time must be strictly after start time.")
        
        if self.start_time is not None and self.registration_deadline is not None:
            st = self.start_time.replace(tzinfo=None) if self.start_time.tzinfo else self.start_time
            rd = self.registration_deadline.replace(tzinfo=None) if self.registration_deadline.tzinfo else self.registration_deadline
            if rd >= st:
                raise ValueError("Registration deadline must be before drive start time.")
                
        if self.registration_start is not None and self.registration_deadline is not None:
            rs = self.registration_start.replace(tzinfo=None) if self.registration_start.tzinfo else self.registration_start
            rd = self.registration_deadline.replace(tzinfo=None) if self.registration_deadline.tzinfo else self.registration_deadline
            if rd < rs:
                raise ValueError("Registration deadline cannot be earlier than registration start.")
        return self

class PlacementDriveOut(PlacementDriveBase):
    id: int
    company_id: int
    class Config:
        from_attributes = True

# --- CANDIDATE ---

class DriveCandidateBase(BaseModel):
    student_id: int

class DriveCandidateCreate(DriveCandidateBase):
    pass

class DriveCandidateOut(DriveCandidateBase):
    id: int
    drive_id: int
    eligibility_status: bool
    registration_status: str
    registration_timestamp: Optional[datetime]
    shortlist_status: bool
    candidate_notes: Optional[str]
    
    class Config:
        from_attributes = True

# --- ELIGIBILITY ---

class EligibilityResponse(BaseModel):
    eligible: bool
    reasons: List[str]
    failed_rules: List[str]
