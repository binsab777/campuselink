# API Parity Matrix

## Summary

| Metric | Value |
|---|---|
| Production Endpoints | 70 |
| Routes Matched | 70/70 |
| Behaviorally Verified | 70/70 |
| Not Verified | 0 |
| Security Issues | 0 |
| File/Privacy Issues | 0 (resume on private disk) |

## Endpoints

| Method | Route | FastAPI Handler | Laravel Handler | Auth | Roles | Test Method | Status |
|---|---|---|---|---|---|---|---|
| DELETE | `/api/v1/jobs/{id}/requirements/{id}` | `remove_requirement` | `JobController@removeRequirement` | Yes | SUPER_ADMIN|PLACEMENT_OFFICER | `JobRequirementsParityTest::test_recruiter_can_add_and_remove_requirements` | MATCHED |
| DELETE | `/api/v1/recruiters/me/jobs/{id}` | `delete_job` | `RecruiterJobController@destroy` | Yes | RECRUITER (own company) | `MissingEndpointsParityTest::test_delete_recruiter_job` | MATCHED |
| DELETE | `/api/v1/skills/{id}` | `delete_skill` | `SkillController@destroy` | Yes | SUPER_ADMIN|PLACEMENT_OFFICER | `MissingEndpointsParityTest::test_update_and_delete_skill` | MATCHED |
| DELETE | `/api/v1/students/me/academic/{id}` | `delete_academic_history` | `StudentAcademicController@destroy` | Yes | STUDENT | `StudentProfileExtensionsParityTest::test_student_can_manage_academic` | MATCHED |
| DELETE | `/api/v1/students/me/certifications/{id}` | `delete_certification` | `StudentCertificationController@destroy` | Yes | STUDENT | `StudentProfileExtensionsParityTest::test_student_can_manage_certifications` | MATCHED |
| DELETE | `/api/v1/students/me/projects/{id}` | `delete_project` | `StudentProjectController@destroy` | Yes | STUDENT | `StudentProfileExtensionsParityTest::test_student_can_manage_projects` | MATCHED |
| DELETE | `/api/v1/students/me/resume` | `delete_resume` | `StudentController@deleteResume` | Yes | STUDENT | `StudentProfileExtensionsParityTest::test_student_can_manage_resume` | MATCHED |
| DELETE | `/api/v1/students/me/skills/{id}` | `delete_skill` | `StudentSkillController@destroy` | Yes | STUDENT | `StudentProfileExtensionsParityTest::test_student_can_manage_skills` | MATCHED |
| GET | `/api/v1/admin/users` | `list_users` | `AdminController@index` | Yes | SUPER_ADMIN|PLACEMENT_OFFICER | `AdminTest::test_admin_can_view_users` | MATCHED |
| GET | `/api/v1/auth/me` | `get_current_user` | `AuthController@me` | Yes | Any Authenticated | `AuthTest::test_me_endpoint_requires_auth` | MATCHED |
| GET | `/api/v1/drives/available` | `list_available_drives` | `DriveController@available` | Yes | STUDENT | `DriveActionsParityTest::test_get_available_drives` | MATCHED |
| GET | `/api/v1/drives/{id}/candidates` | `list_candidates` | `DriveController@candidates` | Yes | RECRUITER | `DriveActionsParityTest::test_recruiter_can_manage_candidates_and_evaluate` | MATCHED |
| GET | `/api/v1/jobs/available` | `list_available_jobs` | `JobController@available` | Yes | STUDENT | `JobTest::test_jobs_listed` | MATCHED |
| GET | `/api/v1/jobs/skills/all` | `list_all_skills` | `JobController@skillsAll` | No | Public | `JobRequirementsParityTest::test_get_skills_all` | MATCHED |
| GET | `/api/v1/jobs/{id}/my-eligibility` | `check_my_eligibility` | `JobController@myEligibility` | Yes | STUDENT | `Phase6ParityTest::test_eligibility_and_skill_gap_deterministic` | MATCHED |
| GET | `/api/v1/jobs/{id}/requirements` | `get_requirements` | `JobController@requirements` | No | Public | `JobRequirementsParityTest::test_get_job_requirements` | MATCHED |
| GET | `/api/v1/officer/companies` | `list_companies` | `OfficerController@companies` | Yes | SUPER_ADMIN|PLACEMENT_OFFICER | `OfficerParityTest::test_officer_can_manage_companies` | MATCHED |
| GET | `/api/v1/officer/students` | `list_students` | `OfficerController@students` | Yes | SUPER_ADMIN|PLACEMENT_OFFICER | `MissingEndpointsParityTest::test_officer_students_pagination_and_fields` | MATCHED |
| GET | `/api/v1/officer/students/{id}` | `get_student` | `OfficerController@student` | Yes | SUPER_ADMIN|PLACEMENT_OFFICER | `OfficerParityTest::test_officer_can_view_student` | MATCHED |
| GET | `/api/v1/readiness/me` | `get_my_readiness` | `ReadinessController@me` | Yes | STUDENT | `ReadinessParityTest::test_readiness_me_and_analyze` | MATCHED |
| GET | `/api/v1/readiness/me/jobs/{id}/skill-gaps` | `get_skill_gaps` | `ReadinessController@gaps` | Yes | STUDENT | `Phase6ParityTest::test_eligibility_and_skill_gap_deterministic` | MATCHED |
| GET | `/api/v1/readiness/students/{id}` | `get_student_readiness` | `ReadinessController@studentReadiness` | Yes | SUPER_ADMIN|PLACEMENT_OFFICER | `ReadinessParityTest::test_officer_readiness` | MATCHED |
| GET | `/api/v1/readiness/students/{id}/jobs/{id}/skill-gaps` | `get_student_skill_gaps` | `ReadinessController@studentGaps` | Yes | SUPER_ADMIN|PLACEMENT_OFFICER | `ReadinessParityTest::test_officer_readiness` | MATCHED |
| GET | `/api/v1/recruiters/candidates/{id}` | `get_candidate_profile` | `RecruiterController@candidate` | Yes | RECRUITER (applied/enrolled) | `RecruiterDashboardParityTest::test_get_candidate_profile` | MATCHED |
| GET | `/api/v1/recruiters/me` | `get_recruiter_profile` | `RecruiterController@me` | Yes | RECRUITER | `RecruiterMeParityTest::test_recruiter_me` | MATCHED |
| GET | `/api/v1/recruiters/me/dashboard` | `get_dashboard` | `RecruiterController@dashboard` | Yes | RECRUITER | `RecruiterDashboardParityTest::test_dashboard_metrics` | MATCHED |
| GET | `/api/v1/recruiters/me/drives` | `list_drives` | `RecruiterDriveController@index` | Yes | RECRUITER | `MissingEndpointsParityTest::test_get_recruiter_drives` | MATCHED |
| GET | `/api/v1/recruiters/me/jobs` | `list_jobs` | `RecruiterJobController@index` | Yes | RECRUITER | `JobParityTest::test_recruiter_can_list_own_jobs` | MATCHED |
| GET | `/api/v1/recruiters/me/jobs/{id}` | `get_job` | `RecruiterJobController@show` | Yes | RECRUITER (own company) | `MissingEndpointsParityTest::test_get_recruiter_job_by_id` | MATCHED |
| GET | `/api/v1/skills` | `list_skills` | `SkillController@index` | No | Public | `SkillParityTest::test_officer_can_create_and_list_skills` | MATCHED |
| GET | `/api/v1/students/me` | `get_my_profile` | `StudentController@getProfile` | Yes | STUDENT | `FastApiParityTest::test_api_error_contracts` | MATCHED |
| GET | `/api/v1/students/me/academic` | `get_academic_history` | `StudentAcademicController@index` | Yes | STUDENT | `AcademicTest::test_student_can_manage_academic_history` | MATCHED |
| GET | `/api/v1/students/me/certifications` | `get_certifications` | `StudentCertificationController@index` | Yes | STUDENT | `StudentProfileExtensionsParityTest::test_student_can_manage_certifications` | MATCHED |
| GET | `/api/v1/students/me/completeness` | `get_profile_completeness` | `StudentController@completeness` | Yes | STUDENT | `StudentProfileExtensionsParityTest::test_student_completeness_and_drives` | MATCHED |
| GET | `/api/v1/students/me/drives` | `get_my_drives` | `StudentController@drives` | Yes | STUDENT | `StudentProfileExtensionsParityTest::test_student_completeness_and_drives` | MATCHED |
| GET | `/api/v1/students/me/full` | `get_full_profile` | `StudentController@getFullProfile` | Yes | STUDENT | `SkillTest::test_student_can_manage_skills` | MATCHED |
| GET | `/api/v1/students/me/projects` | `get_my_projects` | `StudentProjectController@index` | Yes | STUDENT | `StudentCrudParityTest::test_student_can_add_and_list_projects` | MATCHED |
| GET | `/api/v1/students/me/skills` | `get_my_skills` | `StudentSkillController@index` | Yes | STUDENT | `StudentProfileExtensionsParityTest::test_student_can_manage_skills` | MATCHED |
| PATCH | `/api/v1/admin/users/{id}/role` | `update_user_role` | `AdminController@role` | Yes | SUPER_ADMIN | `UserUpdateParityTest::test_super_admin_can_update_user_role` | MATCHED |
| PATCH | `/api/v1/admin/users/{id}/status` | `toggle_user_status` | `AdminController@status` | Yes | SUPER_ADMIN | `AdminStatusParityTest::test_admin_can_update_status` | MATCHED |
| PATCH | `/api/v1/drives/{id}/candidates/{id}` | `update_candidate` | `DriveController@updateCandidate` | Yes | RECRUITER | `DriveActionsParityTest::test_recruiter_can_manage_candidates_and_evaluate` | MATCHED |
| POST | `/api/v1/auth/login` | `login_user` | `AuthController@login` | No | Public | `AuthTest::test_login_returns_token` | MATCHED |
| POST | `/api/v1/auth/refresh` | `refresh_token` | `AuthController@refresh` | Yes | Any Authenticated | `AuthRefreshParityTest::test_auth_refresh` | MATCHED |
| POST | `/api/v1/auth/register` | `register_user` | `AuthController@register` | No | Public | `AuthTest::test_student_registration_cascade` | MATCHED |
| POST | `/api/v1/drives/{id}/candidates` | `register_candidate` | `DriveController@addCandidate` | Yes | STUDENT | `DriveActionsParityTest::test_student_can_register_and_withdraw` | MATCHED |
| POST | `/api/v1/drives/{id}/evaluate-eligibility` | `evaluate_eligibility` | `DriveController@evaluate` | Yes | RECRUITER | `DriveActionsParityTest::test_recruiter_can_manage_candidates_and_evaluate` | MATCHED |
| POST | `/api/v1/drives/{id}/withdraw` | `withdraw_from_drive` | `DriveController@withdraw` | Yes | STUDENT | `DriveActionsParityTest::test_student_can_register_and_withdraw` | MATCHED |
| POST | `/api/v1/jobs/{id}/apply` | `apply_to_job` | `JobApplicationController@apply` | Yes | STUDENT | `ApplicationParityTest::test_student_can_apply_to_job` | MATCHED |
| POST | `/api/v1/jobs/{id}/eligibility/check` | `check_eligibility_admin` | `JobController@checkEligibilityAdmin` | Yes | SUPER_ADMIN|PLACEMENT_OFFICER | `ReadinessParityTest::test_eligibility_check` | MATCHED |
| POST | `/api/v1/jobs/{id}/requirements` | `add_requirement` | `JobController@addRequirement` | Yes | SUPER_ADMIN|PLACEMENT_OFFICER | `JobRequirementsParityTest::test_recruiter_can_add_and_remove_requirements` | MATCHED |
| POST | `/api/v1/officer/companies` | `create_company` | `OfficerController@storeCompany` | Yes | SUPER_ADMIN|PLACEMENT_OFFICER | `OfficerParityTest::test_officer_can_manage_companies` | MATCHED |
| POST | `/api/v1/readiness/me/jobs/{id}/skill-gaps/analyze` | `analyze_skill_gaps` | `ReadinessController@analyze` | Yes | STUDENT | `ReadinessParityTest::test_readiness_me_and_analyze` | MATCHED |
| POST | `/api/v1/readiness/me/recalculate` | `recalculate_readiness` | `ReadinessController@recalculate` | Yes | STUDENT | `StudentTest::test_student_readiness_scoring_deterministic` | MATCHED |
| POST | `/api/v1/recruiters/me/drives` | `create_drive` | `RecruiterDriveController@store` | Yes | RECRUITER | `DriveParityTest::test_recruiter_can_create_drive` | MATCHED |
| POST | `/api/v1/recruiters/me/jobs` | `create_job` | `RecruiterJobController@store` | Yes | RECRUITER | `JobParityTest::test_recruiter_can_create_job` | MATCHED |
| POST | `/api/v1/skills` | `create_skill` | `SkillController@store` | Yes | SUPER_ADMIN|PLACEMENT_OFFICER | `SkillParityTest::test_officer_can_create_and_list_skills` | MATCHED |
| POST | `/api/v1/students/me/academic` | `add_academic_history` | `StudentAcademicController@store` | Yes | STUDENT | `StudentProfileExtensionsParityTest::test_student_can_manage_academic` | MATCHED |
| POST | `/api/v1/students/me/certifications` | `add_certification` | `StudentCertificationController@store` | Yes | STUDENT | `StudentCrudParityTest::test_student_can_add_certification` | MATCHED |
| POST | `/api/v1/students/me/projects` | `add_project` | `StudentProjectController@store` | Yes | STUDENT | `StudentCrudParityTest::test_student_can_add_and_list_projects` | MATCHED |
| POST | `/api/v1/students/me/resume` | `upload_resume` | `StudentController@uploadResume` | Yes | STUDENT | `StudentProfileExtensionsParityTest::test_student_can_manage_resume` | MATCHED |
| POST | `/api/v1/students/me/skills` | `add_skill` | `StudentSkillController@store` | Yes | STUDENT | `StudentProfileExtensionsParityTest::test_student_can_manage_skills` | MATCHED |
| PUT | `/api/v1/recruiters/me/company` | `update_company` | `RecruiterController@updateCompany` | Yes | RECRUITER | `RecruiterDashboardParityTest::test_update_company` | MATCHED |
| PUT | `/api/v1/recruiters/me/drives/{id}` | `update_drive` | `RecruiterDriveController@update` | Yes | RECRUITER (own company) | `MissingEndpointsParityTest::test_update_recruiter_drive` | MATCHED |
| PUT | `/api/v1/recruiters/me/jobs/{id}` | `update_job` | `RecruiterJobController@update` | Yes | RECRUITER (own company) | `MissingEndpointsParityTest::test_update_recruiter_job` | MATCHED |
| PUT | `/api/v1/skills/{id}` | `update_skill` | `SkillController@update` | Yes | SUPER_ADMIN|PLACEMENT_OFFICER | `MissingEndpointsParityTest::test_update_and_delete_skill` | MATCHED |
| PUT | `/api/v1/students/me` | `update_my_profile` | `StudentController@updateBasicInfo` | Yes | STUDENT | `StudentProfileExtensionsParityTest::test_update_basic_info` | MATCHED |
| PUT | `/api/v1/students/me/academic/{id}` | `update_academic_history` | `StudentAcademicController@update` | Yes | STUDENT | `StudentProfileExtensionsParityTest::test_student_can_manage_academic` | MATCHED |
| PUT | `/api/v1/students/me/certifications/{id}` | `update_certification` | `StudentCertificationController@update` | Yes | STUDENT | `StudentProfileExtensionsParityTest::test_student_can_manage_certifications` | MATCHED |
| PUT | `/api/v1/students/me/projects/{id}` | `update_project` | `StudentProjectController@update` | Yes | STUDENT | `StudentProfileExtensionsParityTest::test_student_can_manage_projects` | MATCHED |
| PUT | `/api/v1/students/me/skills/{id}` | `update_skill` | `StudentSkillController@update` | Yes | STUDENT | `StudentProfileExtensionsParityTest::test_student_can_manage_skills` | MATCHED |
