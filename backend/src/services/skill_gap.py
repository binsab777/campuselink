import datetime
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session
from src.models.all_models import (
    Student, StudentSkill, Job, JobRequirement, Skill, SkillGap
)
from src.models.enums import ProficiencyLevel, GapSeverity
from src.services.readiness import calculate_readiness

PROFICIENCY_NUMERIC: Dict[ProficiencyLevel, int] = {
    ProficiencyLevel.BEGINNER: 1,
    ProficiencyLevel.INTERMEDIATE: 2,
    ProficiencyLevel.ADVANCED: 3,
    ProficiencyLevel.EXPERT: 4,
}

NUMERIC_TO_PROFICIENCY: Dict[int, ProficiencyLevel] = {
    1: ProficiencyLevel.BEGINNER,
    2: ProficiencyLevel.INTERMEDIATE,
    3: ProficiencyLevel.ADVANCED,
    4: ProficiencyLevel.EXPERT,
}

# Domain-grounded syllabus recommendations
SKILL_RECOMMENDATION_TEMPLATES: Dict[str, Dict[str, str]] = {
    "docker": {
        "CRITICAL": "Urgent: Master Docker architecture, image build fundamentals, Dockerfile creation, multi-stage builds, container lifecycle, and Docker Compose orchestration.",
        "HIGH": "Learn Docker basics, Dockerfile optimization, container networking, volumes, and multi-container setups with Docker Compose.",
        "MEDIUM": "Deepen container knowledge with multi-stage builds, non-root user permissions, and container security best practices.",
        "LOW": "Review container resource limits, healthchecks, and production container deployment."
    },
    "aws": {
        "CRITICAL": "Essential cloud foundation needed: Master AWS IAM policies, EC2 compute instances, S3 object storage, VPC basics, and basic serverless (Lambda).",
        "HIGH": "Focus on core AWS services: IAM security, EC2 lifecycle, S3 bucket policies, and RDS database management.",
        "MEDIUM": "Enhance cloud skills with CloudWatch monitoring, Load Balancer configuration, and ECS/EKS container deployments.",
        "LOW": "Learn AWS Infrastructure as Code (CloudFormation/Terraform) and cost-optimization principles."
    },
    "python": {
        "CRITICAL": "Core Python foundation required: Study data structures, OOP principles, decorators, generators, exceptions, and file/network I/O.",
        "HIGH": "Advance Python capabilities: Master async programming (asyncio), type hints, context managers, and write comprehensive pytest test suites.",
        "MEDIUM": "Refine idiomatic Python (PEP 8), memory management, profiling tools, and design patterns.",
        "LOW": "Explore advanced metaprogramming, C-extensions, or specialized performance benchmarking."
    },
    "sql": {
        "CRITICAL": "Mandatory database foundation: Learn relational design, normal forms, primary/foreign keys, complex multi-table JOINs, and GROUP BY aggregations.",
        "HIGH": "Master advanced SQL: Window functions (ROW_NUMBER, RANK, LEAD/LAG), Common Table Expressions (CTEs), transactions, and ACID properties.",
        "MEDIUM": "Focus on database optimization: EXPLAIN query plans, B-tree indexing strategies, partitioning, and connection pooling.",
        "LOW": "Study database replication topologies, distributed queries, and query tuning for large-scale datasets."
    },
    "react": {
        "CRITICAL": "Frontend essentials needed: Understand JSX, component lifecycle, props vs state, React hooks (useState, useEffect, useMemo), and DOM event handling.",
        "HIGH": "Advance React patterns: Custom hooks, Context API, state management (Redux/Zustand), component memoization, and Next.js App Router.",
        "MEDIUM": "Refine frontend skills: Server-side rendering (SSR), Suspense, performance profiling, and accessible semantic HTML.",
        "LOW": "Explore micro-frontend architectures, bundle splitting, and automated E2E testing (Playwright/Cypress)."
    },
    "java": {
        "CRITICAL": "Object-oriented core needed: Java OOP fundamentals, Collections framework (List, Map, Set), exception handling, and Streams API.",
        "HIGH": "Enterprise Java foundation: Spring Boot, REST APIs, Hibernate/JPA ORM, Maven/Gradle build tools, and unit testing with JUnit/Mockito.",
        "MEDIUM": "Advance multi-threading, concurrency utilities (ExecutorService), JVM garbage collection, and microservices architecture.",
        "LOW": "Deepen JVM memory tuning, reactive programming (Project Reactor/WebFlux), and cloud-native deployments."
    },
    "machine learning": {
        "CRITICAL": "ML foundation: Review linear algebra, calculus, scikit-learn algorithms (regression, classification, clustering), and model evaluation metrics.",
        "HIGH": "Advance to neural networks, feature engineering, cross-validation, hyperparameter tuning, and PyTorch/TensorFlow pipelines.",
        "MEDIUM": "Focus on model deployment, MLflow tracking, data versioning, and feature stores.",
        "LOW": "Study model monitoring in production, concept drift detection, and scalable inference architectures."
    }
}

def generate_recommendation(skill_name: str, required_prof: ProficiencyLevel, severity: GapSeverity) -> str:
    if severity == GapSeverity.NONE:
        return f"Current proficiency in {skill_name} satisfies job requirements. Maintain active hands-on practice."
        
    normalized_key = skill_name.lower().strip()
    if normalized_key in SKILL_RECOMMENDATION_TEMPLATES:
        template = SKILL_RECOMMENDATION_TEMPLATES[normalized_key]
        if severity.value in template:
            return template[severity.value]
            
    # Generic structured fallback
    target_prof_str = required_prof.value.capitalize()
    if severity in [GapSeverity.CRITICAL, GapSeverity.HIGH]:
        return f"High priority: Build core competencies in {skill_name} through targeted coursework and practical implementation to reach {target_prof_str} proficiency."
    elif severity == GapSeverity.MEDIUM:
        return f"Moderate gap: Advance practical {skill_name} capabilities to {target_prof_str} through project-based exercises."
    else:
        return f"Minor refinement: Review advanced concepts and industry patterns in {skill_name} to fulfill {target_prof_str} expectations."

def analyze_skill_gaps(
    db: Session,
    student_id: int,
    job_id: int,
    persist: bool = True
) -> Dict[str, Any]:
    """
    Deterministically computes skill gap analysis for a student against a target job.
    Categorizes skills into MATCHED, PARTIAL, MISSING with severity and tailored recommendations.
    Also calculates job-specific readiness score (0-100%).
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise ValueError(f"Student with ID {student_id} not found.")

    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise ValueError(f"Job with ID {job_id} not found.")

    # Student skills map: skill_id -> StudentSkill
    student_skills_map: Dict[int, StudentSkill] = {
        ss.skill_id: ss for ss in (student.skills or [])
    }

    requirements = job.requirements or []
    
    matched_skills = []
    partial_skills = []
    missing_skills = []
    gap_records = []

    total_mandatory_weight = 0.0
    earned_mandatory_weight = 0.0
    total_preferred_weight = 0.0
    earned_preferred_weight = 0.0

    for req in requirements:
        skill = req.skill
        skill_name = skill.name if skill else f"Skill #{req.skill_id}"
        req_numeric = PROFICIENCY_NUMERIC[req.required_proficiency]
        weight = req.weight if req.weight and req.weight > 0 else 1.0

        if req.is_mandatory:
            total_mandatory_weight += weight
        else:
            total_preferred_weight += weight

        if req.skill_id in student_skills_map:
            ss = student_skills_map[req.skill_id]
            student_numeric = PROFICIENCY_NUMERIC[ss.proficiency_level]
            diff = req_numeric - student_numeric

            if diff <= 0:
                # MATCHED
                severity = GapSeverity.NONE
                status = "MATCHED"
                earned = weight
                recommendation = generate_recommendation(skill_name, req.required_proficiency, severity)
                matched_skills.append({
                    "skill_id": req.skill_id,
                    "skill_name": skill_name,
                    "required_proficiency": req.required_proficiency.value,
                    "student_proficiency": ss.proficiency_level.value,
                    "severity": severity.value,
                    "is_mandatory": req.is_mandatory,
                    "recommendation": recommendation
                })
            else:
                # PARTIAL MATCH
                status = "PARTIAL"
                earned = weight * (student_numeric / req_numeric)
                if diff == 1:
                    severity = GapSeverity.LOW if not req.is_mandatory else GapSeverity.MEDIUM
                elif diff == 2:
                    severity = GapSeverity.MEDIUM if not req.is_mandatory else GapSeverity.HIGH
                else:
                    severity = GapSeverity.HIGH if not req.is_mandatory else GapSeverity.CRITICAL
                    
                recommendation = generate_recommendation(skill_name, req.required_proficiency, severity)
                partial_skills.append({
                    "skill_id": req.skill_id,
                    "skill_name": skill_name,
                    "required_proficiency": req.required_proficiency.value,
                    "student_proficiency": ss.proficiency_level.value,
                    "severity": severity.value,
                    "is_mandatory": req.is_mandatory,
                    "recommendation": recommendation
                })
        else:
            # MISSING
            status = "MISSING"
            earned = 0.0
            student_numeric = 0
            if req.is_mandatory:
                if req_numeric >= 3:
                    severity = GapSeverity.CRITICAL
                elif req_numeric == 2:
                    severity = GapSeverity.HIGH
                else:
                    severity = GapSeverity.MEDIUM
            else:
                if req_numeric >= 3:
                    severity = GapSeverity.HIGH
                elif req_numeric == 2:
                    severity = GapSeverity.MEDIUM
                else:
                    severity = GapSeverity.LOW

            recommendation = generate_recommendation(skill_name, req.required_proficiency, severity)
            missing_skills.append({
                "skill_id": req.skill_id,
                "skill_name": skill_name,
                "required_proficiency": req.required_proficiency.value,
                "student_proficiency": None,
                "severity": severity.value,
                "is_mandatory": req.is_mandatory,
                "recommendation": recommendation
            })

        if req.is_mandatory:
            earned_mandatory_weight += earned
        else:
            earned_preferred_weight += earned

        gap_records.append({
            "skill_id": req.skill_id,
            "skill_name": skill_name,
            "required_level": req_numeric,
            "current_level": student_numeric if student_numeric > 0 else None,
            "required_proficiency": req.required_proficiency.value,
            "student_proficiency": NUMERIC_TO_PROFICIENCY[student_numeric].value if student_numeric > 0 else None,
            "gap_severity": severity.value,
            "is_mandatory": req.is_mandatory,
            "status": status,
            "recommendation": recommendation
        })

    # Calculate Job Readiness Score (0 - 100%)
    mandatory_score = (
        (earned_mandatory_weight / total_mandatory_weight * 100.0)
        if total_mandatory_weight > 0 else 100.0
    )
    preferred_score = (
        (earned_preferred_weight / total_preferred_weight * 100.0)
        if total_preferred_weight > 0 else 100.0
    )

    # Get student's global readiness score
    global_readiness_data = calculate_readiness(db, student_id, persist=False)
    global_score = global_readiness_data["overall_score"]

    job_readiness_score = round(
        (mandatory_score * 0.60) + (preferred_score * 0.20) + (global_score * 0.20),
        1
    )

    # Persist in skill_gaps if requested
    if persist and requirements:
        # Delete existing gaps for (student_id, job_id)
        db.query(SkillGap).filter(
            SkillGap.student_id == student_id,
            SkillGap.job_id == job_id
        ).delete()

        for g in gap_records:
            gap_entity = SkillGap(
                student_id=student_id,
                job_id=job_id,
                skill_id=g["skill_id"],
                gap_severity=g["gap_severity"],
                current_level=g["current_level"],
                required_level=g["required_level"],
                is_mandatory=g["is_mandatory"],
                analysis_version="v1.0",
                recommendation=g["recommendation"]
            )
            db.add(gap_entity)
        db.commit()

    return {
        "job_id": job.id,
        "job_title": job.title,
        "company_id": job.company_id,
        "company_name": job.company.name if job.company else None,
        "job_readiness_score": job_readiness_score,
        "global_readiness_score": global_score,
        "mandatory_skills_score": round(mandatory_score, 1),
        "preferred_skills_score": round(preferred_score, 1),
        "total_requirements": len(requirements),
        "matched_count": len(matched_skills),
        "partial_count": len(partial_skills),
        "missing_count": len(missing_skills),
        "matched_skills": matched_skills,
        "partial_skills": partial_skills,
        "missing_skills": missing_skills,
        "gaps": gap_records,
        "analysis_version": "v1.0",
        "analyzed_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
