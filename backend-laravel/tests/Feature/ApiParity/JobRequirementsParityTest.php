<?php
namespace Tests\Feature\ApiParity;
use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;
use App\Models\User;
use App\Models\Recruiter;
use App\Models\Company;
use App\Models\Job;
use App\Models\Skill;
use App\Enums\UserRole;

class JobRequirementsParityTest extends TestCase {
    use RefreshDatabase;
    
    public function test_get_skills_all() {
        Skill::create(['name' => 'Python', 'category' => 'Tech']);
        $response = $this->getJson('/api/v1/jobs/skills/all');
        $response->assertStatus(200);
        $this->assertEquals('Python', $response->json()[0]['name']);
    }
    
    public function test_get_job_requirements() {
        $company = Company::create(['name' => 'C']);
        $job = Job::create(['company_id' => $company->id, 'title' => 'T', 'description' => 'D', 'employment_type' => 'Full-time']);
        $skill = Skill::create(['name' => 'Java', 'category' => 'Tech']);
        $job->requirements()->create(['skill_id' => $skill->id, 'required_proficiency' => 'BEGINNER']);
        
        $response = $this->getJson("/api/v1/jobs/{$job->id}/requirements");
        $response->assertStatus(200);
        $this->assertCount(1, $response->json());
    }
    
    public function test_recruiter_can_add_and_remove_requirements() {
        $user = User::create(['email' => 'r@t.com', 'password_hash' => 'x', 'role' => UserRole::RECRUITER->value]);
        $company = Company::create(['name' => 'C']);
        Recruiter::create(['contact_email' => 'c@t.com', 'user_id' => $user->id, 'company_id' => $company->id, 'first_name' => 'F', 'last_name' => 'L']);
        $job = Job::create(['company_id' => $company->id, 'title' => 'T', 'description' => 'D', 'employment_type' => 'Full-time']);
        $skill = Skill::create(['name' => 'Java', 'category' => 'Tech']);
        
        // Add
        $response = $this->actingAs($user)->postJson("/api/v1/jobs/{$job->id}/requirements", [
            'skill_id' => $skill->id,
            'required_proficiency' => 'ADVANCED'
        ]);
        $response->assertStatus(200);
        $reqId = $response->json('id');
        
        // Remove
        $delResponse = $this->actingAs($user)->deleteJson("/api/v1/jobs/{$job->id}/requirements/{$reqId}");
        $delResponse->assertStatus(204);
    }
    
    public function test_other_recruiter_cannot_modify_requirements() {
        $company1 = Company::create(['name' => 'C1']);
        $company2 = Company::create(['name' => 'C2']);
        $job = Job::create(['company_id' => $company1->id, 'title' => 'T', 'description' => 'D', 'employment_type' => 'Full-time']);
        
        $user2 = User::create(['email' => 'r2@t.com', 'password_hash' => 'x', 'role' => UserRole::RECRUITER->value]);
        Recruiter::create(['contact_email' => 'c@t.com', 'user_id' => $user2->id, 'company_id' => $company2->id, 'first_name' => 'F', 'last_name' => 'L']);
        $skill = Skill::create(['name' => 'Java', 'category' => 'Tech']);
        
        $response = $this->actingAs($user2)->postJson("/api/v1/jobs/{$job->id}/requirements", [
            'skill_id' => $skill->id,
            'required_proficiency' => 'ADVANCED'
        ]);
        $response->assertStatus(404); // Maps to FastAPI 404
    }
}
