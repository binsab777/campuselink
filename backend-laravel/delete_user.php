<?php
require 'vendor/autoload.php';
$app = require_once 'bootstrap/app.php';
$app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();

$u = App\Models\User::find(48);
if ($u) {
    if ($u->recruiterProfile) {
        $company = $u->recruiterProfile->company;
        $u->recruiterProfile->delete();
        if ($company) {
            $company->delete();
        }
    }
    $u->delete();
    echo "Deleted user 48 and associated recruiter/company.\n";
} else {
    echo "User 48 not found.\n";
}
