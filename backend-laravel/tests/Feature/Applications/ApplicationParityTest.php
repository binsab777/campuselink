<?php
namespace Tests\Feature\Applications;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use App\Models\User;
use App\Models\Student;
use App\Models\Recruiter;
use App\Models\Company;
use App\Models\Job;
use App\Enums\UserRole;

class ApplicationParityTest extends TestCase {
    use RefreshDatabase;
    private $studentUser;
    private $job;
    
    protected function setUp(): void {
        parent::setUp();
        $this->studentUser = User::factory()->create(['role' => UserRole::STUDENT->value]);
        Student::create(['user_id' => $this->studentUser->id, 'first_name' => 'John', 'last_name' => 'Doe', 'student_identifier' => 'STU456', 'branch' => 'CSE', 'graduation_year' => 2027]);
        
        $recruiterUser = User::factory()->create(['role' => UserRole::RECRUITER->value]);
        $company = Company::create(['name' => 'Tech Corp', 'description' => 'A tech company']);
        Recruiter::create(['user_id' => $recruiterUser->id, 'company_id' => $company->id, 'contact_email' => 'contact@tech.corp']);
        
        $this->job = $company->jobs()->create([
            'title' => 'Software Engineer',
            'description' => 'Coding',
            'employment_type' => 'FULL_TIME',
            'deadline' => '2027-01-01',
            'status' => 'PUBLISHED',
            'posted_by_id' => $recruiterUser->recruiterProfile->id
        ]);
    }

    public function test_student_can_apply_to_job() {
        $response = $this->actingAs($this->studentUser)->postJson("/api/v1/jobs/{$this->job->id}/apply", [
            'job_id' => $this->job->id
        ]);
        $response->assertStatus(201);
        $this->assertDatabaseHas('applications', ['job_id' => $this->job->id, 'student_id' => $this->studentUser->studentProfile->id, 'status' => 'APPLIED']);
    }
}
