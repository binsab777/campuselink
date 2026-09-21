<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class StudentProject extends Model {
    use HasFactory;
    protected $guarded = ['id'];
    protected $casts = ['technologies' => 'array'];

    public function student() { return $this->belongsTo(Student::class); }
}
