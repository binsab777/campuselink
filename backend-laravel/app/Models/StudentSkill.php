<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use App\Enums\ProficiencyLevel;
use App\Enums\SkillSource;

class StudentSkill extends Model {
    use HasFactory;
    protected $guarded = ['id'];
    protected $casts = [
        'proficiency_level' => ProficiencyLevel::class,
        'source' => SkillSource::class,
    ];

    public function student() { return $this->belongsTo(Student::class); }
    public function skill() { return $this->belongsTo(Skill::class); }
}