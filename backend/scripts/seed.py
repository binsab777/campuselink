import sys
import os
import datetime
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.database import SessionLocal, engine, Base
from src.core.security import hash_password
from src.models.all_models import (
    User, Student, Recruiter, Skill, StudentSkill, Job, JobRequirement,
    PlacementDrive, DriveCandidate, Application, Offer, StudentProject, StudentAssessment
)
from src.models.enums import UserRole, ApplicationStatus, OfferStatus

def seed_db():
    db = SessionLocal()
    
    import sys
    force = "--force" in sys.argv
    # Check if we already seeded
    if not force and db.query(User).first():
        print("Database already seeded")
        return

    if force:
        print("Force re-seeding: clearing existing data...")
        from src.core.database import Base
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()

    # Create Users
    admin = User(email="admin@campuslink.com", password_hash=hash_password("admin123"), role=UserRole.SUPER_ADMIN)
    po = User(email="po@campuslink.com", password_hash=hash_password("po123"), role=UserRole.PLACEMENT_OFFICER)
    
    recruiter_users = [
        User(email=f"recruiter{i}@comp{i}.com", password_hash=hash_password("rec123"), role=UserRole.RECRUITER)
        for i in range(1, 4)
    ]
    
    student_users = [
        User(email=f"student{i}@college.edu", password_hash=hash_password("stu123"), role=UserRole.STUDENT)
        for i in range(1, 11)
    ]

    db.add_all([admin, po] + recruiter_users + student_users)
    db.commit()

    # Create Companies
    from src.models.all_models import Company
    companies = [
        Company(name="TechCorp", description="Leading tech company", industry="Software", website="https://techcorp.com", size="1000-5000"),
        Company(name="Innovate Ltd", description="Startup building innovative products", industry="IT", website="https://innovateltd.com", size="50-200"),
        Company(name="Global Systems", description="Enterprise systems", industry="Consulting", website="https://globalsystems.com", size="10000+")
    ]
    db.add_all(companies)
    db.commit()

    # Create Recruiters
    recruiters = [
        Recruiter(user_id=recruiter_users[0].id, company_id=companies[0].id, contact_name="John Doe", contact_email="recruiter1@comp1.com"),
        Recruiter(user_id=recruiter_users[1].id, company_id=companies[1].id, contact_name="Jane Smith", contact_email="recruiter2@comp2.com"),
        Recruiter(user_id=recruiter_users[2].id, company_id=companies[2].id, contact_name="Robert Brown", contact_email="recruiter3@comp3.com")
    ]
    db.add_all(recruiters)
    db.commit()

    from src.models.enums import ProficiencyLevel, SkillSource
    # Create Students
    # Student A: Strong academics, strong tech, several projects
    student_a = Student(
        user_id=student_users[0].id, 
        student_identifier="STU001",
        first_name="Alice", 
        last_name="Johnson", 
        branch="Computer Science", 
        graduation_year=2024, 
        cgpa=9.2,
        dob=datetime.date(2002, 5, 14),
        phone="555-0101",
        profile_metadata={"bio": "Passionate backend engineer", "github_url": "github.com/alice"}
    )
    
    # Student B: Average academics, good projects
    student_b = Student(
        user_id=student_users[1].id, 
        student_identifier="STU002",
        first_name="Bob", 
        last_name="Smith", 
        branch="Information Technology", 
        graduation_year=2024, 
        cgpa=7.5,
        dob=datetime.date(2001, 8, 22),
        phone="555-0102",
        profile_metadata={"bio": "Frontend enthusiast"}
    )
    
    # Fill remaining students
    students = [student_a, student_b]
    branches = ["CSE", "ECE", "MECH", "IT", "CSE"]
    for i in range(2, 10):
        st = Student(
            user_id=student_users[i].id,
            student_identifier=f"ROLL202600{i}",
            first_name=f"First{i}",
            last_name=f"Last{i}",
            branch=branches[i % len(branches)],
            graduation_year=2026,
            cgpa=7.5 + (i * 0.2) % 2.5
        )
        students.append(st)

    db.add_all(students)
    db.commit()

    # Create Skills
    skills_data = ["Python", "Java", "React", "SQL", "Docker", "AWS", "Communication", "C++", "Machine Learning"]
    skills = [Skill(name=s, category="Technical" if s != "Communication" else "Soft Skill") for s in skills_data]
    db.add_all(skills)
    db.commit()

    # Create Jobs
    jobs = [
        Job(company_id=companies[0].id, recruiter_id=recruiters[0].id, title="Software Engineer", description="Backend Dev", employment_type="Full-time", eligibility_config={"min_cgpa": 8.0, "allowed_branches": ["Computer Science", "CSE", "IT"]}),
        Job(company_id=companies[1].id, recruiter_id=recruiters[1].id, title="Frontend Intern", description="React Dev", employment_type="Internship", eligibility_config={"min_cgpa": 7.0, "allowed_branches": ["Computer Science", "CSE", "IT"]}),
        Job(company_id=companies[2].id, recruiter_id=recruiters[2].id, title="Data Analyst", description="SQL and Python", employment_type="Full-time", eligibility_config={"min_cgpa": 7.5}),
        Job(company_id=companies[0].id, recruiter_id=recruiters[0].id, title="DevOps Engineer", description="Docker and AWS", employment_type="Full-time", eligibility_config={"min_cgpa": 7.5})
    ]
    db.add_all(jobs)
    db.commit()

    # Create Job Requirements
    reqs = [
        # Job 0: Software Engineer
        JobRequirement(job_id=jobs[0].id, skill_id=skills[0].id, required_proficiency=ProficiencyLevel.ADVANCED, weight=2.0, is_mandatory=True), # Python
        JobRequirement(job_id=jobs[0].id, skill_id=skills[3].id, required_proficiency=ProficiencyLevel.INTERMEDIATE, weight=1.5, is_mandatory=True), # SQL
        JobRequirement(job_id=jobs[0].id, skill_id=skills[4].id, required_proficiency=ProficiencyLevel.INTERMEDIATE, weight=1.0, is_mandatory=True), # Docker
        JobRequirement(job_id=jobs[0].id, skill_id=skills[5].id, required_proficiency=ProficiencyLevel.INTERMEDIATE, weight=1.0, is_mandatory=False), # AWS (Preferred)

        # Job 1: Frontend Intern
        JobRequirement(job_id=jobs[1].id, skill_id=skills[2].id, required_proficiency=ProficiencyLevel.INTERMEDIATE, weight=2.0, is_mandatory=True), # React
        JobRequirement(job_id=jobs[1].id, skill_id=skills[6].id, required_proficiency=ProficiencyLevel.INTERMEDIATE, weight=1.0, is_mandatory=True), # Communication

        # Job 2: Data Analyst
        JobRequirement(job_id=jobs[2].id, skill_id=skills[3].id, required_proficiency=ProficiencyLevel.ADVANCED, weight=2.0, is_mandatory=True), # SQL
        JobRequirement(job_id=jobs[2].id, skill_id=skills[0].id, required_proficiency=ProficiencyLevel.INTERMEDIATE, weight=1.5, is_mandatory=True), # Python
        JobRequirement(job_id=jobs[2].id, skill_id=skills[8].id, required_proficiency=ProficiencyLevel.BEGINNER, weight=1.0, is_mandatory=False), # ML (Preferred)

        # Job 3: DevOps Engineer
        JobRequirement(job_id=jobs[3].id, skill_id=skills[4].id, required_proficiency=ProficiencyLevel.ADVANCED, weight=2.0, is_mandatory=True), # Docker
        JobRequirement(job_id=jobs[3].id, skill_id=skills[5].id, required_proficiency=ProficiencyLevel.INTERMEDIATE, weight=2.0, is_mandatory=True), # AWS
        JobRequirement(job_id=jobs[3].id, skill_id=skills[0].id, required_proficiency=ProficiencyLevel.INTERMEDIATE, weight=1.0, is_mandatory=False)  # Python (Preferred)
    ]
    db.add_all(reqs)

    # Student 0 (Alice / student1@college.edu) -> Strong Student Archetype
    from src.models.all_models import StudentAcademicHistory, StudentCertification
    ah1 = StudentAcademicHistory(student_id=student_a.id, qualification="10th", institution="Delhi Public School", start_year=2016, end_year=2018, score_value=95.0, score_type="PERCENTAGE")
    ah2 = StudentAcademicHistory(student_id=student_a.id, qualification="12th", institution="Delhi Public School", start_year=2018, end_year=2020, score_value=92.0, score_type="PERCENTAGE")
    db.add_all([ah1, ah2])

    # Alice Skills
    db.add_all([
        StudentSkill(student_id=student_a.id, skill_id=skills[0].id, proficiency_level=ProficiencyLevel.ADVANCED, months_experience=24, source=SkillSource.VERIFIED), # Python
        StudentSkill(student_id=student_a.id, skill_id=skills[3].id, proficiency_level=ProficiencyLevel.ADVANCED, months_experience=18, source=SkillSource.ASSESSMENT), # SQL
        StudentSkill(student_id=student_a.id, skill_id=skills[2].id, proficiency_level=ProficiencyLevel.INTERMEDIATE, months_experience=12, source=SkillSource.STUDENT), # React
        StudentSkill(student_id=student_a.id, skill_id=skills[4].id, proficiency_level=ProficiencyLevel.INTERMEDIATE, months_experience=8, source=SkillSource.STUDENT), # Docker
        StudentSkill(student_id=student_a.id, skill_id=skills[5].id, proficiency_level=ProficiencyLevel.BEGINNER, months_experience=4, source=SkillSource.STUDENT), # AWS
        StudentSkill(student_id=student_a.id, skill_id=skills[6].id, proficiency_level=ProficiencyLevel.ADVANCED, months_experience=12, source=SkillSource.STUDENT), # Communication
    ])

    # Alice Projects
    db.add_all([
        StudentProject(student_id=student_a.id, title="E-Commerce Microservices", description="Architected resilient microservices with FastAPI, Docker, and PostgreSQL with Redis caching.", technologies="Python, FastAPI, Docker, PostgreSQL, Redis", project_url="https://github.com/alice/ecommerce"),
        StudentProject(student_id=student_a.id, title="Campus Placement Analytics", description="Full-stack Next.js and Python analytics dashboard tracking corporate drive outcomes.", technologies="React, Next.js, Python, TailwindCSS", project_url="https://github.com/alice/campuslink"),
        StudentProject(student_id=student_a.id, title="Distributed Task Queue", description="Lightweight distributed task queue leveraging Python asyncio and message brokers.", technologies="Python, asyncio, RabbitMQ", project_url="https://github.com/alice/task-queue")
    ])

    # Alice Certifications
    db.add_all([
        StudentCertification(student_id=student_a.id, name="AWS Certified Cloud Practitioner", issuing_org="Amazon Web Services", credential_id="AWS-CCP-98721", issue_date=datetime.datetime.now() - datetime.timedelta(days=120)),
        StudentCertification(student_id=student_a.id, name="Professional Python Developer", issuing_org="Python Institute", credential_id="PCAP-31-03", issue_date=datetime.datetime.now() - datetime.timedelta(days=200))
    ])

    # Alice Assessments
    db.add_all([
        StudentAssessment(student_id=student_a.id, assessment_type="Coding Test", score=94.0, max_score=100.0, assessment_date=datetime.datetime.now()),
        StudentAssessment(student_id=student_a.id, assessment_type="Aptitude Test", score=88.0, max_score=100.0, assessment_date=datetime.datetime.now()),
        StudentAssessment(student_id=student_a.id, assessment_type="Communication Assessment", score=86.0, max_score=100.0, assessment_date=datetime.datetime.now()),
        StudentAssessment(student_id=student_a.id, assessment_type="Mock Interview", score=90.0, max_score=100.0, assessment_date=datetime.datetime.now())
    ])

    # Student 1 (Bob / student2@college.edu) -> Developing Archetype
    student_b = students[1]
    db.add_all([
        StudentSkill(student_id=student_b.id, skill_id=skills[1].id, proficiency_level=ProficiencyLevel.BEGINNER, months_experience=6, source=SkillSource.STUDENT), # Java
        StudentSkill(student_id=student_b.id, skill_id=skills[3].id, proficiency_level=ProficiencyLevel.BEGINNER, months_experience=4, source=SkillSource.STUDENT), # SQL
        StudentProject(student_id=student_b.id, title="Library Management System", description="Basic CRUD application managing library books and issuing.", technologies="Java, Swing, SQLite"),
        StudentAssessment(student_id=student_b.id, assessment_type="Coding Test", score=58.0, max_score=100.0, assessment_date=datetime.datetime.now()),
        StudentAssessment(student_id=student_b.id, assessment_type="Aptitude Test", score=62.0, max_score=100.0, assessment_date=datetime.datetime.now())
    ])

    # Remaining students: diverse skills & projects
    for st in students[2:]:
        db.add(StudentSkill(student_id=st.id, skill_id=skills[0].id, proficiency_level=ProficiencyLevel.INTERMEDIATE, source=SkillSource.STUDENT))
        db.add(StudentProject(student_id=st.id, title="Demo Project", description="A great portfolio project"))
        db.add(StudentAssessment(student_id=st.id, assessment_type="Coding Test", score=80.0, max_score=100.0, assessment_date=datetime.datetime.now()))
    db.commit()

    # Placement Drives
    drives = [
        PlacementDrive(company_id=companies[0].id, name="TechCorp Campus Drive 2026", job_id=jobs[0].id, date=datetime.datetime.now() + datetime.timedelta(days=10), start_time=datetime.datetime.now(), end_time=datetime.datetime.now()),
        PlacementDrive(company_id=companies[1].id, name="Innovate Intern Drive", job_id=jobs[1].id, date=datetime.datetime.now() + datetime.timedelta(days=15), start_time=datetime.datetime.now(), end_time=datetime.datetime.now()),
        PlacementDrive(company_id=companies[2].id, name="Global Systems Mega Drive", job_id=jobs[2].id, date=datetime.datetime.now() + datetime.timedelta(days=20), start_time=datetime.datetime.now(), end_time=datetime.datetime.now())
    ]
    db.add_all(drives)
    db.commit()

    # Drive Candidates & Applications
    for st in students[:5]:
        db.add(DriveCandidate(drive_id=drives[0].id, student_id=st.id, eligibility_status=True))
        db.add(Application(student_id=st.id, job_id=jobs[0].id, drive_id=drives[0].id, status=ApplicationStatus.APPLIED))
    
    
    db.commit()

    # Offers
    offer1 = Offer(student_id=students[0].id, recruiter_id=recruiters[0].id, job_id=jobs[0].id, ctc=1200000, offer_date=datetime.datetime.now(), status=OfferStatus.PENDING)
    db.add(offer1)
    db.commit()

    print("Seeding complete!")

if __name__ == "__main__":
    seed_db()
