<?php
require __DIR__ . '/vendor/autoload.php';
$app = require_once __DIR__ . '/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

$fastapi = json_decode(file_get_contents('../fastapi_data_snapshot.json'), true);

$tables = [
    'users', 'companies', 'skills', 'recruiters', 'students', 'jobs', 
    'student_academic_history', 'student_assessments', 'student_certifications', 
    'student_projects', 'student_scores', 'student_skills', 'job_requirements', 
    'placement_drives', 'applications', 'drive_candidates', 'offers', 'skill_gaps'
];

$all_matched = true;

foreach ($tables as $table) {
    $fastapi_count = count($fastapi[$table] ?? []);
    $laravel_count = DB::table($table)->count();
    
    if ($fastapi_count === $laravel_count) {
        echo "[OK] $table: $fastapi_count == $laravel_count\n";
    } else {
        echo "[FAIL] $table: FastAPI=$fastapi_count, Laravel=$laravel_count\n";
        $all_matched = false;
    }
}

// Check some specific records to ensure fields/IDs match
$first_user_fastapi = $fastapi['users'][0] ?? null;
$first_user_laravel = DB::table('users')->where('id', $first_user_fastapi['id'])->first();

if ($first_user_fastapi['email'] === $first_user_laravel->email && $first_user_fastapi['role'] === $first_user_laravel->role) {
    echo "[OK] Users fields match for ID {$first_user_fastapi['id']}\n";
} else {
    echo "[FAIL] Users fields mismatch\n";
    $all_matched = false;
}

$first_student_fastapi = $fastapi['students'][0] ?? null;
$first_student_laravel = DB::table('students')->where('id', $first_student_fastapi['id'])->first();
if ($first_student_fastapi['first_name'] === $first_student_laravel->first_name && (float)$first_student_fastapi['cgpa'] === (float)$first_student_laravel->cgpa) {
    echo "[OK] Students fields match for ID {$first_student_fastapi['id']}\n";
} else {
    echo "[FAIL] Students fields mismatch\n";
    $all_matched = false;
}

if ($all_matched) {
    echo "\nPARITY VERIFIED FULLY\n";
} else {
    echo "\nPARITY FAILED\n";
}
