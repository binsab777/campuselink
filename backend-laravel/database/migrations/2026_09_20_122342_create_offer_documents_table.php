<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('offer_documents', function (Blueprint $table) {
            $table->id();
            $table->foreignId('offer_id')->constrained()->cascadeOnDelete();
            $table->string('document_type');
            $table->string('file_url');
            $table->string('verification_status')->default('PENDING');
            $table->timestamp('verified_at')->nullable();
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('offer_documents'); }
};
