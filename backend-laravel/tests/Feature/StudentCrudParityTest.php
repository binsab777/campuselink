<?php
namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use App\Models\User;
use App\Models\Student;
use App\Models\Skill;
use App\Models\StudentProject;
use App\Enums\UserRole;

class StudentCrudParityTest extends TestCase
{
    use RefreshDatabase;

    private $studentUser;
    private $otherStudentUser;
    private $studentProfile;

    protected function setUp(): void
    {
        parent::setUp();
        
        $this->studentUser = clone(User::factory()->create(['role' => UserRole::STUDENT->value]));
        $this->studentProfile = clone(Student::factory()->create(['user_id' => $this->studentUser->id]));
        
        $this->otherStudentUser = clone(User::factory()->create(['role' => UserRole::STUDENT->value]));
        Student::factory()->create(['user_id' => $this->otherStudentUser->id]);
    }

    public function test_student_can_add_and_list_projects()
    {
        $payload = [
            'title' => 'Parity Project',
            'description' => 'A project for parity testing',
            'technologies' => ['PHP', 'Laravel'],
            'github_url' => 'https://github.com/test/project'
        ];

        $response = $this->actingAs($this->studentUser)->postJson('/api/v1/students/me/projects', $payload);
        
        $response->assertStatus(201);
        $this->assertDatabaseHas('student_projects', ['title' => 'Parity Project', 'student_id' => $this->studentProfile->id]);

        $listResponse = $this->actingAs($this->studentUser)->getJson('/api/v1/students/me/projects');
        $listResponse->assertStatus(200);
        $this->assertCount(1, $listResponse->json());
    }

    public function test_student_cannot_delete_other_students_project()
    {
        $project = StudentProject::create([
            'student_id' => $this->studentProfile->id,
            'title' => 'My Project',
            'description' => 'Test'
        ]);

        $response = $this->actingAs($this->otherStudentUser)->deleteJson('/api/v1/students/me/projects/' . $project->id);
        
        $response->assertStatus(404); // Using findOrFail scoped to user's projects returns 404
        $this->assertDatabaseHas('student_projects', ['id' => $project->id]);
    }

    public function test_student_can_add_certification()
    {
        $payload = [
            'name' => 'AWS Certified',
            'issuing_org' => 'Amazon',
            'issue_date' => '2023-01-01',
            'credential_id' => 'aws-123'
        ];

        $response = $this->actingAs($this->studentUser)->postJson('/api/v1/students/me/certifications', $payload);
        $response->assertStatus(200);
        $this->assertDatabaseHas('student_certifications', ['name' => 'AWS Certified', 'student_id' => $this->studentProfile->id]);
    }
}
