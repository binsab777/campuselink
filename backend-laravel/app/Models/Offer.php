<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use App\Enums\OfferStatus;

class Offer extends Model {
    use HasFactory;
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
}