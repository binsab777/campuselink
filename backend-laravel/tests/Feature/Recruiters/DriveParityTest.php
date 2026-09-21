<?php
namespace Tests\Feature\Recruiters;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use App\Models\User;
use App\Models\Recruiter;
use App\Models\Company;
use App\Enums\UserRole;

class DriveParityTest extends TestCase {
    use RefreshDatabase;
    private $recruiterUser;
    private $company;
    
    protected function setUp(): void {
        parent::setUp();
        $this->recruiterUser = User::factory()->create(['role' => UserRole::RECRUITER->value]);
        $this->company = Company::create(['name' => 'Tech Corp', 'description' => 'A tech company']);
        Recruiter::create(['user_id' => $this->recruiterUser->id, 'company_id' => $this->company->id, 'contact_email' => 'r3@test.com']);
    }

    public function test_recruiter_can_create_drive() {
        // First create a job since drives require a job_id (verified by FastAPI schema constraints)
        $job = $this->company->jobs()->create([
            'title' => 'Software Engineer',
            'description' => 'Coding',
            'employment_type' => 'FULL_TIME',
            'deadline' => '2027-01-01',
            'status' => 'DRAFT',
            'posted_by_id' => $this->recruiterUser->recruiterProfile->id
        ]);
        
        $payload = [
            'name' => 'Spring 2027 Hiring', 
            'date' => '2027-04-01', 
            'job_id' => $job->id,
            'start_time' => '2027-04-01 09:00:00',
            'end_time' => '2027-04-01 17:00:00'
        ];
        
        $response = $this->actingAs($this->recruiterUser)->postJson('/api/v1/recruiters/me/drives', $payload);
        $response->assertStatus(201);
        $this->assertDatabaseHas('placement_drives', ['name' => 'Spring 2027 Hiring', 'job_id' => $job->id]);
    }
}
