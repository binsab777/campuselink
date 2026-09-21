<?php
namespace Tests\Feature;
use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;
use App\Models\User;
use App\Models\Student;
use App\Enums\UserRole;
class FastApiParityTest extends TestCase {
    use RefreshDatabase;
    public function test_api_error_contracts() {
        // 401
        $response = $this->getJson('/api/v1/students/me');
        $response->assertStatus(401)->assertJson(['message' => 'Unauthenticated.']); // Laravel default
        
        // 422
        $response = $this->postJson('/api/v1/auth/register', []);
        $response->assertStatus(422)->assertJsonStructure(['message', 'errors' => ['email', 'password', 'role']]);
    }
}
