<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('interviews', function (Blueprint $table) {
            $table->id();
            $table->foreignId('application_id')->constrained()->cascadeOnDelete();
            $table->timestamp('scheduled_start');
            $table->timestamp('scheduled_end');
            $table->string('interview_type');
            $table->float('score')->nullable();
            $table->text('feedback')->nullable();
            $table->string('status')->default('SCHEDULED');
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('interviews'); }
};
