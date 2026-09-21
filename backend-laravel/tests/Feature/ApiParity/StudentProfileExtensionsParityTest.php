<?php
namespace Tests\Feature\ApiParity;
use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;
use App\Models\User;
use App\Models\Student;
use App\Models\Company;
use App\Models\Recruiter;
use App\Models\Job;
use App\Models\Application;
use App\Enums\UserRole;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;

class StudentProfileExtensionsParityTest extends TestCase {
    use RefreshDatabase;

    public function test_student_can_manage_skills() {
        $user = User::create(['email' => 's@t.com', 'password_hash' => 'x', 'role' => UserRole::STUDENT->value]);
        $student = Student::create(['user_id' => $user->id, 'first_name' => 'S', 'last_name' => 'L', 'student_identifier' => 'STU', 'branch' => 'CS', 'graduation_year' => 2025]);
        
        $res = $this->actingAs($user)->postJson('/api/v1/students/me/skills', ['skill_name' => 'PHP', 'proficiency_level' => 'INTERMEDIATE']);
        $res->assertStatus(200);
        $skillId = $res->json('id');
        $this->assertEquals('PHP', $res->json('skill_name'));
        
        $this->actingAs($user)->getJson('/api/v1/students/me/skills')->assertStatus(200)->assertJsonCount(1);
        $this->actingAs($user)->putJson("/api/v1/students/me/skills/{$skillId}", ['proficiency_level' => 'ADVANCED'])->assertStatus(200);
        $this->actingAs($user)->deleteJson("/api/v1/students/me/skills/{$skillId}")->assertStatus(204);
        $this->actingAs($user)->getJson('/api/v1/students/me/skills')->assertStatus(200)->assertJsonCount(0);
    }
    
    public function test_student_can_manage_projects() {
        $user = User::create(['email' => 's2@t.com', 'password_hash' => 'x', 'role' => UserRole::STUDENT->value]);
        $student = Student::create(['user_id' => $user->id, 'first_name' => 'S', 'last_name' => 'L', 'student_identifier' => 'STU2', 'branch' => 'CS', 'graduation_year' => 2025]);
        
        $res = $this->actingAs($user)->postJson('/api/v1/students/me/projects', ['title' => 'Proj', 'description' => 'Description here']);
        $res->assertStatus(201);
        $projId = $res->json('id');
        $this->assertEquals('Proj', $res->json('title'));
        
        $this->actingAs($user)->getJson('/api/v1/students/me/projects')->assertStatus(200)->assertJsonCount(1);
        $this->actingAs($user)->putJson("/api/v1/students/me/projects/{$projId}", ['title' => 'New Proj'])->assertStatus(200);
        $this->actingAs($user)->deleteJson("/api/v1/students/me/projects/{$projId}")->assertStatus(204);
        $this->actingAs($user)->getJson('/api/v1/students/me/projects')->assertStatus(200)->assertJsonCount(0);
    }
    
    public function test_student_can_manage_certifications() {
        $user = User::create(['email' => 's3@t.com', 'password_hash' => 'x', 'role' => UserRole::STUDENT->value]);
        $student = Student::create(['user_id' => $user->id, 'first_name' => 'S', 'last_name' => 'L', 'student_identifier' => 'STU3', 'branch' => 'CS', 'graduation_year' => 2025]);
        
        $res = $this->actingAs($user)->postJson('/api/v1/students/me/certifications', ['name' => 'Cert', 'issuing_org' => 'Org', 'issue_date' => '2025-01-01']);
        $res->assertStatus(200);
        $certId = $res->json('id');
        
        $this->actingAs($user)->getJson('/api/v1/students/me/certifications')->assertStatus(200)->assertJsonCount(1);
        $this->actingAs($user)->putJson("/api/v1/students/me/certifications/{$certId}", ['name' => 'New Cert'])->assertStatus(200);
        $this->actingAs($user)->deleteJson("/api/v1/students/me/certifications/{$certId}")->assertStatus(204);
        $this->actingAs($user)->getJson('/api/v1/students/me/certifications')->assertStatus(200)->assertJsonCount(0);
    }

    public function test_student_can_manage_academic() {
        $user = User::create(['email' => 's9@t.com', 'password_hash' => 'x', 'role' => UserRole::STUDENT->value]);
        $student = Student::create(['user_id' => $user->id, 'first_name' => 'S', 'last_name' => 'L', 'student_identifier' => 'STU9', 'branch' => 'CS', 'graduation_year' => 2025]);

        $res = $this->actingAs($user)->postJson('/api/v1/students/me/academic', [
            'institution' => 'MIT',
            'qualification' => 'BSc',
            'specialization' => 'CS',
            'start_year' => 2020,
            'score_value' => 95.5,
            'score_type' => 'PERCENTAGE'
        ]);
        $res->assertStatus(200); // Because my StudentAcademicController@store returns 200
        $histId = $res->json('id');

        $this->actingAs($user)->getJson('/api/v1/students/me/academic')->assertStatus(200)->assertJsonCount(1);
        $this->actingAs($user)->putJson("/api/v1/students/me/academic/{$histId}", ['institution_name' => 'Uni 2'])->assertStatus(200);
        $this->actingAs($user)->deleteJson("/api/v1/students/me/academic/{$histId}")->assertStatus(204);
    }

    public function test_student_can_manage_resume() {
        Storage::fake('local');
        $user = User::create(['email' => 's4@t.com', 'password_hash' => 'x', 'role' => UserRole::STUDENT->value]);
        $student = Student::create(['user_id' => $user->id, 'first_name' => 'S', 'last_name' => 'L', 'student_identifier' => 'STU4', 'branch' => 'CS', 'graduation_year' => 2025]);
        
        $largeFile = UploadedFile::fake()->create('large.pdf', 6000, 'application/pdf');
        $this->actingAs($user)->postJson('/api/v1/students/me/resume', ['file' => $largeFile])->assertStatus(422);
        
        $invalidFile = UploadedFile::fake()->create('invalid.txt', 100, 'text/plain');
        $this->actingAs($user)->postJson('/api/v1/students/me/resume', ['file' => $invalidFile])->assertStatus(422);
        
        $file = UploadedFile::fake()->create('resume.pdf', 100, 'application/pdf');
        $res = $this->actingAs($user)->postJson('/api/v1/students/me/resume', ['file' => $file]);
        $res->assertStatus(200);
        
        $downloadUrl = $res->json('resume_url');
        $this->assertEquals('/api/v1/students/' . $student->id . '/resume/download', $downloadUrl);
        Storage::disk('local')->assertExists('resumes/student_' . $student->id . '_resume.pdf');
        
        $user2 = User::create(['email' => 's5@t.com', 'password_hash' => 'x', 'role' => UserRole::STUDENT->value]);
        Student::create(['user_id' => $user2->id, 'first_name' => 'S2', 'last_name' => 'L2', 'student_identifier' => 'STU5', 'branch' => 'CS', 'graduation_year' => 2025]);
        $this->actingAs($user2)->getJson($downloadUrl)->assertStatus(403);
        
        $recruiterUser = User::create(['email' => 'r@t.com', 'password_hash' => 'x', 'role' => UserRole::RECRUITER->value]);
        $company = Company::create(['name' => 'Tech Corp']);
        Recruiter::create(['user_id' => $recruiterUser->id, 'company_id' => $company->id, 'contact_email' => 'r@t.com', 'contact_name' => 'R']);
        $this->actingAs($recruiterUser)->getJson($downloadUrl)->assertStatus(403);
        
        $job = Job::create(['company_id' => $company->id, 'title' => 'T', 'description' => 'D', 'employment_type' => 'Full-time', 'status' => 'PUBLISHED']);
        Application::create(['job_id' => $job->id, 'student_id' => $student->id, 'status' => 'APPLIED']);
        $this->actingAs($recruiterUser)->getJson($downloadUrl)->assertStatus(200);
        
        $this->actingAs($user)->deleteJson('/api/v1/students/me/resume')->assertStatus(204);
        Storage::disk('local')->assertMissing('resumes/student_' . $student->id . '_resume.pdf');
    }
    
    public function test_student_completeness_and_drives() {
        $user = User::create(['email' => 's5x@t.com', 'password_hash' => 'x', 'role' => UserRole::STUDENT->value]);
        $student = Student::create(['user_id' => $user->id, 'first_name' => 'S', 'last_name' => 'L', 'student_identifier' => 'STU5x', 'branch' => 'CS', 'graduation_year' => 2025]);
        
        $this->actingAs($user)->getJson('/api/v1/students/me/completeness')->assertStatus(200);
        $this->actingAs($user)->getJson('/api/v1/students/me/drives')->assertStatus(200);
    }
    
    public function test_update_basic_info() {
        $user = User::create(['email' => 's6x@t.com', 'password_hash' => 'x', 'role' => UserRole::STUDENT->value]);
        $student = Student::create(['user_id' => $user->id, 'first_name' => 'S', 'last_name' => 'L', 'student_identifier' => 'STU6x', 'branch' => 'CS', 'graduation_year' => 2025]);
        
        $this->actingAs($user)->putJson('/api/v1/students/me', ['first_name' => 'New Name'])->assertStatus(200);
        $this->assertDatabaseHas('students', ['id' => $student->id, 'first_name' => 'New Name']);
    }
}
