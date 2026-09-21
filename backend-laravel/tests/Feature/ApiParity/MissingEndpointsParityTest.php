<?php
namespace Tests\Feature\ApiParity;
use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;
use App\Models\User;
use App\Models\Recruiter;
use App\Models\Company;
use App\Models\Job;
use App\Models\PlacementDrive;
use App\Models\Skill;
use App\Enums\UserRole;

/**
 * Covers the 8 endpoints remaining unverified:
 * DELETE /api/v1/recruiters/me/jobs/{id}
 * DELETE /api/v1/skills/{id}
 * GET    /api/v1/officer/students
 * GET    /api/v1/recruiters/me/drives
 * GET    /api/v1/recruiters/me/jobs/{id}
 * PUT    /api/v1/recruiters/me/drives/{id}
 * PUT    /api/v1/recruiters/me/jobs/{id}
 * PUT    /api/v1/skills/{id}
 */
class MissingEndpointsParityTest extends TestCase {
    use RefreshDatabase;

    private function makeRecruiter(): array {
        $user = User::create(['email' => 'rec@t.com', 'password_hash' => 'x', 'role' => UserRole::RECRUITER->value]);
        $company = Company::create(['name' => 'TechCo']);
        Recruiter::create(['user_id' => $user->id, 'company_id' => $company->id, 'contact_email' => 'rec@t.com', 'contact_name' => 'Rec']);
        return [$user, $company];
    }

    // ---- Recruiter Job CRUD ----
    public function test_get_recruiter_job_by_id() {
        [$user, $company] = $this->makeRecruiter();
        $job = Job::create(['company_id' => $company->id, 'title' => 'SWE', 'description' => 'D', 'employment_type' => 'Full-time', 'status' => 'DRAFT']);

        $res = $this->actingAs($user)->getJson("/api/v1/recruiters/me/jobs/{$job->id}");
        $res->assertStatus(200);
        $this->assertEquals('SWE', $res->json('title'));
        $this->assertEquals('DRAFT', $res->json('status'));
    }

    public function test_update_recruiter_job() {
        [$user, $company] = $this->makeRecruiter();
        $job = Job::create(['company_id' => $company->id, 'title' => 'SWE', 'description' => 'D', 'employment_type' => 'Full-time', 'status' => 'DRAFT']);

        $res = $this->actingAs($user)->putJson("/api/v1/recruiters/me/jobs/{$job->id}", ['title' => 'Senior SWE', 'status' => 'PUBLISHED']);
        $res->assertStatus(200);
        $this->assertDatabaseHas('jobs', ['id' => $job->id, 'title' => 'Senior SWE', 'status' => 'PUBLISHED']);
    }

    public function test_delete_recruiter_job() {
        [$user, $company] = $this->makeRecruiter();
        $job = Job::create(['company_id' => $company->id, 'title' => 'SWE', 'description' => 'D', 'employment_type' => 'Full-time', 'status' => 'DRAFT']);

        $this->actingAs($user)->deleteJson("/api/v1/recruiters/me/jobs/{$job->id}")->assertStatus(204);
        $this->assertDatabaseMissing('jobs', ['id' => $job->id]);
    }

    public function test_recruiter_cannot_delete_another_recruiters_job() {
        [$user, $company] = $this->makeRecruiter();
        $user2 = User::create(['email' => 'rec2@t.com', 'password_hash' => 'x', 'role' => UserRole::RECRUITER->value]);
        $company2 = Company::create(['name' => 'OtherCo']);
        Recruiter::create(['user_id' => $user2->id, 'company_id' => $company2->id, 'contact_email' => 'rec2@t.com', 'contact_name' => 'Rec2']);
        $job = Job::create(['company_id' => $company->id, 'title' => 'SWE', 'description' => 'D', 'employment_type' => 'Full-time']);

        $this->actingAs($user2)->deleteJson("/api/v1/recruiters/me/jobs/{$job->id}")->assertStatus(404);
        $this->assertDatabaseHas('jobs', ['id' => $job->id]);
    }

    // ---- Recruiter Drive CRUD ----
    public function test_get_recruiter_drives() {
        [$user, $company] = $this->makeRecruiter();
        $job = Job::create(['company_id' => $company->id, 'title' => 'SWE', 'description' => 'D', 'employment_type' => 'Full-time']);
        PlacementDrive::create(['company_id' => $company->id, 'job_id' => $job->id, 'name' => 'Drive 1', 'start_date' => now()->addDays(5)->toDateString(), 'status' => 'DRAFT']);

        $res = $this->actingAs($user)->getJson('/api/v1/recruiters/me/drives');
        $res->assertStatus(200);
        $this->assertCount(1, $res->json());
    }

    public function test_update_recruiter_drive() {
        [$user, $company] = $this->makeRecruiter();
        $job = Job::create(['company_id' => $company->id, 'title' => 'SWE', 'description' => 'D', 'employment_type' => 'Full-time']);
        $drive = PlacementDrive::create(['company_id' => $company->id, 'job_id' => $job->id, 'name' => 'Drive 1', 'start_date' => now()->addDays(5)->toDateString(), 'status' => 'DRAFT']);

        $res = $this->actingAs($user)->putJson("/api/v1/recruiters/me/drives/{$drive->id}", ['name' => 'Updated Drive', 'status' => 'PUBLISHED']);
        $res->assertStatus(200);
        $this->assertDatabaseHas('placement_drives', ['id' => $drive->id, 'name' => 'Updated Drive']);
    }

    // ---- Skills CRUD ----
    public function test_update_and_delete_skill() {
        $officer = User::create(['email' => 'off@t.com', 'password_hash' => 'x', 'role' => UserRole::PLACEMENT_OFFICER->value]);
        $skill = Skill::create(['name' => 'PYTHON', 'category' => 'Programming']);

        $upRes = $this->actingAs($officer)->putJson("/api/v1/skills/{$skill->id}", ['name' => 'PYTHON3', 'category' => 'Scripting']);
        $upRes->assertStatus(200);
        $this->assertDatabaseHas('skills', ['id' => $skill->id, 'name' => 'PYTHON3']);

        $delRes = $this->actingAs($officer)->deleteJson("/api/v1/skills/{$skill->id}");
        $delRes->assertStatus(204);
        $this->assertDatabaseMissing('skills', ['id' => $skill->id]);
    }

    // ---- Officer Students ----
    public function test_officer_students_pagination_and_fields() {
        $officer = User::create(['email' => 'off2@t.com', 'password_hash' => 'x', 'role' => UserRole::PLACEMENT_OFFICER->value]);
        $stuUser = User::create(['email' => 'stu@t.com', 'password_hash' => 'x', 'role' => UserRole::STUDENT->value]);
        \App\Models\Student::create(['user_id' => $stuUser->id, 'first_name' => 'Alice', 'last_name' => 'Smith', 'student_identifier' => 'STU001', 'branch' => 'CS', 'graduation_year' => 2025]);

        $res = $this->actingAs($officer)->getJson('/api/v1/officer/students');
        $res->assertStatus(200);
        $this->assertArrayHasKey('total', $res->json());
        $this->assertArrayHasKey('students', $res->json());
        $this->assertCount(1, $res->json('students'));

        // Student role gets 403
        $this->actingAs($stuUser)->getJson('/api/v1/officer/students')->assertStatus(403);
    }
}
