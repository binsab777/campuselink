import os
import datetime

migration_dir = "database/migrations/"
os.makedirs(migration_dir, exist_ok=True)

def get_prefix(idx):
    base_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=idx + 10)
    return base_time.strftime("%Y_%m_%d_%H%M%S")

migrations = [
    ("create_placement_drives_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

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
"""),

    ("create_drive_candidates_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('drive_candidates', function (Blueprint $table) {
            $table->id();
            $table->foreignId('drive_id')->constrained('placement_drives')->cascadeOnDelete();
            $table->foreignId('student_id')->constrained()->cascadeOnDelete();
            $table->string('status')->default('REGISTERED');
            $table->float('eligibility_score')->nullable();
            $table->json('eligibility_details')->nullable();
            $table->timestamp('registered_at')->useCurrent();
            $table->timestamps();
            
            $table->unique(['drive_id', 'student_id']);
        });
    }
    public function down(): void { Schema::dropIfExists('drive_candidates'); }
};
"""),

    ("create_applications_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('applications', function (Blueprint $table) {
            $table->id();
            $table->foreignId('student_id')->constrained()->cascadeOnDelete();
            $table->foreignId('job_id')->constrained()->cascadeOnDelete();
            $table->foreignId('drive_id')->nullable()->constrained('placement_drives')->nullOnDelete();
            $table->string('status')->default('APPLIED')->index();
            $table->timestamp('applied_at')->useCurrent();
            $table->timestamps();
            
            $table->unique(['student_id', 'job_id']);
        });
    }
    public function down(): void { Schema::dropIfExists('applications'); }
};
"""),

    ("create_skill_gaps_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('skill_gaps', function (Blueprint $table) {
            $table->id();
            $table->foreignId('student_id')->constrained()->cascadeOnDelete();
            $table->foreignId('job_id')->constrained()->cascadeOnDelete();
            $table->foreignId('skill_id')->constrained()->cascadeOnDelete();
            $table->string('gap_severity');
            $table->integer('current_level')->nullable();
            $table->integer('required_level')->nullable();
            $table->boolean('is_mandatory')->default(true);
            $table->string('analysis_version')->default('v1.0');
            $table->text('recommendation')->nullable();
            $table->timestamp('calculated_at')->useCurrent();
            $table->timestamps();
            
            $table->unique(['student_id', 'job_id', 'skill_id']);
        });
    }
    public function down(): void { Schema::dropIfExists('skill_gaps'); }
};
"""),

    ("create_student_scores_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

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
"""),

    ("create_student_projects_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('student_projects', function (Blueprint $table) {
            $table->id();
            $table->foreignId('student_id')->constrained()->cascadeOnDelete();
            $table->string('title');
            $table->text('description')->nullable();
            $table->string('technologies')->nullable();
            $table->string('project_url')->nullable();
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('student_projects'); }
};
"""),

    ("create_student_certifications_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

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
"""),

    ("create_student_academic_history_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

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
"""),

]

for idx, (name, content) in enumerate(migrations):
    filename = f"{get_prefix(idx)}_{name}.php"
    filepath = os.path.join(migration_dir, filename)
    with open(filepath, 'w') as f:
        f.write(content)

print(f"Generated {len(migrations)} secondary migrations.")
