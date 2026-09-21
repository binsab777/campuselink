<?php
namespace Tests\Feature\Students;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use App\Models\User;
use App\Models\Student;
use App\Enums\UserRole;

class AcademicParityTest extends TestCase {
    use RefreshDatabase;
    
    public function test_student_can_create_academic_record() {
        $studentUser = User::factory()->create(['role' => UserRole::STUDENT->value]);
        Student::create(['user_id' => $studentUser->id, 'first_name' => 'Alice', 'last_name' => 'Smith', 'student_identifier' => 'STU999', 'branch' => 'ECE', 'graduation_year' => 2026]);
        
        $response = $this->actingAs($studentUser)->postJson('/api/v1/students/me/academic', [
            'institution' => 'MIT',
            'qualification' => 'BSc',
            'specialization' => 'CS',
            'start_year' => 2020,
            'score_value' => 95.5,
            'score_type' => 'PERCENTAGE'
        ]);
        $response->assertStatus(200);
        $this->assertDatabaseHas('student_academic_history', ['institution' => 'MIT', 'qualification' => 'BSc', 'score_value' => 95.5]);
    }
}
