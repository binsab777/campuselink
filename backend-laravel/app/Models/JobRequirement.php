<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use App\Enums\ProficiencyLevel;

class JobRequirement extends Model {
    use HasFactory;
    protected $guarded = ['id'];
    protected $casts = [
        'required_proficiency' => ProficiencyLevel::class,
        'is_mandatory' => 'boolean',
    ];

    public function job() { return $this->belongsTo(Job::class); }
    public function skill() { return $this->belongsTo(Skill::class); }
}