<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class StudentCertification extends Model {
    use HasFactory;
    protected $guarded = ['id'];
    protected $casts = [
        'issue_date' => 'datetime',
        'expiry_date' => 'datetime',
    ];

    public function student() { return $this->belongsTo(Student::class); }
}