<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use App\Models\User;
use App\Models\Student;
use App\Enums\UserRole;
use Illuminate\Support\Facades\Hash;

class AuthTest extends TestCase
{
    use RefreshDatabase;

    public function test_student_registration_cascade()
    {
        $response = $this->postJson('/api/v1/auth/register', [
            'email' => 'newstudent@college.edu',
            'password' => 'secret123',
            'role' => UserRole::STUDENT->value,
            'first_name' => 'New',
            'last_name' => 'Student',
            'branch' => 'Computer Science',
            'graduation_year' => 2026,
        ]);

        $response->assertStatus(201)
                 ->assertJsonStructure(['message', 'user' => ['id', 'email', 'role']]);

        // Verify database cascade
        $this->assertDatabaseHas('users', ['email' => 'newstudent@college.edu']);
        $this->assertDatabaseHas('students', [
            'first_name' => 'New',
            'branch' => 'Computer Science',
        ]);
        
        $student = Student::first();
        $this->assertEquals('STU' . str_pad($student->user_id, 4, '0', STR_PAD_LEFT), $student->student_identifier);
    }

    public function test_login_returns_token()
    {
        $user = User::create([
            'email' => 'test@example.com',
            'password_hash' => Hash::make('password'),
            'role' => UserRole::STUDENT->value,
        ]);

        $response = $this->postJson('/api/v1/auth/login', [
            'username' => 'test@example.com',
            'password' => 'password',
        ]);

        $response->assertStatus(200)
                 ->assertJsonStructure(['access_token', 'refresh_token', 'token_type']);
    }

    public function test_me_endpoint_requires_auth()
    {
        $response = $this->getJson('/api/v1/auth/me');
        $response->assertStatus(401);
    }
}
