# Major System Modules

To ensure modularity and maintainability, the CAMPUSLINK backend and frontend are divided into distinct logical modules.

## 1. Authentication & Authorization
- **Responsibilities**: User login, registration, JWT token generation/validation, password reset, and Role-Based Access Control (RBAC).
- **Roles**:
  - **Super Admin**: Platform owner, manages settings, all users, global analytics.
  - **Placement Officer**: College representative, manages students, drives, and recruiters.
  - **Recruiter**: Company representative, posts jobs, views applicants, conducts interviews.
  - **Student**: Job seeker, manages profile, applies for jobs, views schedules.
  - **Mentor**: Assists students with skill gaps, mock interviews, and readiness.

## 2. Student Management
- **Responsibilities**: Student profile CRUD, academic history, skill inventory, uploaded projects, certifications, and assessment records.

## 3. Recruiter Management
- **Responsibilities**: Company profiles, recruiter contacts, company policies, historical hiring data.

## 4. Job/Requirement Management
- **Responsibilities**: Job Postings (JDs), required skills, eligibility criteria, salary details, and application deadlines.

## 5. Placement Drives
- **Responsibilities**: Managing placement events (on-campus, off-campus), associating multiple jobs to a drive, tracking drive participants.

## 6. Matching & Readiness Engine (AI/ML)
- **Responsibilities**:
  - Analyzing student profiles vs. Job Descriptions.
  - Providing a compatibility score using vector embeddings and skill extraction.
  - Generating skill-gap analysis (identifying what the student lacks).
  - Readiness scoring based on assessments and profile completeness.

## 7. Scheduling Engine
- **Responsibilities**: Interview slot generation, conflict detection (e.g., student double-booked), managing interviewer availability.

## 8. Offer & Documentation Management
- **Responsibilities**: Tracking job offers, offer letter generation/upload, student acceptance/rejection, and onboarding document verification.

## 9. Notification System
- **Responsibilities**: Email and in-app alerts for interview schedules, job recommendations, application status changes, and drive announcements.

## 10. Analytics & Reporting
- **Responsibilities**: Real-time dashboards.
  - Placement metrics (placed vs. unplaced).
  - Skill trends (what recruiters are asking for vs. what students have).
  - Drive success rates.

## 11. Audit & Logging
- **Responsibilities**: Tracking system changes, important user actions (e.g., who changed an offer status, when an interview was cancelled).
