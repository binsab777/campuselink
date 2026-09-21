<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class AuditLog extends Model {
    use HasFactory;
    public $timestamps = false;
    protected $guarded = ['id'];
    protected $casts = [
        'old_values' => 'array',
        'new_values' => 'array',
        'request_metadata' => 'array',
        'timestamp' => 'datetime',
    ];

    public function user() { return $this->belongsTo(User::class); }
}