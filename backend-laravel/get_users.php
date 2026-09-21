<?php
require __DIR__ . '/vendor/autoload.php';
$app = require_once __DIR__ . '/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

$users = \App\Models\User::whereIn('email', ['student1@college.edu', 'recruiter1@comp1.com'])->get();
foreach ($users as $u) {
    $u->password_hash = \Illuminate\Support\Facades\Hash::make('password');
    $u->save();
}
echo "Passwords updated!\n";
