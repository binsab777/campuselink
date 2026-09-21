<?php
namespace Tests\Feature;
use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;
use App\Models\User;
use App\Models\Student;
use App\Enums\UserRole;
class SkillTest extends TestCase {
    use RefreshDatabase;
    public function test_student_can_manage_skills() {
        $user = User::factory()->create(['role' => UserRole::STUDENT->value]);
        $student = Student::factory()->create(['user_id' => $user->id]);
        
        $response = $this->actingAs($user)->getJson('/api/v1/students/me/full');
        $response->assertStatus(200)->assertJsonStructure(['skills']);
    }
}
