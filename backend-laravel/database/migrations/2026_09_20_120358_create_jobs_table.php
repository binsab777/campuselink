<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('jobs', function (Blueprint $table) {
            $table->id();
            $table->foreignId('company_id')->constrained()->cascadeOnDelete();
            $table->foreignId('recruiter_id')->nullable()->constrained()->nullOnDelete();
            $table->string('title')->index();
            $table->text('description');
            $table->string('employment_type');
            $table->string('location')->nullable();
            $table->string('remote_type')->nullable();
            $table->string('salary_range')->nullable();
            $table->string('experience_requirement')->nullable();
            $table->timestamp('application_deadline')->nullable();
            $table->integer('openings')->nullable();
            $table->string('job_code')->nullable();
            $table->json('job_description_json')->nullable();
            $table->json('eligibility_config')->nullable();
            $table->string('status')->default('DRAFT')->index();
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('jobs'); }
};
