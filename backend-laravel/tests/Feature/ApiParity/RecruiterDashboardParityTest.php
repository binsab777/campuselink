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

class RecruiterDashboardParityTest extends TestCase {
    use RefreshDatabase;
    
    public function test_dashboard_metrics() {
        $user = User::create(['email' => 'r@t.com', 'password_hash' => 'x', 'role' => UserRole::RECRUITER->value]);
        $company = Company::create(['name' => 'C']);
        Recruiter::create(['contact_email' => 'a@t.com', 'user_id' => $user->id, 'company_id' => $company->id, 'first_name' => 'F', 'last_name' => 'L']);
        
        $job = Job::create(['company_id' => $company->id, 'title' => 'T1', 'description' => 'D', 'employment_type' => 'Full-time', 'status' => 'PUBLISHED']);
        Job::create(['company_id' => $company->id, 'title' => 'T2', 'description' => 'D', 'employment_type' => 'Full-time', 'status' => 'DRAFT']);
        
        $drive = PlacementDrive::create([
            'company_id' => $company->id,
            'job_id' => $job->id,
            'name' => 'Drive',
            'start_date' => now()->addDays(5)->toDateString(),
            'status' => 'PUBLISHED'
        ]);
        
        $studentUser = User::create(['email' => 's@t.com', 'password_hash' => 'x', 'role' => UserRole::STUDENT->value]);
        $student = Student::create(['user_id' => $studentUser->id, 'first_name' => 'S', 'last_name' => 'L', 'student_identifier' => 'STU', 'branch' => 'CS', 'graduation_year' => 2025]);
        
        DriveCandidate::create(['drive_id' => $drive->id, 'student_id' => $student->id, 'status' => 'SHORTLISTED']);
        
        $response = $this->actingAs($user)->getJson('/api/v1/recruiters/me/dashboard');
        $response->assertStatus(200);
        $response->assertJsonStructure([
            'active_jobs_count',
            'upcoming_drives_count',
            'total_candidates_count',
            'shortlisted_candidates_count'
        ]);
        $data = $response->json();
        $this->assertEquals(1, $data['active_jobs_count']);
        $this->assertEquals(1, $data['upcoming_drives_count']);
        $this->assertEquals(1, $data['total_candidates_count']);
        $this->assertEquals(1, $data['shortlisted_candidates_count']);
    }
    
    public function test_get_candidate_profile() {
        $user = User::create(['email' => 'r@t.com', 'password_hash' => 'x', 'role' => UserRole::RECRUITER->value]);
        $company = Company::create(['name' => 'C']);
        Recruiter::create(['contact_email' => 'a@t.com', 'user_id' => $user->id, 'company_id' => $company->id, 'first_name' => 'F', 'last_name' => 'L']);
        
        $studentUser = User::create(['email' => 's@t.com', 'password_hash' => 'x', 'role' => UserRole::STUDENT->value]);
        $student = Student::create(['user_id' => $studentUser->id, 'first_name' => 'S', 'last_name' => 'L', 'student_identifier' => 'STU', 'branch' => 'CS', 'graduation_year' => 2025, 'branch' => 'CS', 'graduation_year' => 2025, 'cgpa' => 9.0]);
        
        $response = $this->actingAs($user)->getJson("/api/v1/recruiters/candidates/{$student->id}");
        $response->assertStatus(200);
        $this->assertEquals(9.0, $response->json('cgpa'));
    }
    
    public function test_update_company() {
        $user = User::create(['email' => 'r@t.com', 'password_hash' => 'x', 'role' => UserRole::RECRUITER->value]);
        $company = Company::create(['name' => 'Old']);
        Recruiter::create(['contact_email' => 'a@t.com', 'user_id' => $user->id, 'company_id' => $company->id, 'first_name' => 'F', 'last_name' => 'L']);
        
        $response = $this->actingAs($user)->putJson("/api/v1/recruiters/me/company", ['name' => 'New']);
        $response->assertStatus(200);
        $this->assertDatabaseHas('companies', ['id' => $company->id, 'name' => 'New']);
    }
}
