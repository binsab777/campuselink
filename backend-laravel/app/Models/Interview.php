<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class Interview extends Model {
    use HasFactory;
    protected $guarded = ['id'];
    protected $casts = [
        'scheduled_start' => 'datetime',
        'scheduled_end' => 'datetime',
    ];

    public function application() { return $this->belongsTo(Application::class); }
}