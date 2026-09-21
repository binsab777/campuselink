<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('drive_candidates', function (Blueprint $table) {
            $table->id();
            $table->foreignId('drive_id')->constrained('placement_drives')->cascadeOnDelete();
            $table->foreignId('student_id')->constrained()->cascadeOnDelete();
            $table->string('status')->default('REGISTERED');
            $table->float('eligibility_score')->nullable();
            $table->json('eligibility_details')->nullable();
            $table->timestamp('registered_at')->useCurrent();
            $table->timestamps();
            
            $table->unique(['drive_id', 'student_id']);
        });
    }
    public function down(): void { Schema::dropIfExists('drive_candidates'); }
};
