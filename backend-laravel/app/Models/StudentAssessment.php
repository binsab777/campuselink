<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class StudentAssessment extends Model {
    use HasFactory;
    protected $guarded = ['id'];
    protected $casts = [
        'assessment_date' => 'datetime',
        'metadata_json' => 'array',
    ];

    public function student() { return $this->belongsTo(Student::class); }
}