import os

files = {
    "database/factories/UserFactory.php": """<?php
namespace Database\\Factories;
use App\\Models\\User;
use App\\Enums\\UserRole;
use Illuminate\\Database\\Eloquent\\Factories\\Factory;
use Illuminate\\Support\\Facades\\Hash;
class UserFactory extends Factory {
    protected $model = User::class;
    public function definition() {
        return [
            'email' => $this->faker->unique()->safeEmail,
            'password_hash' => Hash::make('password'),
            'role' => UserRole::STUDENT->value,
            'is_active' => true,
        ];
    }
}
""",
    "database/factories/StudentFactory.php": """<?php
namespace Database\\Factories;
use App\\Models\\Student;
use App\\Models\\User;
use Illuminate\\Database\\Eloquent\\Factories\\Factory;
class StudentFactory extends Factory {
    protected $model = Student::class;
    public function definition() {
        return [
            'user_id' => User::factory(),
            'student_identifier' => 'STU' . $this->faker->unique()->numberBetween(1000, 9999),
            'first_name' => $this->faker->firstName,
            'last_name' => $this->faker->lastName,
            'branch' => 'Computer Science',
            'graduation_year' => 2025,
            'cgpa' => $this->faker->randomFloat(2, 6, 9.9),
            'backlogs_current' => 0,
            'backlogs_history' => 0,
            'phone' => $this->faker->phoneNumber,
        ];
    }
}
""",
    "database/factories/CompanyFactory.php": """<?php
namespace Database\\Factories;
use App\\Models\\Company;
use Illuminate\\Database\\Eloquent\\Factories\\Factory;
class CompanyFactory extends Factory {
    protected $model = Company::class;
    public function definition() {
        return [
            'name' => $this->faker->company,
            'description' => $this->faker->catchPhrase,
            'industry' => 'Technology',
            'website_url' => $this->faker->url,
        ];
    }
}
""",
    "database/factories/JobFactory.php": """<?php
namespace Database\\Factories;
use App\\Models\\Job;
use App\\Models\\Company;
use App\\Enums\\JobStatus;
use Illuminate\\Database\\Eloquent\\Factories\\Factory;
class JobFactory extends Factory {
    protected $model = Job::class;
    public function definition() {
        return [
            'company_id' => Company::factory(),
            'title' => $this->faker->jobTitle,
            'description' => $this->faker->paragraph,
            'employment_type' => 'Full-time',
            'location' => $this->faker->city,
            'salary_range' => '$80k - $120k',
            'status' => JobStatus::OPEN->value,
            'eligibility_config' => ['min_cgpa' => 7.0, 'allowed_branches' => ['Computer Science', 'IT']],
        ];
    }
}
""",
    "database/factories/SkillFactory.php": """<?php
namespace Database\\Factories;
use App\\Models\\Skill;
use Illuminate\\Database\\Eloquent\\Factories\\Factory;
class SkillFactory extends Factory {
    protected $model = Skill::class;
    public function definition() {
        return [
            'name' => $this->faker->unique()->word,
            'category' => 'Technical',
        ];
    }
}
""",
    "database/seeders/DatabaseSeeder.php": """<?php
namespace Database\\Seeders;
use Illuminate\\Database\\Seeder;
use App\\Models\\User;
use App\\Models\\Student;
use App\\Models\\Company;
use App\\Models\\Recruiter;
use App\\Models\\Job;
use App\\Models\\Skill;
use App\\Models\\StudentSkill;
use App\\Enums\\UserRole;
use App\\Enums\\ProficiencyLevel;
use App\\Enums\\JobStatus;
use App\\Services\\ReadinessScoringService;
use App\\Services\\SkillGapService;
class DatabaseSeeder extends Seeder {
    public function run() {
        // Admin
        User::factory()->create(['email' => 'testadmin99@test.com', 'role' => UserRole::SUPER_ADMIN->value]);
        
        // Master Skills
        $python = Skill::factory()->create(['name' => 'Python']);
        $java = Skill::factory()->create(['name' => 'Java']);
        $react = Skill::factory()->create(['name' => 'React']);
        $comm = Skill::factory()->create(['name' => 'Communication', 'category' => 'Soft Skill']);

        // Company & Job
        $company = Company::factory()->create(['name' => 'Tech Corp']);
        $recUser = User::factory()->create(['email' => 'testrecruiter99@test.com', 'role' => UserRole::RECRUITER->value]);
        Recruiter::create(['user_id' => $recUser->id, 'company_id' => $company->id, 'contact_name' => 'Recruiter Bob']);
        
        $job = Job::factory()->create(['company_id' => $company->id, 'title' => 'Backend Engineer']);
        $job->requirements()->create(['skill_id' => $python->id, 'required_proficiency' => ProficiencyLevel::ADVANCED->value, 'is_mandatory' => true]);
        $job->requirements()->create(['skill_id' => $java->id, 'required_proficiency' => ProficiencyLevel::INTERMEDIATE->value, 'is_mandatory' => false]);

        // Student for Phase 6 Testing
        $stuUser = User::factory()->create(['email' => 'teststudent99@test.com', 'role' => UserRole::STUDENT->value]);
        $student = Student::factory()->create([
            'user_id' => $stuUser->id, 
            'first_name' => 'Test', 
            'last_name' => 'Student',
            'cgpa' => 8.5
        ]);

        StudentSkill::create(['student_id' => $student->id, 'skill_id' => $python->id, 'proficiency_level' => ProficiencyLevel::INTERMEDIATE->value]);
        StudentSkill::create(['student_id' => $student->id, 'skill_id' => $comm->id, 'proficiency_level' => ProficiencyLevel::ADVANCED->value]);

        $student->projects()->create(['title' => 'Web App', 'description' => 'Test', 'technologies' => ['Python']]);

        // Calculate initial phase 6 scores
        $readiness = new ReadinessScoringService();
        $readiness->calculateReadiness($student);

        $skillGap = new SkillGapService();
        $skillGap->analyzeSkillGaps($student, $job);
    }
}
"""
}

for filepath, content in files.items():
    os.makedirs(os.path.dirname(f"d:/xampp/htdocs/campuslink/backend-laravel/{filepath}"), exist_ok=True)
    with open(f"d:/xampp/htdocs/campuslink/backend-laravel/{filepath}", 'w') as f:
        f.write(content)
print("Factories and seeders generated.")
