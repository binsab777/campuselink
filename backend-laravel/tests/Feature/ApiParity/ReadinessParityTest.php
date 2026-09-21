<?php
namespace Tests\Feature\ApiParity;
use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;
use App\Models\User;
use App\Models\Student;
use App\Models\Job;
use App\Models\Company;
use App\Models\Recruiter;
use App\Enums\UserRole;

class ReadinessParityTest extends TestCase {
    use RefreshDatabase;
    
    public function test_eligibility_check() {
        $user = User::create(['email' => 'r@t.com', 'password_hash' => 'x', 'role' => UserRole::RECRUITER->value]);
        $company = Company::create(['name' => 'C']);
        Recruiter::create(['contact_email' => 'a@t.com', 'user_id' => $user->id, 'company_id' => $company->id, 'first_name' => 'F', 'last_name' => 'L']);
        $job = Job::create(['company_id' => $company->id, 'title' => 'T', 'description' => 'D', 'employment_type' => 'Full-time']);
        
        $studentUser = User::create(['email' => 's@t.com', 'password_hash' => 'x', 'role' => UserRole::STUDENT->value]);
        $student = Student::create(['user_id' => $studentUser->id, 'first_name' => 'S', 'last_name' => 'L', 'student_identifier' => 'STU', 'branch' => 'CS', 'graduation_year' => 2025]);
        
        $res = $this->actingAs($user)->postJson("/api/v1/jobs/{$job->id}/eligibility/check", ['student_id' => $student->id]);
        $res->assertStatus(200);
    }
    
    public function test_readiness_me_and_analyze() {
        $studentUser = User::create(['email' => 's@t.com', 'password_hash' => 'x', 'role' => UserRole::STUDENT->value]);
        $student = Student::create(['user_id' => $studentUser->id, 'first_name' => 'S', 'last_name' => 'L', 'student_identifier' => 'STU', 'branch' => 'CS', 'graduation_year' => 2025]);
        
        $this->actingAs($studentUser)->getJson("/api/v1/readiness/me")->assertStatus(200);
        
        $company = Company::create(['name' => 'C']);
        $job = Job::create(['company_id' => $company->id, 'title' => 'T', 'description' => 'D', 'employment_type' => 'Full-time']);
        
        $this->actingAs($studentUser)->postJson("/api/v1/readiness/me/jobs/{$job->id}/skill-gaps/analyze")->assertStatus(200);
    }
    
    public function test_officer_readiness() {
        $officer = User::create(['email' => 'o@t.com', 'password_hash' => 'x', 'role' => UserRole::PLACEMENT_OFFICER->value]);
        
        $studentUser = User::create(['email' => 's@t.com', 'password_hash' => 'x', 'role' => UserRole::STUDENT->value]);
        $student = Student::create(['user_id' => $studentUser->id, 'first_name' => 'S', 'last_name' => 'L', 'student_identifier' => 'STU', 'branch' => 'CS', 'graduation_year' => 2025]);
        
        $this->actingAs($officer)->getJson("/api/v1/readiness/students/{$student->id}")->assertStatus(200);
        
        $company = Company::create(['name' => 'C']);
        $job = Job::create(['company_id' => $company->id, 'title' => 'T', 'description' => 'D', 'employment_type' => 'Full-time']);
        
        $this->actingAs($officer)->getJson("/api/v1/readiness/students/{$student->id}/jobs/{$job->id}/skill-gaps")->assertStatus(200);
    }
}
