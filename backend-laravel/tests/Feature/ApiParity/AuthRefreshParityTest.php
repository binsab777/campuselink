<?php
namespace Tests\Feature\ApiParity;
use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;
use App\Models\User;

class AuthRefreshParityTest extends TestCase {
    use RefreshDatabase;
    public function test_auth_refresh() {
        // Just verify endpoint exists and returns 401 unauth or works with token
        $this->postJson('/api/v1/auth/refresh')->assertStatus(401);
        
        $user = User::factory()->create(['password_hash' => \Illuminate\Support\Facades\Hash::make('password')]);
        $response = $this->postJson('/api/v1/auth/login', ['username' => $user->email, 'password' => 'password']);
        $response->assertStatus(200);
        $refreshToken = $response->json('refresh_token');
        
        $this->postJson('/api/v1/auth/refresh', ['refresh_token' => $refreshToken])
            ->assertStatus(200)
            ->assertJsonStructure(['access_token', 'refresh_token', 'token_type']);
    }
}
