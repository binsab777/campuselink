<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('student_skills', function (Blueprint $table) {
            $table->id();
            $table->foreignId('student_id')->constrained()->cascadeOnDelete();
            $table->foreignId('skill_id')->constrained()->cascadeOnDelete();
            $table->string('proficiency_level');
            $table->integer('months_experience')->default(0);
            $table->string('source')->nullable();
            $table->timestamps();
            
            $table->unique(['student_id', 'skill_id']);
        });
    }
    public function down(): void { Schema::dropIfExists('student_skills'); }
};
