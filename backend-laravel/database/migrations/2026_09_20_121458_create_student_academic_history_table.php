<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('student_academic_history', function (Blueprint $table) {
            $table->id();
            $table->foreignId('student_id')->constrained('students')->cascadeOnDelete();
            $table->string('qualification');
            $table->string('institution');
            $table->string('specialization')->nullable();
            $table->integer('start_year')->nullable();
            $table->integer('end_year')->nullable();
            $table->float('score_value');
            $table->string('score_type');
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('student_academic_history'); }
};
