<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use App\Enums\GapSeverity;

class SkillGap extends Model {
    use HasFactory;
    protected $guarded = ['id'];
    protected $casts = [
        'gap_severity' => GapSeverity::class,
        'is_mandatory' => 'boolean',
        'calculated_at' => 'datetime',
    ];

    public function student() { return $this->belongsTo(Student::class); }
    public function job() { return $this->belongsTo(Job::class); }
    public function skill() { return $this->belongsTo(Skill::class); }
}