<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class MatchingScore extends Model {
    use HasFactory;
    protected $guarded = ['id'];
    protected $casts = [
        'explanation_data' => 'array',
        'calculated_at' => 'datetime',
    ];

    public function student() { return $this->belongsTo(Student::class); }
    public function job() { return $this->belongsTo(Job::class); }
    public function drive() { return $this->belongsTo(PlacementDrive::class, 'drive_id'); }
}