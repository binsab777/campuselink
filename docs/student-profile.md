# Student Profile Module (Phase 4)

The Student Profile module is the central hub for storing student employability data. It is designed to act as the primary source of truth for the upcoming AI modules (Readiness Scoring and Recruiter Matching).

## Core Data Architecture

The architecture segregates the profile into functional areas to maintain clean relations and allow granular updates.

1. **Basic Info (`Student` model)**
   - Core identity: Name, Roll Number, Phone, DOB, Gender
   - Core academics: Branch, Graduation Year, CGPA, Backlogs
   - Extensible JSON schema (`profile_metadata`) for dynamic fields like `bio`, `github_url`, `linkedin_url`, `career_interests`.

2. **Academic History (`StudentAcademicHistory`)**
   - Detailed past qualifications (e.g., 10th, 12th, Diploma, B.Tech).
   - Allows tracking upward/downward academic trends.

3. **Skills Management (`StudentSkill`)**
   - Many-to-many relationship mapping a student to global `Skill` definitions.
   - Captures `proficiency_level` (BEGINNER to EXPERT).
   - Captures `source` (STUDENT, RESUME, AI_EXTRACTED) which will be crucial for auditability when AI starts extracting skills automatically in later phases.

4. **Projects & Certifications (`StudentProject`, `StudentCertification`)**
   - Stores granular records rather than comma-separated text strings.

## API Endpoints

The API is structured around `/api/v1/students/me` to inherently enforce authorization—students can only modify their own data.

| Endpoint | Method | Description |
|---|---|---|
| `/students/me` | GET, PUT | Manage basic info and JSON metadata. |
| `/students/me/full` | GET | Aggregates all profile aspects into a single large payload for UI consumption. |
| `/students/me/academic` | GET, POST, DELETE | Manage historical academic records. |
| `/students/me/skills` | GET, POST, DELETE | Manage skills with proficiency and source tags. |
| `/students/me/projects` | GET, POST, PUT, DELETE | Manage projects. |
| `/students/me/certifications`| GET, POST, DELETE | Manage certifications. |
| `/students/me/resume` | POST, DELETE | MVP local file storage for resumes, mounting static files in FastAPI. |
| `/students/me/completeness` | GET | Deterministic score (0-100%) indicating how many sections are filled. |

## Profile Completeness vs Readiness Score

- **Completeness**: Implemented in Phase 4. It purely calculates if data fields are populated. (e.g., "You filled out 80% of your profile.")
- **Readiness Score**: To be implemented in Phase 5. It uses predictive modeling to evaluate *quality* (e.g., "Your skills and CGPA give you a high probability of passing a TechCorp interview").

## UI Implementation
A Next.js dashboard view is available at `/dashboard/profile` rendering the aggregated `StudentProfileResponse` efficiently.
