<?php
namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Sanctum\HasApiTokens;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class User extends Authenticatable {
    use HasFactory;
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
}
