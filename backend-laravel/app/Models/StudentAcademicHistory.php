<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class StudentAcademicHistory extends Model {
    use HasFactory;
    protected $table = 'student_academic_history';
    protected $guarded = ['id'];

    public function student() { return $this->belongsTo(Student::class); }
}