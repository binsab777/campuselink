<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('skill_gaps', function (Blueprint $table) {
            $table->id();
            $table->foreignId('student_id')->constrained()->cascadeOnDelete();
            $table->foreignId('job_id')->constrained()->cascadeOnDelete();
            $table->foreignId('skill_id')->constrained()->cascadeOnDelete();
            $table->string('gap_severity');
            $table->integer('current_level')->nullable();
            $table->integer('required_level')->nullable();
            $table->boolean('is_mandatory')->default(true);
            $table->string('analysis_version')->default('v1.0');
            $table->text('recommendation')->nullable();
            $table->timestamp('calculated_at')->useCurrent();
            $table->timestamps();
            
            $table->unique(['student_id', 'job_id', 'skill_id']);
        });
    }
    public function down(): void { Schema::dropIfExists('skill_gaps'); }
};
