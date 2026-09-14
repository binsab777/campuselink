# Development Roadmap

This project will be built progressively through the following logical phases:

## Phase 1: Foundation
- Project setup (Frontend Next.js, Backend FastAPI).
- Dockerization and Database setup (PostgreSQL).
- Basic CI/CD, linting, and formatting.

## Phase 2: Authentication & Roles
- JWT-based authentication.
- User management and RBAC (Super Admin, Placement Officer, Recruiter, Student, Mentor).

## Phase 3: Student & Recruiter Management
- Student profile CRUD (academics, skills, projects).
- Company and recruiter profile CRUD.

## Phase 4: Placement Management
- Job postings (JDs) and eligibility criteria.
- Placement Drives creation and management.
- Basic application workflow (Apply -> Shortlist -> Reject).

## Phase 5: Readiness & Skill-Gap Analysis
- Initial rule-based assessment and scoring.
- Highlighting missing skills based on basic exact-match logic.

## Phase 6: AI Matching
- Integrate `pgvector` and `sentence-transformers`.
- Implement vector embeddings for students and JDs.
- Generate explainable AI match scores.

## Phase 7: Scheduling & Conflict Detection
- Interview scheduling system.
- Logic to prevent double-booking for students/interviewers.

## Phase 8: Offer & Documentation Tracking
- Offer rollout workflows.
- Uploading and verifying offer letters.

## Phase 9: Analytics
- Real-time dashboards for Placement Officers.
- Placement statistics and drive success rates.

## Phase 10: Predictive ML
- Historical data analysis to predict placement probability.

## Phase 11: RAG/AI Assistant
- LLM integration for conversational query over placement data.

## Phase 12: Production Deployment
- Final security audits, optimization, and production deployment.

## MVP Scope (Minimum Viable Product)
The MVP targets demonstrating end-to-end value with essential features:
- Core Profiles (Students, Jobs)
- AI Matching Engine (Vector-based)
- Basic Scheduling
- Notifications (Mocked or simple email)
- Offer Tracking
- Essential Analytics Dashboard
