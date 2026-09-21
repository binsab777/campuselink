<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('student_scores', function (Blueprint $table) {
            $table->id();
            $table->foreignId('student_id')->constrained()->cascadeOnDelete();
            $table->string('score_type');
            $table->float('score_value');
            $table->string('model_version')->nullable();
            $table->json('explanation_data')->nullable();
            $table->timestamp('calculated_at')->useCurrent();
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('student_scores'); }
};
