<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('student_assessments', function (Blueprint $table) {
            $table->id();
            $table->foreignId('student_id')->constrained()->cascadeOnDelete();
            $table->string('assessment_type');
            $table->float('score');
            $table->float('max_score');
            $table->timestamp('assessment_date');
            $table->json('metadata_json')->nullable();
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('student_assessments'); }
};
