import os
import datetime

migration_dir = "database/migrations/"
os.makedirs(migration_dir, exist_ok=True)

def get_prefix(idx):
    base_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=idx + 20)
    return base_time.strftime("%Y_%m_%d_%H%M%S")

migrations = [
    ("create_student_assessments_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

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
"""),

    ("create_drive_schedules_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('drive_schedules', function (Blueprint $table) {
            $table->id();
            $table->foreignId('drive_id')->constrained('placement_drives')->cascadeOnDelete();
            $table->foreignId('student_id')->constrained()->cascadeOnDelete();
            $table->string('interviewer_ref')->nullable();
            $table->string('venue')->nullable();
            $table->timestamp('start_time');
            $table->timestamp('end_time');
            $table->string('status')->default('SCHEDULED');
            $table->timestamps();
            
            $table->unique(['drive_id', 'student_id', 'start_time'], 'uq_drive_schedule');
        });
    }
    public function down(): void { Schema::dropIfExists('drive_schedules'); }
};
"""),

    ("create_interviews_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

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
"""),

    ("create_offers_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

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
"""),

    ("create_offer_documents_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

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
"""),

    ("create_notifications_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('notifications', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->string('notification_type');
            $table->string('title');
            $table->text('message');
            $table->string('channel')->default('IN_APP');
            $table->string('status')->default('PENDING');
            $table->timestamp('scheduled_at')->nullable();
            $table->timestamp('sent_at')->nullable();
            $table->timestamp('read_at')->nullable();
            $table->json('metadata_json')->nullable();
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('notifications'); }
};
"""),

    ("create_matching_scores_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('matching_scores', function (Blueprint $table) {
            $table->id();
            $table->foreignId('student_id')->constrained()->cascadeOnDelete();
            $table->foreignId('job_id')->constrained()->cascadeOnDelete();
            $table->foreignId('drive_id')->nullable()->constrained('placement_drives')->nullOnDelete();
            $table->float('eligibility_score')->nullable();
            $table->float('skill_similarity_score')->nullable();
            $table->float('project_relevance_score')->nullable();
            $table->float('academic_score')->nullable();
            $table->float('interview_score')->nullable();
            $table->float('final_score');
            $table->string('model_version')->nullable();
            $table->json('explanation_data')->nullable();
            $table->timestamp('calculated_at')->useCurrent();
            $table->timestamps();
            
            $table->unique(['student_id', 'job_id', 'drive_id'], 'uq_match_score');
        });
    }
    public function down(): void { Schema::dropIfExists('matching_scores'); }
};
"""),

    ("create_audit_logs_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

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
"""),
]

for idx, (name, content) in enumerate(migrations):
    filename = f"{get_prefix(idx)}_{name}.php"
    filepath = os.path.join(migration_dir, filename)
    with open(filepath, 'w') as f:
        f.write(content)

print(f"Generated {len(migrations)} tertiary migrations.")
