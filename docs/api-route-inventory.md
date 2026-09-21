# API Route Inventory
## Count Summary
- **FastAPI routes**: 71
- **Laravel routes**: 70
- **Matched routes**: 70
- **Missing in Laravel**: 1 (`GET /api/v1/admin/only` - dummy test endpoint)

| # | Method | Route Pattern | FastAPI Controller/Action | Laravel Controller/Action | Auth / Middleware | Status |
|---|--------|---------------|---------------------------|---------------------------|-------------------|--------|
| 1 | POST | /api/v1/auth/login | unknown | AuthController@login | Public | MATCHED |
| 2 | POST | /api/v1/auth/register | unknown | AuthController@register | Public | MATCHED |
| 3 | POST | /api/v1/auth/refresh | unknown | AuthController@refresh | Public | MATCHED |
| 4 | GET | /api/v1/auth/me | unknown | AuthController@me | Illuminate\Auth\Middleware\Authenticate:sanctum | MATCHED |
| 5 | GET | /api/v1/students/me | unknown | StudentController@getProfile | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 6 | PUT | /api/v1/students/me | unknown | StudentController@updateBasicInfo | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 7 | GET | /api/v1/students/me/completeness | unknown | StudentController@completeness | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 8 | GET | /api/v1/students/me/full | unknown | StudentController@getFullProfile | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 9 | GET | /api/v1/students/me/academic | unknown | StudentAcademicController@index | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 10 | POST | /api/v1/students/me/academic | unknown | StudentAcademicController@store | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 11 | PUT | /api/v1/students/me/academic/{hist_id} | unknown | StudentAcademicController@update | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 12 | DELETE | /api/v1/students/me/academic/{hist_id} | unknown | StudentAcademicController@destroy | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 13 | GET | /api/v1/students/me/skills | unknown | StudentSkillController@index | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 14 | POST | /api/v1/students/me/skills | unknown | StudentSkillController@store | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 15 | PUT | /api/v1/students/me/skills/{skill_id} | unknown | StudentSkillController@update | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 16 | DELETE | /api/v1/students/me/skills/{skill_id} | unknown | StudentSkillController@destroy | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 17 | GET | /api/v1/students/me/projects | unknown | StudentProjectController@index | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 18 | POST | /api/v1/students/me/projects | unknown | StudentProjectController@store | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 19 | PUT | /api/v1/students/me/projects/{project_id} | unknown | StudentProjectController@update | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 20 | DELETE | /api/v1/students/me/projects/{project_id} | unknown | StudentProjectController@destroy | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 21 | GET | /api/v1/students/me/certifications | unknown | StudentCertificationController@index | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 22 | POST | /api/v1/students/me/certifications | unknown | StudentCertificationController@store | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 23 | PUT | /api/v1/students/me/certifications/{cert_id} | unknown | StudentCertificationController@update | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 24 | DELETE | /api/v1/students/me/certifications/{cert_id} | unknown | StudentCertificationController@destroy | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 25 | POST | /api/v1/students/me/resume | unknown | StudentController@uploadResume | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 26 | DELETE | /api/v1/students/me/resume | unknown | StudentController@deleteResume | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 27 | GET | /api/v1/students/me/drives | unknown | StudentController@drives | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 28 | GET | /api/v1/recruiters/me | unknown | RecruiterController@me | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:RECRUITER | MATCHED |
| 29 | PUT | /api/v1/recruiters/me/company | unknown | RecruiterController@updateCompany | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:RECRUITER | MATCHED |
| 30 | GET | /api/v1/recruiters/me/jobs | unknown | RecruiterJobController@index | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:RECRUITER | MATCHED |
| 31 | POST | /api/v1/recruiters/me/jobs | unknown | RecruiterJobController@store | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:RECRUITER | MATCHED |
| 32 | GET | /api/v1/recruiters/me/jobs/{job_id} | unknown | RecruiterJobController@show | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:RECRUITER | MATCHED |
| 33 | PUT | /api/v1/recruiters/me/jobs/{job_id} | unknown | RecruiterJobController@update | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:RECRUITER | MATCHED |
| 34 | DELETE | /api/v1/recruiters/me/jobs/{job_id} | unknown | RecruiterJobController@destroy | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:RECRUITER | MATCHED |
| 35 | GET | /api/v1/recruiters/me/drives | unknown | RecruiterDriveController@index | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:RECRUITER | MATCHED |
| 36 | POST | /api/v1/recruiters/me/drives | unknown | RecruiterDriveController@store | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:RECRUITER | MATCHED |
| 37 | PUT | /api/v1/recruiters/me/drives/{drive_id} | unknown | RecruiterDriveController@update | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:RECRUITER | MATCHED |
| 38 | GET | /api/v1/recruiters/me/dashboard | unknown | RecruiterController@dashboard | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:RECRUITER | MATCHED |
| 39 | GET | /api/v1/recruiters/candidates/{student_id} | unknown | RecruiterController@candidate | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:RECRUITER | MATCHED |
| 40 | GET | /api/v1/jobs/skills/all | unknown | JobController@skillsAll | Illuminate\Auth\Middleware\Authenticate:sanctum | MATCHED |
| 41 | GET | /api/v1/jobs/{job_id}/requirements | unknown | JobController@requirements | Illuminate\Auth\Middleware\Authenticate:sanctum | MATCHED |
| 42 | POST | /api/v1/jobs/{job_id}/requirements | unknown | JobController@addRequirement | Illuminate\Auth\Middleware\Authenticate:sanctum | MATCHED |
| 43 | DELETE | /api/v1/jobs/{job_id}/requirements/{req_id} | unknown | JobController@removeRequirement | Illuminate\Auth\Middleware\Authenticate:sanctum | MATCHED |
| 44 | POST | /api/v1/jobs/{job_id}/eligibility/check | unknown | JobController@checkEligibilityAdmin | Illuminate\Auth\Middleware\Authenticate:sanctum | MATCHED |
| 45 | GET | /api/v1/jobs/available | unknown | JobController@index | Illuminate\Auth\Middleware\Authenticate:sanctum | MATCHED |
| 46 | GET | /api/v1/jobs/{job_id}/my-eligibility | unknown | JobController@checkEligibility | Illuminate\Auth\Middleware\Authenticate:sanctum | MATCHED |
| 47 | POST | /api/v1/jobs/{job_id}/apply | unknown | JobApplicationController@apply | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 48 | POST | /api/v1/drives/{drive_id}/candidates | unknown | DriveController@addCandidate | Illuminate\Auth\Middleware\Authenticate:sanctum | MATCHED |
| 49 | GET | /api/v1/drives/{drive_id}/candidates | unknown | DriveController@candidates | Illuminate\Auth\Middleware\Authenticate:sanctum | MATCHED |
| 50 | GET | /api/v1/drives/available | unknown | DriveController@available | Illuminate\Auth\Middleware\Authenticate:sanctum | MATCHED |
| 51 | PATCH | /api/v1/drives/{drive_id}/candidates/{candidate_id} | unknown | DriveController@updateCandidate | Illuminate\Auth\Middleware\Authenticate:sanctum | MATCHED |
| 52 | POST | /api/v1/drives/{drive_id}/evaluate-eligibility | unknown | DriveController@evaluate | Illuminate\Auth\Middleware\Authenticate:sanctum | MATCHED |
| 53 | POST | /api/v1/drives/{drive_id}/withdraw | unknown | DriveController@withdraw | Illuminate\Auth\Middleware\Authenticate:sanctum | MATCHED |
| 54 | GET | /api/v1/readiness/me | unknown | ReadinessController@me | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 55 | POST | /api/v1/readiness/me/recalculate | unknown | ReadinessController@recalculate | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 56 | GET | /api/v1/readiness/me/jobs/{job_id}/skill-gaps | unknown | ReadinessController@gaps | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 57 | POST | /api/v1/readiness/me/jobs/{job_id}/skill-gaps/analyze | unknown | ReadinessController@analyze | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:STUDENT | MATCHED |
| 58 | GET | /api/v1/readiness/students/{student_id} | unknown | ReadinessController@studentReadiness | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:SUPER_ADMIN,PLACEMENT_OFFICER | MATCHED |
| 59 | GET | /api/v1/readiness/students/{student_id}/jobs/{job_id}/skill-gaps | unknown | ReadinessController@studentGaps | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:SUPER_ADMIN,PLACEMENT_OFFICER | MATCHED |
| 60 | GET | /api/v1/admin/users | unknown | AdminController@index | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:SUPER_ADMIN,PLACEMENT_OFFICER | MATCHED |
| 61 | PATCH | /api/v1/admin/users/{user_id}/status | unknown | AdminController@status | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:SUPER_ADMIN,PLACEMENT_OFFICER | MATCHED |
| 62 | PATCH | /api/v1/admin/users/{user_id}/role | unknown | AdminController@role | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:SUPER_ADMIN | MATCHED |
| 63 | GET | /api/v1/skills | unknown | SkillController@index | Public | MATCHED |
| 64 | POST | /api/v1/skills | unknown | SkillController@store | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:SUPER_ADMIN,PLACEMENT_OFFICER | MATCHED |
| 65 | PUT | /api/v1/skills/{skill_id} | unknown | SkillController@update | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:SUPER_ADMIN,PLACEMENT_OFFICER | MATCHED |
| 66 | DELETE | /api/v1/skills/{skill_id} | unknown | SkillController@destroy | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:SUPER_ADMIN,PLACEMENT_OFFICER | MATCHED |
| 67 | GET | /api/v1/officer/students | unknown | OfficerController@students | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:SUPER_ADMIN,PLACEMENT_OFFICER | MATCHED |
| 68 | GET | /api/v1/officer/students/{student_id} | unknown | OfficerController@student | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:SUPER_ADMIN,PLACEMENT_OFFICER | MATCHED |
| 69 | GET | /api/v1/officer/companies | unknown | OfficerController@companies | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:SUPER_ADMIN,PLACEMENT_OFFICER | MATCHED |
| 70 | POST | /api/v1/officer/companies | unknown | OfficerController@storeCompany | Illuminate\Auth\Middleware\Authenticate:sanctum, App\Http\Middleware\CheckRole:SUPER_ADMIN,PLACEMENT_OFFICER | MATCHED |
| 71 | GET | /api/v1/admin/only | unknown | N/A | N/A | MISSING IN LARAVEL |
