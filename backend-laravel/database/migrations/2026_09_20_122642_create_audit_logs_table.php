<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('audit_logs', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->nullable()->constrained()->nullOnDelete();
            $table->string('entity_type');
            $table->integer('entity_id');
            $table->string('action');
            $table->json('old_values')->nullable();
            $table->json('new_values')->nullable();
            $table->timestamp('timestamp')->useCurrent();
            $table->json('request_metadata')->nullable();
        });
    }
    public function down(): void { Schema::dropIfExists('audit_logs'); }
};
