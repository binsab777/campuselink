<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('applications', function (Blueprint $table) {
            $table->id();
            $table->foreignId('student_id')->constrained()->cascadeOnDelete();
            $table->foreignId('job_id')->constrained()->cascadeOnDelete();
            $table->foreignId('drive_id')->nullable()->constrained('placement_drives')->nullOnDelete();
            $table->string('status')->default('APPLIED')->index();
            $table->timestamp('applied_at')->useCurrent();
            $table->timestamps();
            
            $table->unique(['student_id', 'job_id']);
        });
    }
    public function down(): void { Schema::dropIfExists('applications'); }
};
