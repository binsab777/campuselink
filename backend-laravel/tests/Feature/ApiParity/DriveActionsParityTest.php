<?php
namespace Tests\Feature\ApiParity;
use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;
use App\Models\User;
use App\Models\Recruiter;
use App\Models\Company;
use App\Models\Job;
use App\Models\PlacementDrive;
use App\Models\DriveCandidate;
use App\Models\Student;
use App\Enums\UserRole;

class DriveActionsParityTest extends TestCase {
    use RefreshDatabase;
    
    public function test_get_available_drives() {
        $user = User::create(['email' => 's@t.com', 'password_hash' => 'x', 'role' => UserRole::STUDENT->value]);
        Student::create(['user_id' => $user->id, 'first_name' => 'S', 'last_name' => 'L', 'student_identifier' => 'STU', 'branch' => 'CS', 'graduation_year' => 2025]);
        
        $company = Company::create(['name' => 'C']);
        $job = Job::create(['company_id' => $company->id, 'title' => 'T', 'description' => 'D', 'employment_type' => 'Full-time']);
        $drive = PlacementDrive::create(['company_id' => $company->id, 'job_id' => $job->id, 'name' => 'D', 'status' => 'PUBLISHED', 'start_date' => now()]);
        
        $response = $this->actingAs($user)->getJson('/api/v1/drives/available');
        $response->assertStatus(200);
        $this->assertEquals('D', $response->json()[0]['name']);
    }
    
    public function test_student_can_register_and_withdraw() {
        $user = User::create(['email' => 's@t.com', 'password_hash' => 'x', 'role' => UserRole::STUDENT->value]);
        $student = Student::create(['user_id' => $user->id, 'first_name' => 'S', 'last_name' => 'L', 'student_identifier' => 'STU', 'branch' => 'CS', 'graduation_year' => 2025]);
        
        $company = Company::create(['name' => 'C']);
        $job = Job::create(['company_id' => $company->id, 'title' => 'T', 'description' => 'D', 'employment_type' => 'Full-time']);
        $drive = PlacementDrive::create(['company_id' => $company->id, 'job_id' => $job->id, 'name' => 'D', 'status' => 'PUBLISHED', 'start_date' => now()]);
        
        // Add Candidate
        $response = $this->actingAs($user)->postJson("/api/v1/drives/{$drive->id}/candidates", ['student_id' => $student->id]);
        $response->assertStatus(201);
        $this->assertDatabaseHas('drive_candidates', ['student_id' => $student->id, 'drive_id' => $drive->id, 'status' => 'REGISTERED']);
        
        // Try to add someone else
        $res2 = $this->actingAs($user)->postJson("/api/v1/drives/{$drive->id}/candidates", ['student_id' => 999]);
        $res2->assertStatus(403);
        
        // Withdraw
        $withdrawResponse = $this->actingAs($user)->postJson("/api/v1/drives/{$drive->id}/withdraw");
        $withdrawResponse->assertStatus(200);
        $this->assertDatabaseHas('drive_candidates', ['student_id' => $student->id, 'drive_id' => $drive->id, 'status' => 'WITHDRAWN']);
    }
    
    public function test_recruiter_can_manage_candidates_and_evaluate() {
        $user = User::create(['email' => 'r@t.com', 'password_hash' => 'x', 'role' => UserRole::RECRUITER->value]);
        $company = Company::create(['name' => 'C']);
        Recruiter::create(['contact_email' => 'a@t.com', 'user_id' => $user->id, 'company_id' => $company->id, 'first_name' => 'F', 'last_name' => 'L']);
        
        $studentUser = User::create(['email' => 's@t.com', 'password_hash' => 'x', 'role' => UserRole::STUDENT->value]);
        $student = Student::create(['user_id' => $studentUser->id, 'first_name' => 'S', 'last_name' => 'L', 'student_identifier' => 'STU', 'branch' => 'CS', 'graduation_year' => 2025, 'cgpa' => 8.5]);
        
        $job = Job::create(['company_id' => $company->id, 'title' => 'T', 'description' => 'D', 'employment_type' => 'Full-time', 'eligibility_config' => ['min_cgpa' => 8.0]]);
        $drive = PlacementDrive::create(['company_id' => $company->id, 'job_id' => $job->id, 'name' => 'D', 'status' => 'PUBLISHED', 'start_date' => now()]);
        
        // Recruiter adds candidate
        $this->actingAs($user)->postJson("/api/v1/drives/{$drive->id}/candidates", ['student_id' => $student->id])->assertStatus(201);
        
        // Evaluate
        $evalRes = $this->actingAs($user)->postJson("/api/v1/drives/{$drive->id}/evaluate-eligibility");
        $evalRes->assertStatus(200);
        $this->assertDatabaseHas('drive_candidates', ['student_id' => $student->id, 'status' => 'ELIGIBLE']);
        
        // Get Candidates
        $getRes = $this->actingAs($user)->getJson("/api/v1/drives/{$drive->id}/candidates");
        $getRes->assertStatus(200);
        $this->assertCount(1, $getRes->json());
        
        // Update Candidate (Shortlist)
        $candId = $getRes->json()[0]['id'];
        $updRes = $this->actingAs($user)->patchJson("/api/v1/drives/{$drive->id}/candidates/{$candId}", ['status' => 'SHORTLISTED']);
        $updRes->assertStatus(200);
        $this->assertDatabaseHas('drive_candidates', ['id' => $candId, 'status' => 'SHORTLISTED']);
        
        // Other recruiter denied
        $user2 = User::create(['email' => 'r2@t.com', 'password_hash' => 'x', 'role' => UserRole::RECRUITER->value]);
        $company2 = Company::create(['name' => 'C2']);
        Recruiter::create(['contact_email' => 'a@t.com', 'user_id' => $user2->id, 'company_id' => $company2->id, 'first_name' => 'F', 'last_name' => 'L']);
        
        $this->actingAs($user2)->getJson("/api/v1/drives/{$drive->id}/candidates")->assertStatus(404);
        $this->actingAs($user2)->postJson("/api/v1/drives/{$drive->id}/evaluate-eligibility")->assertStatus(404);
        $this->actingAs($user2)->patchJson("/api/v1/drives/{$drive->id}/candidates/{$candId}", ['status' => 'REJECTED'])->assertStatus(404);
    }
}
