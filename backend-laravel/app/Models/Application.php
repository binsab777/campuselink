<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use App\Enums\ApplicationStatus;

class Application extends Model {
    use HasFactory;
    protected $guarded = ['id'];
    protected $casts = [
        'applied_at' => 'datetime',
        'status' => ApplicationStatus::class,
    ];

    public function student() { return $this->belongsTo(Student::class); }
    public function job() { return $this->belongsTo(Job::class); }
    public function drive() { return $this->belongsTo(PlacementDrive::class, 'drive_id'); }
    public function interviews() { return $this->hasMany(Interview::class); }
}