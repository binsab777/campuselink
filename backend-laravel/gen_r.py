import re

with open('routes/api.php', 'r') as f:
    r = f.read()

# Add missing student routes (Academic, Skills, Projects, Certifications)
# Note: I already added some to `routes/api.php` manually in the previous turn, but let's just append the missing ones.
r = r.replace("Route::post('/me/skills',", "Route::get('/me/certifications', [\\App\\Http\\Controllers\\Api\\StudentCertificationController::class, 'index']);\\n        Route::post('/me/certifications', [\\App\\Http\\Controllers\\Api\\StudentCertificationController::class, 'store']);\\n        Route::put('/me/certifications/{id}', [\\App\\Http\\Controllers\\Api\\StudentCertificationController::class, 'update']);\\n        Route::delete('/me/certifications/{id}', [\\App\\Http\\Controllers\\Api\\StudentCertificationController::class, 'destroy']);\\n        Route::get('/me/projects', [\\App\\Http\\Controllers\\Api\\StudentProjectController::class, 'index']);\\n        Route::put('/me/projects/{id}', [\\App\\Http\\Controllers\\Api\\StudentProjectController::class, 'update']);\\n        Route::put('/me/skills/{id}', [\\App\\Http\\Controllers\\Api\\StudentSkillController::class, 'update']);\\n        Route::post('/me/academic', [\\App\\Http\\Controllers\\Api\\StudentAcademicController::class, 'store']);\\n        Route::put('/me/academic/{id}', [\\App\\Http\\Controllers\\Api\\StudentAcademicController::class, 'update']);\\n        Route::delete('/me/academic/{id}', [\\App\\Http\\Controllers\\Api\\StudentAcademicController::class, 'destroy']);\\n        Route::post('/me/skills',")

# Add recruiter routes
recruiter_routes = """
    Route::middleware(['auth:sanctum', 'role:RECRUITER'])->group(function () {
        Route::get('/me/company', [\\App\\Http\\Controllers\\Api\\RecruiterCompanyController::class, 'show']);
        Route::put('/me/company', [\\App\\Http\\Controllers\\Api\\RecruiterCompanyController::class, 'update']);
        
        Route::get('/me/jobs', [\\App\\Http\\Controllers\\Api\\RecruiterJobController::class, 'index']);
        Route::post('/me/jobs', [\\App\\Http\\Controllers\\Api\\RecruiterJobController::class, 'store']);
        Route::get('/me/jobs/{id}', [\\App\\Http\\Controllers\\Api\\RecruiterJobController::class, 'show']);
        Route::put('/me/jobs/{id}', [\\App\\Http\\Controllers\\Api\\RecruiterJobController::class, 'update']);
        Route::delete('/me/jobs/{id}', [\\App\\Http\\Controllers\\Api\\RecruiterJobController::class, 'destroy']);
        
        Route::get('/me/drives', [\\App\\Http\\Controllers\\Api\\RecruiterDriveController::class, 'index']);
        Route::post('/me/drives', [\\App\\Http\\Controllers\\Api\\RecruiterDriveController::class, 'store']);
        Route::put('/me/drives/{id}', [\\App\\Http\\Controllers\\Api\\RecruiterDriveController::class, 'update']);
    });
"""

# Add officer routes and skill routes
officer_routes = """
    Route::middleware(['auth:sanctum', 'role:PLACEMENT_OFFICER,SUPER_ADMIN'])->prefix('officer')->group(function () {
        Route::get('/students', [\\App\\Http\\Controllers\\Api\\OfficerController::class, 'getStudents']);
        Route::get('/students/{id}', [\\App\\Http\\Controllers\\Api\\OfficerController::class, 'getStudent']);
        Route::get('/companies', [\\App\\Http\\Controllers\\Api\\OfficerController::class, 'getCompanies']);
        Route::post('/companies', [\\App\\Http\\Controllers\\Api\\OfficerController::class, 'storeCompany']);
    });

    Route::middleware(['auth:sanctum', 'role:SUPER_ADMIN'])->prefix('skills')->group(function () {
        Route::get('/', [\\App\\Http\\Controllers\\Api\\SkillController::class, 'index']);
        Route::post('/', [\\App\\Http\\Controllers\\Api\\SkillController::class, 'store']);
        Route::put('/{id}', [\\App\\Http\\Controllers\\Api\\SkillController::class, 'update']);
        Route::delete('/{id}', [\\App\\Http\\Controllers\\Api\\SkillController::class, 'destroy']);
    });
"""

r = r.replace("Route::middleware(['auth:sanctum', 'role:SUPER_ADMIN'])->prefix('admin')->group(function () {", recruiter_routes + "\\n" + officer_routes + "\\n    Route::middleware(['auth:sanctum', 'role:SUPER_ADMIN'])->prefix('admin')->group(function () {")

# Remove extra escape slashes inside python script
r = r.replace('\\\\', '\\')

with open('routes/api.php', 'w') as f:
    f.write(r)
