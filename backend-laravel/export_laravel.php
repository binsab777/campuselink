<?php
require __DIR__.'/vendor/autoload.php';
$app = require_once __DIR__.'/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

use Illuminate\Support\Facades\DB;

$tables = ['users', 'companies', 'skills', 'recruiters', 'students', 'jobs', 'student_academic_history', 'student_certifications', 'student_projects', 'student_skills', 'job_requirements', 'placement_drives', 'applications', 'drive_candidates'];

$data = [];
foreach ($tables as $table) {
    $data[$table] = DB::table($table)->get()->toArray();
}

file_put_contents('../laravel_data_snapshot.json', json_encode($data, JSON_PRETTY_PRINT));
echo "Exported Laravel data.\n";
