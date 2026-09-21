import os

model_dir = "app/Models/"
os.makedirs(model_dir, exist_ok=True)

models = {
    "User": """<?php
namespace App\\Models;

use Illuminate\\Foundation\\Auth\\User as Authenticatable;
use Illuminate\\Notifications\\Notifiable;
use Laravel\\Sanctum\\HasApiTokens;

class User extends Authenticatable {
    use HasApiTokens, Notifiable;

    protected $fillable = ['email', 'password_hash', 'role', 'is_active'];
    protected $hidden = ['password_hash'];
    
    // In Laravel, the Auth component looks for 'password'
    public function getAuthPassword() {
        return $this->password_hash;
    }

    public function studentProfile() { return $this->hasOne(Student::class); }
    public function recruiterProfile() { return $this->hasOne(Recruiter::class); }
    public function auditLogs() { return $this->hasMany(AuditLog::class); }
}""",
    
    "Student": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;

class Student extends Model {
    protected $guarded = ['id'];
    protected $casts = [
        'profile_metadata' => 'array',
        'dob' => 'date',
    ];

    public function user() { return $this->belongsTo(User::class); }
    public function academicHistory() { return $this->hasMany(StudentAcademicHistory::class); }
    public function skills() { return $this->hasMany(StudentSkill::class); }
    public function projects() { return $this->hasMany(StudentProject::class); }
    public function certifications() { return $this->hasMany(StudentCertification::class); }
    public function assessments() { return $this->hasMany(StudentAssessment::class); }
    public function applications() { return $this->hasMany(Application::class); }
    public function scores() { return $this->hasMany(StudentScore::class); }
    public function offers() { return $this->hasMany(Offer::class); }
}""",

    "Company": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;

class Company extends Model {
    protected $guarded = ['id'];
    protected $casts = [
        'metadata_json' => 'array',
    ];

    public function recruiters() { return $this->hasMany(Recruiter::class); }
    public function jobs() { return $this->hasMany(Job::class); }
    public function drives() { return $this->hasMany(PlacementDrive::class); }
}""",

    "Recruiter": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;

class Recruiter extends Model {
    protected $guarded = ['id'];

    public function user() { return $this->belongsTo(User::class); }
    public function company() { return $this->belongsTo(Company::class); }
    public function jobs() { return $this->hasMany(Job::class); }
}""",

    "Skill": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;

class Skill extends Model {
    protected $guarded = ['id'];
}""",

    "StudentSkill": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;
use App\\Enums\\ProficiencyLevel;
use App\\Enums\\SkillSource;

class StudentSkill extends Model {
    protected $guarded = ['id'];
    protected $casts = [
        'proficiency_level' => ProficiencyLevel::class,
        'source' => SkillSource::class,
    ];

    public function student() { return $this->belongsTo(Student::class); }
    public function skill() { return $this->belongsTo(Skill::class); }
}""",

    "StudentProject": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;

class StudentProject extends Model {
    protected $guarded = ['id'];

    public function student() { return $this->belongsTo(Student::class); }
}""",

    "StudentCertification": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;

class StudentCertification extends Model {
    protected $guarded = ['id'];
    protected $casts = [
        'issue_date' => 'datetime',
        'expiry_date' => 'datetime',
    ];

    public function student() { return $this->belongsTo(Student::class); }
}""",

    "StudentAcademicHistory": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;

class StudentAcademicHistory extends Model {
    protected $table = 'student_academic_history';
    protected $guarded = ['id'];

    public function student() { return $this->belongsTo(Student::class); }
}""",

    "StudentAssessment": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;

class StudentAssessment extends Model {
    protected $guarded = ['id'];
    protected $casts = [
        'assessment_date' => 'datetime',
        'metadata_json' => 'array',
    ];

    public function student() { return $this->belongsTo(Student::class); }
}""",

    "Job": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;
use App\\Enums\\JobStatus;

class Job extends Model {
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
}""",

    "JobRequirement": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;
use App\\Enums\\ProficiencyLevel;

class JobRequirement extends Model {
    protected $guarded = ['id'];
    protected $casts = [
        'required_proficiency' => ProficiencyLevel::class,
        'is_mandatory' => 'boolean',
    ];

    public function job() { return $this->belongsTo(Job::class); }
    public function skill() { return $this->belongsTo(Skill::class); }
}""",

    "PlacementDrive": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;
use App\\Enums\\DriveStatus;

class PlacementDrive extends Model {
    protected $guarded = ['id'];
    protected $casts = [
        'registration_deadline' => 'datetime',
        'start_date' => 'datetime',
        'end_date' => 'datetime',
        'status' => DriveStatus::class,
        'metadata_json' => 'array',
    ];

    public function company() { return $this->belongsTo(Company::class); }
    public function job() { return $this->belongsTo(Job::class); }
    public function candidates() { return $this->hasMany(DriveCandidate::class, 'drive_id'); }
}""",

    "DriveCandidate": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;

class DriveCandidate extends Model {
    protected $guarded = ['id'];
    protected $casts = [
        'eligibility_details' => 'array',
        'registered_at' => 'datetime',
    ];

    public function drive() { return $this->belongsTo(PlacementDrive::class, 'drive_id'); }
    public function student() { return $this->belongsTo(Student::class); }
}""",

    "Application": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;
use App\\Enums\\ApplicationStatus;

class Application extends Model {
    protected $guarded = ['id'];
    protected $casts = [
        'applied_at' => 'datetime',
        'status' => ApplicationStatus::class,
    ];

    public function student() { return $this->belongsTo(Student::class); }
    public function job() { return $this->belongsTo(Job::class); }
    public function drive() { return $this->belongsTo(PlacementDrive::class, 'drive_id'); }
    public function interviews() { return $this->hasMany(Interview::class); }
}""",

    "Interview": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;

class Interview extends Model {
    protected $guarded = ['id'];
    protected $casts = [
        'scheduled_start' => 'datetime',
        'scheduled_end' => 'datetime',
    ];

    public function application() { return $this->belongsTo(Application::class); }
}""",

    "Offer": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;
use App\\Enums\\OfferStatus;

class Offer extends Model {
    protected $guarded = ['id'];
    protected $casts = [
        'offer_date' => 'datetime',
        'acceptance_date' => 'datetime',
        'joining_date' => 'datetime',
        'status' => OfferStatus::class,
    ];

    public function student() { return $this->belongsTo(Student::class); }
    public function recruiter() { return $this->belongsTo(Recruiter::class); }
    public function job() { return $this->belongsTo(Job::class); }
    public function application() { return $this->belongsTo(Application::class); }
    public function documents() { return $this->hasMany(OfferDocument::class); }
}""",

    "OfferDocument": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;

class OfferDocument extends Model {
    protected $guarded = ['id'];
    protected $casts = [
        'verified_at' => 'datetime',
    ];

    public function offer() { return $this->belongsTo(Offer::class); }
}""",

    "StudentScore": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;

class StudentScore extends Model {
    protected $guarded = ['id'];
    protected $casts = [
        'explanation_data' => 'array',
        'calculated_at' => 'datetime',
    ];

    public function student() { return $this->belongsTo(Student::class); }
}""",

    "SkillGap": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;
use App\\Enums\\GapSeverity;

class SkillGap extends Model {
    protected $guarded = ['id'];
    protected $casts = [
        'gap_severity' => GapSeverity::class,
        'is_mandatory' => 'boolean',
        'calculated_at' => 'datetime',
    ];

    public function student() { return $this->belongsTo(Student::class); }
    public function job() { return $this->belongsTo(Job::class); }
    public function skill() { return $this->belongsTo(Skill::class); }
}""",

    "MatchingScore": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;

class MatchingScore extends Model {
    protected $guarded = ['id'];
    protected $casts = [
        'explanation_data' => 'array',
        'calculated_at' => 'datetime',
    ];

    public function student() { return $this->belongsTo(Student::class); }
    public function job() { return $this->belongsTo(Job::class); }
    public function drive() { return $this->belongsTo(PlacementDrive::class, 'drive_id'); }
}""",

    "AuditLog": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;

class AuditLog extends Model {
    public $timestamps = false;
    protected $guarded = ['id'];
    protected $casts = [
        'old_values' => 'array',
        'new_values' => 'array',
        'request_metadata' => 'array',
        'timestamp' => 'datetime',
    ];

    public function user() { return $this->belongsTo(User::class); }
}""",

    "Notification": """<?php
namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;

class Notification extends Model {
    protected $guarded = ['id'];
    protected $casts = [
        'scheduled_at' => 'datetime',
        'sent_at' => 'datetime',
        'read_at' => 'datetime',
        'metadata_json' => 'array',
    ];

    public function user() { return $this->belongsTo(User::class); }
}"""
}

for name, content in models.items():
    filepath = os.path.join(model_dir, f"{name}.php")
    with open(filepath, 'w') as f:
        f.write(content)

print(f"Generated {len(models)} Eloquent Models.")
