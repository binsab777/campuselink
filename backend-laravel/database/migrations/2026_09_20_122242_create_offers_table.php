<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('offers', function (Blueprint $table) {
            $table->id();
            $table->foreignId('student_id')->constrained()->cascadeOnDelete();
            $table->foreignId('recruiter_id')->constrained()->cascadeOnDelete();
            $table->foreignId('job_id')->constrained()->cascadeOnDelete();
            $table->foreignId('application_id')->nullable()->constrained()->nullOnDelete();
            $table->string('status')->default('PENDING')->index();
            $table->float('ctc');
            $table->timestamp('offer_date');
            $table->timestamp('acceptance_date')->nullable();
            $table->timestamp('joining_date')->nullable();
            $table->text('deferral_info')->nullable();
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('offers'); }
};
