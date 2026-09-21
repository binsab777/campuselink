import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip())

write_file('tests/Feature/Recruiters/JobParityTest.php', """<?php
namespace Tests\\Feature\\Recruiters;
use Illuminate\\Foundation\\Testing\\RefreshDatabase;
use Tests\\TestCase;
use App\\Models\\User;
use App\\Models\\Recruiter;
use App\\Models\\Company;
use App\\Enums\\UserRole;

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
        $payload = ['title' => 'Software Engineer', 'description' => 'Coding', 'type' => 'FULL_TIME', 'deadline' => '2027-01-01'];
        $response = $this->actingAs($this->recruiterUser)->postJson('/api/v1/me/jobs', $payload);
        $response->assertStatus(201);
        $this->assertDatabaseHas('jobs', ['title' => 'Software Engineer', 'status' => 'DRAFT']);
    }

    public function test_recruiter_can_list_own_jobs() {
        $payload = ['title' => 'Software Engineer', 'description' => 'Coding', 'type' => 'FULL_TIME', 'deadline' => '2027-01-01'];
        $this->actingAs($this->recruiterUser)->postJson('/api/v1/me/jobs', $payload);
        $response = $this->actingAs($this->recruiterUser)->getJson('/api/v1/me/jobs');
        $response->assertStatus(200);
        $this->assertCount(1, $response->json());
    }

    public function test_recruiter_cannot_delete_other_recruiters_job() {
        $payload = ['title' => 'Software Engineer', 'description' => 'Coding', 'type' => 'FULL_TIME', 'deadline' => '2027-01-01'];
        $response = $this->actingAs($this->recruiterUser)->postJson('/api/v1/me/jobs', $payload);
        $jobId = $response->json('id');
        
        $deleteResponse = $this->actingAs($this->otherRecruiter)->deleteJson('/api/v1/me/jobs/' . $jobId);
        $deleteResponse->assertStatus(404);
        $this->assertDatabaseHas('jobs', ['id' => $jobId]);
    }
}
""")

write_file('tests/Feature/Recruiters/DriveParityTest.php', """<?php
namespace Tests\\Feature\\Recruiters;
use Illuminate\\Foundation\\Testing\\RefreshDatabase;
use Tests\\TestCase;
use App\\Models\\User;
use App\\Models\\Recruiter;
use App\\Models\\Company;
use App\\Enums\\UserRole;

class DriveParityTest extends TestCase {
    use RefreshDatabase;
    private $recruiterUser;
    
    protected function setUp(): void {
        parent::setUp();
        $this->recruiterUser = User::factory()->create(['role' => UserRole::RECRUITER->value]);
        $company = Company::create(['name' => 'Tech Corp', 'description' => 'A tech company']);
        Recruiter::create(['user_id' => $this->recruiterUser->id, 'company_id' => $company->id, 'contact_email' => 'r3@test.com']);
    }

    public function test_recruiter_can_create_drive() {
        $payload = ['name' => 'Spring 2027 Hiring', 'date' => '2027-04-01'];
        $response = $this->actingAs($this->recruiterUser)->postJson('/api/v1/me/drives', $payload);
        $response->assertStatus(201);
        $this->assertDatabaseHas('placement_drives', ['name' => 'Spring 2027 Hiring']);
    }
}
""")

print("Tests rewritten!")
