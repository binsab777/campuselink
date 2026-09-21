<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class Notification extends Model {
    use HasFactory;
    protected $guarded = ['id'];
    protected $casts = [
        'scheduled_at' => 'datetime',
        'sent_at' => 'datetime',
        'read_at' => 'datetime',
        'metadata_json' => 'array',
    ];

    public function user() { return $this->belongsTo(User::class); }
}