<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class Skill extends Model {
    use HasFactory;
    protected $guarded = ['id'];

    public function studentSkills() {
        return $this->hasMany(StudentSkill::class, 'skill_id');
    }

    public function jobRequirements() {
        return $this->hasMany(JobRequirement::class, 'skill_id');
    }
}