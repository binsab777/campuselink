<?php
require 'vendor/autoload.php';
$app = require_once 'bootstrap/app.php';
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();

$u = App\Models\User::find(48);
if ($u) {
    echo json_encode([
        'user' => $u,
        'recruiter' => $u->recruiterProfile,
        'company' => $u->recruiterProfile ? $u->recruiterProfile->company : null
    ], JSON_PRETTY_PRINT);
} else {
    echo "User not found";
}
