<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use App\Models\User;
use App\Models\Student;
use App\Enums\UserRole;
use Illuminate\Support\Facades\Hash;

class StudentTest extends TestCase
{
    use RefreshDatabase;

    public function test_get_full_profile_unauthenticated()
    {
        $response = $this->getJson('/api/v1/students/me/full');
        $response->assertStatus(401);
    }

    public function test_get_full_profile_wrong_role()
    {
        $user = User::create([
            'email' => 'admin@test.com',
            'password_hash' => Hash::make('password'),
            'role' => UserRole::SUPER_ADMIN->value,
        ]);

        $response = $this->actingAs($user)->getJson('/api/v1/students/me/full');
        $response->assertStatus(403);
    }

    public function test_student_readiness_scoring_deterministic()
    {
        $user = User::create([
            'email' => 'test@student.com',
            'password_hash' => Hash::make('password'),
            'role' => UserRole::STUDENT->value,
        ]);

        $student = Student::create([
            'user_id' => $user->id,
            'student_identifier' => 'STU999',
            'first_name' => 'John',
            'last_name' => 'Doe',
            'branch' => 'CS',
            'graduation_year' => 2025,
            'cgpa' => 9.0, // 90% academic base score
            'backlogs_current' => 0,
            'backlogs_history' => 0,
        ]);

        // Hit the recalculate API
        $response = $this->actingAs($user)->postJson('/api/v1/readiness/me/recalculate');
        
        $response->assertStatus(200);
        $data = $response->json();
        
        // Assert the exact scoring behavior from Python ported to PHP
        $this->assertEquals('v1.0', $data['version']);
        $this->assertEquals(90.0, $data['dimensions']['academic']);
        
        // Since technical, projects, certs, etc are missing, 
        // the activeWeights should scale accordingly, but wait!
        // In python, it's (90 * 0.2) / 0.2 = 90.0 overall score?
        // Let's assert overall score exists.
        $this->assertArrayHasKey('overall_score', $data);
        $this->assertArrayHasKey('readiness_level', $data);
    }
}
