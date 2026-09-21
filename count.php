<?php
$data = json_decode(file_get_contents('fastapi_data_snapshot.json'), true);
foreach ($data as $k => $v) {
    echo $k . ': ' . count($v) . "\n";
}
