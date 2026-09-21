<?php
namespace Tests\Feature\Admin;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use App\Models\User;
use App\Enums\UserRole;

class UserUpdateParityTest extends TestCase {
    use RefreshDatabase;
    
    public function test_super_admin_can_update_user_role() {
        $admin = clone(User::factory()->create(['role' => UserRole::SUPER_ADMIN->value]));
        $target = clone(User::factory()->create(['role' => UserRole::STUDENT->value]));
        
        $response = $this->actingAs($admin)->patchJson("/api/v1/admin/users/{$target->id}/role", [
            'role' => UserRole::PLACEMENT_OFFICER->value
        ]);
        
        $response->assertStatus(200);
        $this->assertDatabaseHas('users', ['id' => $target->id, 'role' => UserRole::PLACEMENT_OFFICER->value]);
    }

    public function test_placement_officer_cannot_update_roles() {
        $officer = clone(User::factory()->create(['role' => UserRole::PLACEMENT_OFFICER->value]));
        $target = clone(User::factory()->create(['role' => UserRole::STUDENT->value]));
        $response = $this->actingAs($officer)->patchJson("/api/v1/admin/users/{$target->id}/role", [
            'role' => UserRole::SUPER_ADMIN->value
        ]);
        $response->assertStatus(403);
    }
    
    public function test_recruiter_cannot_update_roles() {
        $recruiter = clone(User::factory()->create(['role' => UserRole::RECRUITER->value]));
        $target = clone(User::factory()->create(['role' => UserRole::STUDENT->value]));
        $response = $this->actingAs($recruiter)->patchJson("/api/v1/admin/users/{$target->id}/role", [
            'role' => UserRole::SUPER_ADMIN->value
        ]);
        $response->assertStatus(403);
    }

    public function test_student_cannot_update_roles() {
        $student = clone(User::factory()->create(['role' => UserRole::STUDENT->value]));
        $target = clone(User::factory()->create(['role' => UserRole::STUDENT->value]));
        $response = $this->actingAs($student)->patchJson("/api/v1/admin/users/{$target->id}/role", [
            'role' => UserRole::SUPER_ADMIN->value
        ]);
        $response->assertStatus(403);
    }
}
