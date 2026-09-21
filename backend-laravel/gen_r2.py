import os

with open('routes/api.php', 'r') as f:
    r = f.read()

inject_student = """
        Route::get('/me/skills', [\\App\\Http\\Controllers\\Api\\StudentSkillController::class, 'index']);
        Route::get('/me/completeness', [\\App\\Http\\Controllers\\Api\\StudentController::class, 'getCompleteness']);
        Route::get('/me/drives', [\\App\\Http\\Controllers\\Api\\StudentController::class, 'getDrives']);
"""

inject_readiness = """
        Route::get('/me', [\\App\\Http\\Controllers\\Api\\StudentController::class, 'getReadinessDb']);
        Route::get('/students/{id}', [\\App\\Http\\Controllers\\Api\\OfficerController::class, 'getReadinessDb']);
        Route::get('/me/jobs/{id}/skill-gaps', [\\App\\Http\\Controllers\\Api\\JobController::class, 'calculateSkillGap']);
        Route::get('/students/{id}/jobs/{job_id}/skill-gaps', [\\App\\Http\\Controllers\\Api\\OfficerController::class, 'calculateSkillGap']);
"""

r = r.replace("Route::post('/me/skills', [\\App\\Http\\Controllers\\Api\\StudentSkillController::class, 'store']);", inject_student + "\\n        Route::post('/me/skills', [\\App\\Http\\Controllers\\Api\\StudentSkillController::class, 'store']);")

# We will just map the recruiter candidates and dashboard
inject_recruiter = """
        Route::get('/me/dashboard', [\\App\\Http\\Controllers\\Api\\RecruiterCompanyController::class, 'dashboard']);
        Route::get('/candidates/{id}', [\\App\\Http\\Controllers\\Api\\RecruiterCompanyController::class, 'candidate']);
"""
r = r.replace("Route::get('/me/company', [\\App\\Http\\Controllers\\Api\\RecruiterCompanyController::class, 'show']);", inject_recruiter + "\\n        Route::get('/me/company', [\\App\\Http\\Controllers\\Api\\RecruiterCompanyController::class, 'show']);")

with open('routes/api.php', 'w') as f:
    f.write(r)
