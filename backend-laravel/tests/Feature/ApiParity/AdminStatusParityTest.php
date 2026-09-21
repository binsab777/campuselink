<?php
namespace Tests\Feature\ApiParity;
use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;
use App\Models\User;
use App\Enums\UserRole;

class AdminStatusParityTest extends TestCase {
    use RefreshDatabase;
    public function test_admin_can_update_status() {
        $admin = User::create(['email' => 'a2@test.com', 'password_hash' => 'x', 'role' => UserRole::SUPER_ADMIN->value]);
        $target = User::create(['email' => 't2@test.com', 'password_hash' => 'x', 'role' => UserRole::STUDENT->value, 'is_active' => true]);
        
        $this->actingAs($admin)->patchJson("/api/v1/admin/users/{$target->id}/status", ['is_active' => false])->assertStatus(200);
        $this->assertDatabaseHas('users', ['id' => $target->id, 'is_active' => false]);
    }
}
