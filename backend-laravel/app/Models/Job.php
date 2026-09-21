<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use App\Enums\JobStatus;

class Job extends Model {
    use HasFactory;
    protected $guarded = ['id'];
    protected $casts = [
        'application_deadline' => 'datetime',
        'job_description_json' => 'array',
        'eligibility_config' => 'array',
        'status' => JobStatus::class,
    ];

    public function company() { return $this->belongsTo(Company::class); }
    public function recruiter() { return $this->belongsTo(Recruiter::class); }
    public function requirements() { return $this->hasMany(JobRequirement::class); }
    public function applications() { return $this->hasMany(Application::class); }
}