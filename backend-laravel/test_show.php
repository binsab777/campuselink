<?php
require __DIR__ . '/vendor/autoload.php';
$app = require_once __DIR__ . '/bootstrap/app.php';
$kernel = $app->make(Illuminate\Contracts\Console\Kernel::class);
$kernel->bootstrap();

$r = Illuminate\Http\Request::create('/api/v1/admin/users/5', 'GET');
$controller = app(\App\Http\Controllers\Api\AdminController::class);
echo $controller->show($r, 5)->getContent();
