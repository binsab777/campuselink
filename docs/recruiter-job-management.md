# Phase 5: Recruiter, Job & Placement Drive Management

## Architecture Overview

The Recruiter module provides a secure, role-based boundary for corporate partners to manage their placement activities on the CAMPUSLINK platform. It establishes the foundational schema required for the future AI matching engine without tightly coupling to it.

### Key Components

1. **Company & Recruiter Profiles**
   - **Company**: Stores organization-level data (industry, size, metadata). Serves as the root entity for Jobs and Drives.
   - **Recruiter**: A `User` with `RECRUITER` role. Acts as a proxy or agent for a `Company`.

2. **Job Management**
   - **Job**: Contains details about an open position (title, description, salary, remote type).
   - **Eligibility Config**: A JSON structure storing hard eligibility rules (e.g., minimum CGPA, allowed branches, maximum backlogs).
   - **JobRequirement**: Normalized relational table linking `Job` to `Skill`, defining the `ProficiencyLevel`, weight, and whether the skill is mandatory. This normalized structure is critical for future ML/AI similarity scoring.

3. **Deterministic Eligibility Engine**
   - Implemented in `src/services/eligibility.py`.
   - Before a student applies to a job or registers for a drive, the backend validates their `Student` profile against the Job's `eligibility_config`.
   - Returns a structured response containing `is_eligible` and a list of specific failure reasons (e.g., "CGPA 7.5 is below the required minimum of 8.0").

4. **Placement Drives**
   - **PlacementDrive**: Represents a campus event. Linked to a `Company` and optionally a specific `Job`.
   - **DriveCandidate**: Represents a student's registration for a drive. Maintains an `eligibility_status` flag updated upon registration, and a `shortlist_status` flag for recruiter workflows.

## API Boundaries

- `GET /api/v1/recruiters/me`: Fetch recruiter profile and associated company.
- `PUT /api/v1/recruiters/me/company`: Update company information.
- `POST /api/v1/recruiters/me/jobs`: Create a new job listing.
- `POST /api/v1/jobs/{id}/eligibility/check`: Deterministic check for a student against a job.
- `POST /api/v1/drives`: Create a placement drive.
- `POST /api/v1/drives/{id}/candidates`: Register a candidate for a drive (authorized for the student themselves, or the owning recruiter).

## Security & Authorization

- All endpoints are protected by JWT authentication.
- Recruiter endpoints strictly enforce ownership: a recruiter can only modify Jobs and Drives belonging to their `company_id`.
- Students can only register themselves for drives, preventing ID spoofing.
