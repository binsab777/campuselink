<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class Student extends Model {
    use HasFactory;
    protected $guarded = ['id'];
    protected $casts = [
        'profile_metadata' => 'array',
        'dob' => 'date',
    ];

    public function user() { return $this->belongsTo(User::class); }
    
    public function getResumeUrlAttribute($value) {
        if ($value) {
            return '/api/v1/students/' . $this->id . '/resume/download';
        }
        return null;
    }

    public function academicHistory() { return $this->hasMany(StudentAcademicHistory::class); }
    public function skills() { return $this->hasMany(StudentSkill::class); }
    public function projects() { return $this->hasMany(StudentProject::class); }
    public function certifications() { return $this->hasMany(StudentCertification::class); }
    public function assessments() { return $this->hasMany(StudentAssessment::class); }
    public function applications() { return $this->hasMany(Application::class); }
    public function scores() { return $this->hasMany(StudentScore::class); }
    public function offers() { return $this->hasMany(Offer::class); }
}