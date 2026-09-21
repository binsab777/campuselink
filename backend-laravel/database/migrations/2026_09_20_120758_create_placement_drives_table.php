<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('placement_drives', function (Blueprint $table) {
            $table->id();
            $table->foreignId('company_id')->constrained()->cascadeOnDelete();
            $table->foreignId('job_id')->constrained()->cascadeOnDelete();
            $table->string('name')->index();
            $table->string('drive_type')->nullable();
            $table->timestamp('registration_deadline')->nullable();
            $table->timestamp('start_date')->nullable();
            $table->timestamp('end_date')->nullable();
            $table->integer('capacity')->nullable();
            $table->string('status')->default('DRAFT');
            $table->json('metadata_json')->nullable();
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('placement_drives'); }
};
