<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class Company extends Model {
    use HasFactory;
    protected $guarded = ['id'];
    protected $casts = [
        'metadata_json' => 'array',
    ];

    public function recruiters() { return $this->hasMany(Recruiter::class); }
    public function jobs() { return $this->hasMany(Job::class); }
    public function drives() { return $this->hasMany(PlacementDrive::class); }
}