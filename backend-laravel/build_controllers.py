import os

files = {
    # Controllers
    "app/Http/Controllers/Api/RecruiterController.php": """<?php
namespace App\\Http\\Controllers\\Api;
use App\\Http\\Controllers\\Controller;
use Illuminate\\Http\\Request;
class RecruiterController extends Controller {
    public function getCompany(Request $request) {
        $recruiter = $request->user()->recruiterProfile;
        return response()->json($recruiter->company);
    }
}
""",
    "app/Http/Controllers/Api/JobController.php": """<?php
namespace App\\Http\\Controllers\\Api;
use App\\Http\\Controllers\\Controller;
use Illuminate\\Http\\Request;
use App\\Models\\Job;
use App\\Services\\EligibilityService;
use App\\Services\\SkillGapService;
class JobController extends Controller {
    public function index() { return response()->json(Job::with('company')->get()); }
    public function show(Job $job) { return response()->json($job->load(['company', 'requirements.skill'])); }
    public function checkEligibility(Request $request, Job $job, EligibilityService $service) {
        return response()->json($service->checkHardEligibility($request->user()->studentProfile, $job));
    }
    public function calculateSkillGap(Request $request, Job $job, SkillGapService $service) {
        return response()->json($service->analyzeSkillGaps($request->user()->studentProfile, $job));
    }
}
""",
    "app/Http/Controllers/Api/DriveController.php": """<?php
namespace App\\Http\\Controllers\\Api;
use App\\Http\\Controllers\\Controller;
use Illuminate\\Http\\Request;
use App\\Models\\PlacementDrive;
class DriveController extends Controller {
    public function index() { return response()->json(PlacementDrive::with('company', 'job')->get()); }
}
""",
    # Tests
    "tests/Feature/Phase6ParityTest.php": """<?php
namespace Tests\\Feature;
use Tests\\TestCase;
use Illuminate\\Foundation\\Testing\\RefreshDatabase;
use App\\Models\\User;
use App\\Models\\Student;
use App\\Models\\Job;
use App\\Models\\Company;
use App\\Models\\Recruiter;
use App\\Enums\\UserRole;
use App\\Enums\\ProficiencyLevel;
use App\\Models\\Skill;
class Phase6ParityTest extends TestCase {
    use RefreshDatabase;
    public function test_eligibility_and_skill_gap_deterministic() {
        $user = User::create(['email' => 'stu@test.com', 'password_hash' => 'x', 'role' => UserRole::STUDENT->value]);
        $student = Student::create(['user_id' => $user->id, 'student_identifier' => 'STU1', 'first_name' => 'A', 'last_name' => 'B', 'branch' => 'CS', 'graduation_year' => 2025, 'cgpa' => 8.0, 'backlogs_current' => 0]);
        $company = Company::create(['name' => 'Tech Corp']);
        $job = Job::create(['company_id' => $company->id, 'title' => 'Software Engineer', 'description' => 'Desc', 'employment_type' => 'Full-time', 'eligibility_config' => ['min_cgpa' => 7.5, 'allowed_branches' => ['CS', 'IT']]]);
        $skill = Skill::create(['name' => 'Python', 'category' => 'Technical']);
        $job->requirements()->create(['skill_id' => $skill->id, 'required_proficiency' => ProficiencyLevel::ADVANCED->value, 'is_mandatory' => true]);
        
        // Skill Gap - Student has NO python
        $response = $this->actingAs($user)->getJson("/api/v1/jobs/{$job->id}/skill-gaps");
        $response->assertStatus(200);
        $data = $response->json();
        $this->assertEquals('CRITICAL', $data[0]['gap_severity']); // since mandatory and student has 0
        
        // Eligibility - Student has 8.0 > 7.5
        $resp2 = $this->actingAs($user)->getJson("/api/v1/jobs/{$job->id}/eligibility");
        $resp2->assertStatus(200)->assertJsonFragment(['is_eligible' => true]);
    }
}
"""
}

for filepath, content in files.items():
    os.makedirs(os.path.dirname(f"d:/xampp/htdocs/campuslink/backend-laravel/{filepath}"), exist_ok=True)
    with open(f"d:/xampp/htdocs/campuslink/backend-laravel/{filepath}", 'w') as f:
        f.write(content)
