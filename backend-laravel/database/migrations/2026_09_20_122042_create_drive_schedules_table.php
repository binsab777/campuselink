<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('drive_schedules', function (Blueprint $table) {
            $table->id();
            $table->foreignId('drive_id')->constrained('placement_drives')->cascadeOnDelete();
            $table->foreignId('student_id')->constrained()->cascadeOnDelete();
            $table->string('interviewer_ref')->nullable();
            $table->string('venue')->nullable();
            $table->timestamp('start_time');
            $table->timestamp('end_time');
            $table->string('status')->default('SCHEDULED');
            $table->timestamps();
            
            $table->unique(['drive_id', 'student_id', 'start_time'], 'uq_drive_schedule');
        });
    }
    public function down(): void { Schema::dropIfExists('drive_schedules'); }
};
