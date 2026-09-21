<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class StudentScore extends Model {
    use HasFactory;
    protected $guarded = ['id'];
    protected $casts = [
        'explanation_data' => 'array',
        'calculated_at' => 'datetime',
    ];

    public function student() { return $this->belongsTo(Student::class); }
}