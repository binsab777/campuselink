<?php
require __DIR__ . '/vendor/autoload.php';
$app = require_once __DIR__ . '/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

$fastapi = json_decode(file_get_contents('../fastapi_data_snapshot.json'), true);

$tables = [
    'users' => 'users',
    'students' => 'students',
    'student_academic_history' => 'student_academic_history',
    'skills' => 'skills',
    'student_skills' => 'student_skills',
    'student_projects' => 'student_projects',
    'student_certifications' => 'student_certifications',
    'companies' => 'companies',
    'recruiters' => 'recruiters',
    'jobs' => 'jobs',
    'job_requirements' => 'job_requirements',
    'applications' => 'applications',
    'placement_drives' => 'placement_drives',
    'drive_candidates' => 'drive_candidates',
];

$all_matched = true;
$output = "";

foreach ($tables as $fk => $lk) {
    $fastapi_count = count($fastapi[$fk] ?? []);
    $laravel_count = DB::table($lk)->count();
    
    if ($fastapi_count === $laravel_count) {
        $output .= "[OK] $fk: $fastapi_count == $laravel_count\n";
    } else {
        $output .= "[FAIL] $fk: FastAPI=$fastapi_count, Laravel=$laravel_count\n";
        $all_matched = false;
    }
}

echo $output;
if ($all_matched) {
    echo "\nPARITY VERIFIED FULLY\n";
} else {
    echo "\nPARITY FAILED\n";
}
