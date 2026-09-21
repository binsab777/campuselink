<?php
namespace Tests\Feature;
use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;
use App\Models\User;
use App\Enums\UserRole;
class AdminTest extends TestCase {
    use RefreshDatabase;
    public function test_admin_can_view_users() {
        $admin = User::factory()->create(['role' => UserRole::SUPER_ADMIN->value]);
        $response = $this->actingAs($admin)->getJson('/api/v1/admin/users');
        $response->assertStatus(200);
    }
    public function test_student_cannot_view_users() {
        $student = User::factory()->create(['role' => UserRole::STUDENT->value]);
        $response = $this->actingAs($student)->getJson('/api/v1/admin/users');
        $response->assertStatus(403);
    }
}
