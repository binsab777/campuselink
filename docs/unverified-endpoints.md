# Unverified Endpoints Worklist

## 1. Candidate Pipeline (Recruiter)
- **Endpoint:** `GET /api/v1/recruiters/me/dashboard`
  - **Reason Not Verified:** Missing deep relational test for recruiter dashboard metrics matching FastAPI's `RecruiterProfileOut`.
  - **Next Action:** Create `DashboardParityTest.php` mapping recruiter company, jobs, and candidates, verifying the output stats.
- **Endpoint:** `GET /api/v1/recruiters/candidates/{id}`
  - **Reason Not Verified:** Candidate detailed view lacks tests ensuring recruiter cannot view unauthorized candidates.
  - **Next Action:** Add `CandidateParityTest.php` with RBAC assertions (own candidate vs other recruiter's candidate).

## 2. Student Profile CRUD
- **Endpoints (12 total):** `GET/POST/PUT/DELETE /api/v1/students/me/skills`, `/api/v1/students/me/projects`, `/api/v1/students/me/certifications`
  - **Reason Not Verified:** While `AcademicHistory` was mapped and verified, Projects, Skills, and Certifications still lack dedicated FormRequest vs DB schema field mapping parity tests.
  - **Next Action:** Create `StudentProfileParityTest.php` to run CRUD workflows for Projects, Skills, and Certs, verifying PostgreSQL constraints.

## 3. Placement Officer Directory
- **Endpoints:** `GET /api/v1/officer/students/{id}`, `GET /api/v1/officer/companies`
  - **Reason Not Verified:** The endpoints are scaffolded but lack deep filtering parity tests (CGPA filters, department/branch filtering combinations).
  - **Next Action:** Expand `OfficerParityTest.php` to include multi-filter query tests and single-student read constraints.

## 4. Master Skills
- **Endpoints:** `PUT /api/v1/skills/{id}`, `DELETE /api/v1/skills/{id}`
  - **Reason Not Verified:** Controller logic was patched for deletion safety, but no automated test guarantees the transaction rollback if a skill is actively used by a JobRequirement.
  - **Next Action:** Add tests in `SkillParityTest.php` for `DELETE` against used/unused skills.

## 5. Readiness Gaps
- **Endpoints:** `GET /api/v1/readiness/students/{id}`, `GET /api/v1/readiness/students/{s_id}/jobs/{j_id}/skill-gaps`
  - **Reason Not Verified:** Currently testing `me` endpoints for students, but officer-access to readiness metrics is untested for authorization bounds.
  - **Next Action:** Add tests to `ReadinessParityTest.php` acting as Officer evaluating a Student.

## 6. Resumes
- **Endpoints:** `POST /api/v1/students/me/resume`, `DELETE /api/v1/students/me/resume`
  - **Reason Not Verified:** File storage parity (Disk/S3 mapping and MIME validation) is untested.
  - **Next Action:** Create `ResumeUploadTest.php` simulating `application/pdf` uploads using `Storage::fake()`.
