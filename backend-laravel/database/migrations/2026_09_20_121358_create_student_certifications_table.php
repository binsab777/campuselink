<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('student_certifications', function (Blueprint $table) {
            $table->id();
            $table->foreignId('student_id')->constrained()->cascadeOnDelete();
            $table->string('name');
            $table->string('issuing_org');
            $table->timestamp('issue_date')->nullable();
            $table->timestamp('expiry_date')->nullable();
            $table->string('credential_id')->nullable();
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('student_certifications'); }
};
