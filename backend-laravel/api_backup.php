<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\StudentController;
use App\Http\Controllers\Api\JobController;
use App\Http\Controllers\Api\DriveController;

Route::prefix('v1')->group(function () {
    Route::prefix('auth')->group(function () {
        Route::post('/register', [AuthController::class, 'register']);
        Route::post('/login', [AuthController::class, 'login']);
        
        Route::middleware('auth:sanctum')->group(function () {
            Route::get('/me', [AuthController::class, 'me']);
        });
    });

    Route::middleware(['auth:sanctum', 'role:STUDENT'])->prefix('students')->group(function () {
        Route::get('/me', [StudentController::class, 'getProfile']);
        Route::get('/me/full', [StudentController::class, 'getFullProfile']);
        Route::put('/me', [StudentController::class, 'updateBasicInfo']);
        Route::get('/me/academic', [StudentController::class, 'getAcademicHistory']);
        Route::post('/me/recalculate', [StudentController::class, 'getReadiness']); 
    });

    Route::middleware('auth:sanctum')->group(function () {
        Route::get('/jobs', [JobController::class, 'index']);
        Route::get('/jobs/{job}', [JobController::class, 'show']);
        Route::get('/jobs/{job}/eligibility', [JobController::class, 'checkEligibility']);
        Route::get('/jobs/{job}/skill-gaps', [JobController::class, 'calculateSkillGap']);
        Route::get('/drives', [DriveController::class, 'index']);
    });
});

use App\Http\Controllers\Api\StudentResumeController;
use App\Http\Controllers\Api\AdminController;
Route::middleware(['auth:sanctum', 'role:STUDENT'])->group(function () {
Route::post('/students/me/resume', [StudentResumeController::class, 'upload']);
});
Route::middleware(['auth:sanctum', 'role:SUPER_ADMIN'])->prefix('admin')->group(function () {
Route::get('/users', [AdminController::class, 'index']);
Route::put('/users/{user}/activate', [AdminController::class, 'activate']);
Route::put('/users/{user}/deactivate', [AdminController::class, 'deactivate']);
});
