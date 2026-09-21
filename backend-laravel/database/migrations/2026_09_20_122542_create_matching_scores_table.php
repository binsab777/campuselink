<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('matching_scores', function (Blueprint $table) {
            $table->id();
            $table->foreignId('student_id')->constrained()->cascadeOnDelete();
            $table->foreignId('job_id')->constrained()->cascadeOnDelete();
            $table->foreignId('drive_id')->nullable()->constrained('placement_drives')->nullOnDelete();
            $table->float('eligibility_score')->nullable();
            $table->float('skill_similarity_score')->nullable();
            $table->float('project_relevance_score')->nullable();
            $table->float('academic_score')->nullable();
            $table->float('interview_score')->nullable();
            $table->float('final_score');
            $table->string('model_version')->nullable();
            $table->json('explanation_data')->nullable();
            $table->timestamp('calculated_at')->useCurrent();
            $table->timestamps();
            
            $table->unique(['student_id', 'job_id', 'drive_id'], 'uq_match_score');
        });
    }
    public function down(): void { Schema::dropIfExists('matching_scores'); }
};
