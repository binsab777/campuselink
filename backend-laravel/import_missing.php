<?php
require __DIR__ . '/vendor/autoload.php';
$app = require_once __DIR__ . '/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

$data = json_decode(file_get_contents('../fastapi_data_snapshot.json'), true);

function getMeta($item, $key = 'metadata_json') {
    if (!isset($item[$key])) return null;
    return is_array($item[$key]) ? json_encode($item[$key]) : $item[$key];
}

DB::table('student_assessments')->truncate();
foreach ($data['student_assessments'] as $sa) {
    DB::table('student_assessments')->insert([
        'id' => $sa['id'],
        'student_id' => $sa['student_id'],
        'assessment_type' => $sa['assessment_type'],
        'score' => $sa['score'],
        'max_score' => $sa['max_score'],
        'assessment_date' => $sa['assessment_date'] ?? null,
        'metadata_json' => getMeta($sa),
        'created_at' => $sa['created_at'] ?? null,
        'updated_at' => $sa['updated_at'] ?? null,
    ]);
}

DB::table('student_scores')->truncate();
foreach ($data['student_scores'] as $ss) {
    DB::table('student_scores')->insert([
        'id' => $ss['id'],
        'student_id' => $ss['student_id'],
        'score_type' => $ss['score_type'],
        'score_value' => $ss['score_value'],
        'metadata_json' => getMeta($ss),
        'created_at' => $ss['created_at'] ?? null,
        'updated_at' => $ss['updated_at'] ?? null,
    ]);
}

DB::table('offers')->truncate();
foreach ($data['offers'] as $offer) {
    DB::table('offers')->insert([
        'id' => $offer['id'],
        'application_id' => $offer['application_id'],
        'offer_type' => $offer['offer_type'],
        'ctc_value' => $offer['ctc_value'],
        'base_salary' => $offer['base_salary'] ?? null,
        'bonus' => $offer['bonus'] ?? null,
        'stock_options' => $offer['stock_options'] ?? null,
        'status' => $offer['status'],
        'deadline' => $offer['deadline'] ?? null,
        'metadata_json' => getMeta($offer),
        'created_at' => $offer['created_at'] ?? null,
        'updated_at' => $offer['updated_at'] ?? null,
    ]);
}

DB::table('skill_gaps')->truncate();
foreach ($data['skill_gaps'] as $sg) {
    DB::table('skill_gaps')->insert([
        'id' => $sg['id'],
        'student_id' => $sg['student_id'],
        'target_role' => $sg['target_role'],
        'missing_skills' => getMeta($sg, 'missing_skills'),
        'severity' => $sg['severity'],
        'created_at' => $sg['created_at'] ?? null,
        'updated_at' => $sg['updated_at'] ?? null,
    ]);
}

echo "Imported missing tables successfully.\n";
