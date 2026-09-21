<?php
namespace Tests\Feature\Recruiters;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use App\Models\User;
use App\Models\Recruiter;
use App\Models\Company;
use App\Enums\UserRole;

class JobParityTest extends TestCase {
    use RefreshDatabase;
    private $recruiterUser;
    private $otherRecruiter;

    protected function setUp(): void {
        parent::setUp();
        $this->recruiterUser = User::factory()->create(['role' => UserRole::RECRUITER->value]);
        $company = Company::create(['name' => 'Tech Corp', 'description' => 'A tech company']);
        Recruiter::create(['user_id' => $this->recruiterUser->id, 'company_id' => $company->id, 'contact_email' => 'r1@test.com']);

        $this->otherRecruiter = User::factory()->create(['role' => UserRole::RECRUITER->value]);
        $company2 = Company::create(['name' => 'Other Corp', 'description' => 'Another company']);
        Recruiter::create(['user_id' => $this->otherRecruiter->id, 'company_id' => $company2->id, 'contact_email' => 'r2@test.com']);
    }

    public function test_recruiter_can_create_job() {
        $payload = ['title' => 'Software Engineer', 'description' => 'Coding in PHP and Laravel', 'employment_type' => 'FULL_TIME', 'application_deadline' => '2027-01-01'];
        $response = $this->actingAs($this->recruiterUser)->postJson('/api/v1/recruiters/me/jobs', $payload);
        $response->assertStatus(201);
        $this->assertDatabaseHas('jobs', ['title' => 'Software Engineer', 'status' => 'DRAFT']);
    }

    public function test_recruiter_can_list_own_jobs() {
        $payload = ['title' => 'Software Engineer', 'description' => 'Coding in PHP and Laravel', 'employment_type' => 'FULL_TIME', 'application_deadline' => '2027-01-01'];
        $this->actingAs($this->recruiterUser)->postJson('/api/v1/recruiters/me/jobs', $payload);
        $response = $this->actingAs($this->recruiterUser)->getJson('/api/v1/recruiters/me/jobs');
        $response->assertStatus(200);
        $this->assertCount(1, $response->json());
    }

    public function test_recruiter_cannot_delete_other_recruiters_job() {
        $payload = ['title' => 'Software Engineer', 'description' => 'Coding in PHP and Laravel', 'employment_type' => 'FULL_TIME', 'application_deadline' => '2027-01-01'];
        $response = $this->actingAs($this->recruiterUser)->postJson('/api/v1/recruiters/me/jobs', $payload);
        $jobId = $response->json('id');
        
        $deleteResponse = $this->actingAs($this->otherRecruiter)->deleteJson('/api/v1/me/jobs/' . $jobId);
        $deleteResponse->assertStatus(404);
        $this->assertDatabaseHas('jobs', ['id' => $jobId]);
    }
}
