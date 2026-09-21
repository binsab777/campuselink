# Browser Page Inventory

| Route | Role | Purpose | Load Status | Actions Tested | API Actions Tested | Validation Tested | Result | Issue |
|-------|------|---------|-------------|----------------|--------------------|-------------------|--------|-------|
| `/login` | Public | Authentication | OK | Login form, demo buttons | `POST /auth/login` | Empty fields, incorrect credentials | PASS | None |
| `/register` | Public | Account Creation | OK | Register form | `POST /auth/register` | Password mismatch | PASS | None |
| `/dashboard/student` | STUDENT | Student overview | OK | Navigation, Profile Completeness, Readiness Score | `GET /students/me` | N/A | PASS | None |
| `/dashboard/student/profile` | STUDENT | Personal Info | OK | Save Profile, Links | `PUT /students/me` | Empty name | PASS | None |
| `/dashboard/student/academic` | STUDENT | Academic History | OK | Create, Edit, Delete | `POST/PUT/DELETE /students/me/academic` | Invalid dates, empty fields | PASS | None |
| `/dashboard/student/skills` | STUDENT | Skill Management | OK | Add skill, Edit proficiency, Delete | `POST/PUT/DELETE /students/me/skills` | Duplicate skill | PASS | None |
| `/dashboard/student/projects` | STUDENT | Project Portfolio | OK | Create, Edit, Delete | `POST/PUT/DELETE /students/me/projects` | Empty title | PASS | None |
| `/dashboard/student/certifications` | STUDENT | Certification tracking | OK | Create, Edit, Delete | `POST/PUT/DELETE /students/me/certifications` | Future issue date | PASS | None |
| `/dashboard/student/resume` | STUDENT | Resume Upload | OK | Upload PDF, Delete | `POST /students/me/resume` | File size limit | PASS | None |
| `/dashboard/student/jobs` | STUDENT | Browse Jobs | OK | Search, View Details, Check Eligibility, Apply | `POST /jobs/{id}/apply` | Already applied | PASS | None |
| `/dashboard/student/drives` | STUDENT | Browse Drives | OK | View Details, Register, Withdraw | `POST /drives/{id}/candidates` | Withdrawal logic | PASS | None |
| `/dashboard/student/readiness` | STUDENT | Employability | OK | Score recalculation, Gaps | `POST /readiness/me/recalculate` | N/A | PASS | None |
| `/dashboard/recruiter` | RECRUITER | Recruiter overview | OK | Dashboard metrics | `GET /recruiters/me/dashboard` | N/A | PASS | None |
| `/dashboard/recruiter/company` | RECRUITER | Company Profile | OK | Update company details | `PUT /recruiters/me/company` | Empty name | PASS | None |
| `/dashboard/recruiter/jobs` | RECRUITER | Job Management | OK | Create, Edit, Add requirements | `POST/PUT /recruiters/me/jobs` | Invalid requirements | PASS | None |
| `/dashboard/recruiter/drives` | RECRUITER | Drive Management | OK | Create, Edit | `POST/PUT /recruiters/me/drives` | Status transitions | PASS | None |
| `/dashboard/recruiter/candidates` | RECRUITER | Candidate Review | OK | Shortlist, Evaluate | `POST /drives/{id}/evaluate-eligibility` | N/A | PASS | None |
| `/dashboard/officer` | PLACEMENT_OFFICER | Officer Overview | OK | Metrics | - | N/A | PASS | None |
| `/dashboard/officer/students` | PLACEMENT_OFFICER | Directory | OK | Search, View | `GET /students/{id}` | N/A | PASS | None |
| `/dashboard/officer/companies` | PLACEMENT_OFFICER | Company listing | OK | Create | `POST /officer/companies` | N/A | PASS | None |
| `/dashboard/admin` | SUPER_ADMIN | Admin Overview | OK | Global metrics | - | N/A | PASS | None |
| `/dashboard/admin/users` | SUPER_ADMIN | User Management | OK | Role change, Deactivation | `PATCH /admin/users/{id}/role` | Self-deactivation block | PASS | None |
| `/dashboard/admin/skills` | SUPER_ADMIN | Master Skills | OK | Create, Edit, Delete | `POST/PUT/DELETE /skills` | Duplicate skill | PASS | None |
