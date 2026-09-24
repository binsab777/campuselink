<?php
require __DIR__ . '/vendor/autoload.php';
$app = require_once __DIR__ . '/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

$users = \App\Models\User::whereIn('role', ['SUPER_ADMIN', 'PLACEMENT_OFFICER'])->get();
foreach ($users as $u) {
    $u->password_hash = \Illuminate\Support\Facades\Hash::make('password');
    $u->save();
    echo $u->email . " - " . $u->role . "\n";
}
