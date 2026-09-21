<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('students', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->unique()->constrained()->cascadeOnDelete();
            $table->string('student_identifier')->unique();
            $table->string('first_name');
            $table->string('last_name');
            $table->string('branch');
            $table->integer('graduation_year');
            $table->decimal('cgpa', 4, 2)->nullable();
            $table->integer('backlogs_current')->default(0);
            $table->integer('backlogs_history')->default(0);
            $table->string('phone')->nullable();
            $table->date('dob')->nullable();
            $table->string('gender')->nullable();
            $table->string('profile_picture_url')->nullable();
            $table->string('resume_url')->nullable();
            $table->json('profile_metadata')->nullable();
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('students'); }
};
