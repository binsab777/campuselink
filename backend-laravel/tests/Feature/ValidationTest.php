<?php
namespace Tests\Feature;
use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;
use App\Models\User;
use App\Enums\UserRole;
class ValidationTest extends TestCase {
    use RefreshDatabase;
    public function test_registration_validation() {
        $response = $this->postJson('/api/v1/auth/register', [
            'email' => 'invalid-email',
            'password' => '123' // too short
        ]);
        $response->assertStatus(422)
                 ->assertJsonValidationErrors(['email', 'password', 'role']);
    }
}
