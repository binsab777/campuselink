from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, JSON, Enum, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.core.database import Base
from src.models.enums import UserRole, ApplicationStatus, OfferStatus, ReadinessLevel, ProficiencyLevel, SkillSource, JobStatus, DriveStatus, GapSeverity

class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

# ================= IDENTITY =================

class User(Base, TimestampMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    student_profile = relationship("Student", back_populates="user", uselist=False)
    recruiter_profile = relationship("Recruiter", back_populates="user", uselist=False)

class Student(Base, TimestampMixin):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    student_identifier = Column(String, unique=True, index=True, nullable=False) # e.g., Roll Number
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    branch = Column(String, index=True, nullable=False)
    graduation_year = Column(Integer, index=True, nullable=False)
    cgpa = Column(Float, nullable=False)
    backlogs_current = Column(Integer, default=0, nullable=False)
    backlogs_history = Column(Integer, default=0, nullable=False)
    phone = Column(String, nullable=True)
    dob = Column(DateTime, nullable=True)
    gender = Column(String, nullable=True)
    profile_picture_url = Column(String, nullable=True)
    resume_url = Column(String, nullable=True)
    profile_metadata = Column(JSON, nullable=True)

    __table_args__ = (
        CheckConstraint('cgpa >= 0.0 AND cgpa <= 10.0', name='chk_student_cgpa'),
        CheckConstraint('backlogs_current >= 0', name='chk_student_backlogs_current'),
        CheckConstraint('backlogs_history >= 0', name='chk_student_backlogs_history'),
    )

    user = relationship("User", back_populates="student_profile")
    academic_history = relationship("StudentAcademicHistory", back_populates="student", cascade="all, delete")
    skills = relationship("StudentSkill", back_populates="student", cascade="all, delete")
    projects = relationship("StudentProject", back_populates="student", cascade="all, delete")
    certifications = relationship("StudentCertification", back_populates="student", cascade="all, delete")
    assessments = relationship("StudentAssessment", back_populates="student", cascade="all, delete")
    applications = relationship("Application", back_populates="student")
    scores = relationship("StudentScore", back_populates="student")
    offers = relationship("Offer", back_populates="student")

class StudentAcademicHistory(Base, TimestampMixin):
    __tablename__ = "student_academic_history"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    qualification = Column(String, nullable=False) # e.g., 10th, 12th, Bachelor's
    institution = Column(String, nullable=False)
    specialization = Column(String, nullable=True)
    start_year = Column(Integer, nullable=True)
    end_year = Column(Integer, nullable=True)
    score_value = Column(Float, nullable=False)
    score_type = Column(String, nullable=False) # CGPA or PERCENTAGE
    
    student = relationship("Student", back_populates="academic_history")

class Company(Base, TimestampMixin):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    industry = Column(String, nullable=True)
    website = Column(String, nullable=True)
    size = Column(String, nullable=True)
    headquarters = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    metadata_json = Column(JSON, nullable=True)

    recruiters = relationship("Recruiter", back_populates="company")
    jobs = relationship("Job", back_populates="company")
    drives = relationship("PlacementDrive", back_populates="company")

class Recruiter(Base, TimestampMixin):
    __tablename__ = "recruiters"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    contact_name = Column(String, nullable=True)
    contact_email = Column(String, nullable=False)
    contact_phone = Column(String, nullable=True)

    user = relationship("User", back_populates="recruiter_profile")
    company = relationship("Company", back_populates="recruiters")


# ================= SKILLS =================

class Skill(Base, TimestampMixin):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, index=True, nullable=True)
    description = Column(Text, nullable=True)

class StudentSkill(Base, TimestampMixin):
    __tablename__ = "student_skills"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    proficiency_level = Column(Enum(ProficiencyLevel), nullable=False)
    months_experience = Column(Integer, default=0)
    source = Column(Enum(SkillSource), nullable=True)

    __table_args__ = (
        UniqueConstraint('student_id', 'skill_id', name='uq_student_skill'),
        CheckConstraint('months_experience >= 0', name='chk_student_skill_experience'),
    )

    student = relationship("Student", back_populates="skills")
    skill = relationship("Skill")

class StudentProject(Base, TimestampMixin):
    __tablename__ = "student_projects"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    technologies = Column(String, nullable=True) # Comma separated or JSON
    project_url = Column(String, nullable=True)

    student = relationship("Student", back_populates="projects")

class StudentCertification(Base, TimestampMixin):
    __tablename__ = "student_certifications"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    issuing_org = Column(String, nullable=False)
    issue_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)
    credential_id = Column(String, nullable=True)

    student = relationship("Student", back_populates="certifications")

class StudentAssessment(Base, TimestampMixin):
    __tablename__ = "student_assessments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    assessment_type = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False)
    assessment_date = Column(DateTime, nullable=False)
    metadata_json = Column(JSON, nullable=True)

    student = relationship("Student", back_populates="assessments")


# ================= RECRUITER / JOB =================

class Job(Base, TimestampMixin):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    recruiter_id = Column(Integer, ForeignKey("recruiters.id", ondelete="SET NULL"), nullable=True) # Creator
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    employment_type = Column(String, nullable=False) # e.g., Full-time, Internship
    location = Column(String, nullable=True)
    remote_type = Column(String, nullable=True) # Remote, Hybrid, On-site
    salary_range = Column(String, nullable=True)
    experience_requirement = Column(String, nullable=True)
    application_deadline = Column(DateTime, nullable=True)
    openings = Column(Integer, nullable=True)
    job_code = Column(String, nullable=True)
    job_description_json = Column(JSON, nullable=True)
    eligibility_config = Column(JSON, nullable=True) # E.g., allowed branches, min cgpa
    status = Column(Enum(JobStatus), default=JobStatus.DRAFT, index=True)

    __table_args__ = (
        CheckConstraint('openings IS NULL OR openings > 0', name='chk_job_openings'),
    )

    company = relationship("Company", back_populates="jobs")
    recruiter = relationship("Recruiter")
    requirements = relationship("JobRequirement", back_populates="job")
    applications = relationship("Application", back_populates="job")

class JobRequirement(Base, TimestampMixin):
    __tablename__ = "job_requirements"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    required_proficiency = Column(Enum(ProficiencyLevel), nullable=False)
    weight = Column(Float, default=1.0)
    is_mandatory = Column(Boolean, default=True)
    minimum_experience = Column(Integer, default=0) # months
    notes = Column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint('job_id', 'skill_id', name='uq_job_skill'),
        CheckConstraint('weight >= 0.1 AND weight <= 10.0', name='chk_job_req_weight'),
        CheckConstraint('minimum_experience >= 0', name='chk_job_req_min_exp'),
    )

    job = relationship("Job", back_populates="requirements")
    skill = relationship("Skill")


# ================= PLACEMENT DRIVES =================

class PlacementDrive(Base, TimestampMixin):
    __tablename__ = "placement_drives"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime, index=True, nullable=False)
    registration_start = Column(DateTime, nullable=True)
    registration_deadline = Column(DateTime, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    mode = Column(String, nullable=True) # Online, Offline
    venue = Column(String, nullable=True)
    capacity = Column(Integer, nullable=True)
    coordinator_info = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(Enum(DriveStatus), default=DriveStatus.DRAFT, index=True)

    __table_args__ = (
        CheckConstraint('capacity IS NULL OR capacity > 0', name='chk_drive_capacity'),
    )

    company = relationship("Company", back_populates="drives")
    job = relationship("Job")
    candidates = relationship("DriveCandidate", back_populates="drive")
    schedules = relationship("DriveSchedule", back_populates="drive")

class DriveCandidate(Base, TimestampMixin):
    __tablename__ = "drive_candidates"
    id = Column(Integer, primary_key=True, index=True)
    drive_id = Column(Integer, ForeignKey("placement_drives.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    eligibility_status = Column(Boolean, default=True)
    registration_status = Column(String, default="REGISTERED")
    registration_timestamp = Column(DateTime, nullable=True)
    matching_status = Column(String, nullable=True)
    shortlist_status = Column(Boolean, default=False)
    candidate_notes = Column(Text, nullable=True)

    __table_args__ = (UniqueConstraint('drive_id', 'student_id', name='uq_drive_candidate'),)

    drive = relationship("PlacementDrive", back_populates="candidates")
    student = relationship("Student")

class DriveSchedule(Base, TimestampMixin):
    __tablename__ = "drive_schedules"
    id = Column(Integer, primary_key=True, index=True)
    drive_id = Column(Integer, ForeignKey("placement_drives.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    interviewer_ref = Column(String, nullable=True)
    venue = Column(String, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String, default="SCHEDULED")

    __table_args__ = (UniqueConstraint('drive_id', 'student_id', 'start_time', name='uq_drive_schedule'),)

    drive = relationship("PlacementDrive", back_populates="schedules")
    student = relationship("Student")


# ================= APPLICATIONS =================

class Application(Base, TimestampMixin):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    drive_id = Column(Integer, ForeignKey("placement_drives.id", ondelete="SET NULL"), nullable=True)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.APPLIED, index=True)
    applied_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint('student_id', 'job_id', name='uq_student_job_application'),)

    student = relationship("Student", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    drive = relationship("PlacementDrive")
    interviews = relationship("Interview", back_populates="application")

class Interview(Base, TimestampMixin):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)
    scheduled_start = Column(DateTime, nullable=False)
    scheduled_end = Column(DateTime, nullable=False)
    interview_type = Column(String, nullable=False) # e.g., Technical, HR
    score = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    status = Column(String, default="SCHEDULED")

    application = relationship("Application", back_populates="interviews")


# ================= OFFERS =================

class Offer(Base, TimestampMixin):
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    recruiter_id = Column(Integer, ForeignKey("recruiters.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete="SET NULL"), nullable=True)
    status = Column(Enum(OfferStatus), default=OfferStatus.PENDING, index=True)
    ctc = Column(Float, nullable=False)
    offer_date = Column(DateTime, nullable=False)
    acceptance_date = Column(DateTime, nullable=True)
    joining_date = Column(DateTime, nullable=True)
    deferral_info = Column(Text, nullable=True)

    student = relationship("Student", back_populates="offers")
    recruiter = relationship("Recruiter")
    job = relationship("Job")
    application = relationship("Application")
    documents = relationship("OfferDocument", back_populates="offer")

class OfferDocument(Base, TimestampMixin):
    __tablename__ = "offer_documents"
    id = Column(Integer, primary_key=True, index=True)
    offer_id = Column(Integer, ForeignKey("offers.id", ondelete="CASCADE"), nullable=False)
    document_type = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    verification_status = Column(String, default="PENDING")
    verified_at = Column(DateTime, nullable=True)

    offer = relationship("Offer", back_populates="documents")


# ================= NOTIFICATIONS =================

class Notification(Base, TimestampMixin):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    notification_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    channel = Column(String, default="IN_APP")
    status = Column(String, default="PENDING")
    scheduled_at = Column(DateTime, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)
    metadata_json = Column(JSON, nullable=True)


# ================= AI / SCORING =================

class StudentScore(Base):
    __tablename__ = "student_scores"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    score_type = Column(String, nullable=False) # e.g., READINESS
    score_value = Column(Float, nullable=False)
    model_version = Column(String, nullable=True)
    explanation_data = Column(JSON, nullable=True)
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="scores")

class MatchingScore(Base):
    __tablename__ = "matching_scores"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    drive_id = Column(Integer, ForeignKey("placement_drives.id", ondelete="SET NULL"), nullable=True)
    eligibility_score = Column(Float, nullable=True)
    skill_similarity_score = Column(Float, nullable=True)
    project_relevance_score = Column(Float, nullable=True)
    academic_score = Column(Float, nullable=True)
    interview_score = Column(Float, nullable=True)
    final_score = Column(Float, nullable=False)
    model_version = Column(String, nullable=True)
    explanation_data = Column(JSON, nullable=True)
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint('student_id', 'job_id', 'drive_id', name='uq_match_score'),)

class SkillGap(Base):
    __tablename__ = "skill_gaps"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    gap_severity = Column(String, nullable=False) # NONE, LOW, MEDIUM, HIGH, CRITICAL
    current_level = Column(Integer, nullable=True) # 1=Beginner, 2=Intermediate, 3=Advanced, 4=Expert
    required_level = Column(Integer, nullable=True)
    is_mandatory = Column(Boolean, default=True, nullable=False)
    analysis_version = Column(String, default="v1.0", nullable=False)
    recommendation = Column(Text, nullable=True)
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint('student_id', 'job_id', 'skill_id', name='uq_skill_gap'),)

    student = relationship("Student")
    job = relationship("Job")
    skill = relationship("Skill")


# ================= AUDITING =================

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    entity_type = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=False)
    action = Column(String, nullable=False)
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    request_metadata = Column(JSON, nullable=True)
