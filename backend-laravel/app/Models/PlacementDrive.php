<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use App\Enums\DriveStatus;

class PlacementDrive extends Model {
    use HasFactory;
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
}