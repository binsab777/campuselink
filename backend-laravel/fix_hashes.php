<?php
require 'vendor/autoload.php';
$app = require_once 'bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

use Illuminate\Support\Facades\DB;

$affected = DB::statement("UPDATE users SET password_hash = REPLACE(password_hash, '$2b$', '$2y$')");
echo "Updated hashes. Affected rows: $affected\n";
