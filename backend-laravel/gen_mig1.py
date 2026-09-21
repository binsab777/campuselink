import os
import datetime

migration_dir = "database/migrations/"
os.makedirs(migration_dir, exist_ok=True)

# Generate a timestamp prefix
def get_prefix(idx):
    base_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=idx)
    return base_time.strftime("%Y_%m_%d_%H%M%S")

migrations = [
    ("create_users_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('users', function (Blueprint $table) {
            $table->id();
            $table->string('email')->unique();
            $table->string('password_hash');
            $table->string('role');
            $table->boolean('is_active')->default(true);
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('users'); }
};
"""),

    ("create_students_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('students', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->string('student_identifier')->unique();
            $table->string('first_name');
            $table->string('last_name');
            $table->string('branch');
            $table->integer('graduation_year');
            $table->decimal('cgpa', 4, 2)->nullable();
            $table->integer('backlogs_current')->default(0);
            $table->integer('backlogs_history')->default(0);
            $table->string('phone')->nullable();
            $table->date('dob')->nullable();
            $table->string('gender')->nullable();
            $table->string('profile_picture_url')->nullable();
            $table->string('resume_url')->nullable();
            $table->json('profile_metadata')->nullable();
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('students'); }
};
"""),

    ("create_companies_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('companies', function (Blueprint $table) {
            $table->id();
            $table->string('name')->index();
            $table->text('description')->nullable();
            $table->string('industry')->nullable();
            $table->string('website')->nullable();
            $table->string('size')->nullable();
            $table->string('headquarters')->nullable();
            $table->string('logo_url')->nullable();
            $table->json('metadata_json')->nullable();
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('companies'); }
};
"""),

    ("create_recruiters_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('recruiters', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('company_id')->constrained()->cascadeOnDelete();
            $table->string('contact_name')->nullable();
            $table->string('contact_email');
            $table->string('contact_phone')->nullable();
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('recruiters'); }
};
"""),

    ("create_skills_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('skills', function (Blueprint $table) {
            $table->id();
            $table->string('name')->unique();
            $table->string('category')->nullable()->index();
            $table->text('description')->nullable();
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('skills'); }
};
"""),

    ("create_student_skills_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('student_skills', function (Blueprint $table) {
            $table->id();
            $table->foreignId('student_id')->constrained()->cascadeOnDelete();
            $table->foreignId('skill_id')->constrained()->cascadeOnDelete();
            $table->string('proficiency_level');
            $table->integer('months_experience')->default(0);
            $table->string('source')->nullable();
            $table->timestamps();
            
            $table->unique(['student_id', 'skill_id']);
        });
    }
    public function down(): void { Schema::dropIfExists('student_skills'); }
};
"""),

    ("create_jobs_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('jobs', function (Blueprint $table) {
            $table->id();
            $table->foreignId('company_id')->constrained()->cascadeOnDelete();
            $table->foreignId('recruiter_id')->nullable()->constrained()->nullOnDelete();
            $table->string('title')->index();
            $table->text('description');
            $table->string('employment_type');
            $table->string('location')->nullable();
            $table->string('remote_type')->nullable();
            $table->string('salary_range')->nullable();
            $table->string('experience_requirement')->nullable();
            $table->timestamp('application_deadline')->nullable();
            $table->integer('openings')->nullable();
            $table->string('job_code')->nullable();
            $table->json('job_description_json')->nullable();
            $table->json('eligibility_config')->nullable();
            $table->string('status')->default('DRAFT')->index();
            $table->timestamps();
        });
    }
    public function down(): void { Schema::dropIfExists('jobs'); }
};
"""),

    ("create_job_requirements_table", """<?php
use Illuminate\\Database\\Migrations\\Migration;
use Illuminate\\Database\\Schema\\Blueprint;
use Illuminate\\Support\\Facades\\Schema;

return new class extends Migration {
    public function up(): void {
        Schema::create('job_requirements', function (Blueprint $table) {
            $table->id();
            $table->foreignId('job_id')->constrained()->cascadeOnDelete();
            $table->foreignId('skill_id')->constrained()->cascadeOnDelete();
            $table->string('required_proficiency');
            $table->boolean('is_mandatory')->default(true);
            $table->timestamps();
            
            $table->unique(['job_id', 'skill_id']);
        });
    }
    public function down(): void { Schema::dropIfExists('job_requirements'); }
};
"""),

]

for idx, (name, content) in enumerate(migrations):
    filename = f"{get_prefix(idx)}_{name}.php"
    filepath = os.path.join(migration_dir, filename)
    with open(filepath, 'w') as f:
        f.write(content)

print(f"Generated {len(migrations)} core migrations.")
