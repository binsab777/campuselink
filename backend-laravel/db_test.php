<?php
require 'vendor/autoload.php';
$app = require_once 'bootstrap/app.php';
$app->make('Illuminate\Contracts\Console\Kernel')->bootstrap();
$res = \Illuminate\Support\Facades\DB::select("SELECT column_name, is_nullable FROM information_schema.columns WHERE table_name = 'placement_drives'");
print_r($res);
