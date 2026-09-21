<?php

namespace Tests\Feature\Admin;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use App\Models\User;
use App\Enums\UserRole;

class UserUpdateParityTest extends TestCase {
    use RefreshDatabase;
    
    public function test_role_update_endpoint_is_removed() {
        $admin = clone(User::factory()->create(['role' => UserRole::SUPER_ADMIN->value]));
        $target = clone(User::factory()->create(['role' => UserRole::STUDENT->value]));
        
        $response = $this->actingAs($admin)->patchJson("/api/v1/admin/users/{$target->id}/role", [
            'role' => UserRole::PLACEMENT_OFFICER->value
        ]);
        
        $response->assertStatus(404);
    }
    
    public function test_admin_can_view_user_details() {
        $admin = clone(User::factory()->create(['role' => UserRole::SUPER_ADMIN->value]));
        $target = clone(User::factory()->create(['role' => UserRole::STUDENT->value]));
        
        $response = $this->actingAs($admin)->getJson("/api/v1/admin/users/{$target->id}");
        
        $response->assertStatus(200);
        $response->assertJsonFragment(['email' => $target->email]);
    }
    
    public function test_officer_cannot_view_user_details() {
        $officer = clone(User::factory()->create(['role' => UserRole::PLACEMENT_OFFICER->value]));
        $target = clone(User::factory()->create(['role' => UserRole::RECRUITER->value]));
        
        $response = $this->actingAs($officer)->getJson("/api/v1/admin/users/{$target->id}");
        
        $response->assertStatus(403);
    }
    
    public function test_student_cannot_view_user_details() {
        $student = clone(User::factory()->create(['role' => UserRole::STUDENT->value]));
        $target = clone(User::factory()->create(['role' => UserRole::STUDENT->value]));
        
        $response = $this->actingAs($student)->getJson("/api/v1/admin/users/{$target->id}");
        $response->assertStatus(403);
    }

    public function test_super_admin_can_update_user_status() {
        $admin = clone(User::factory()->create(['role' => UserRole::SUPER_ADMIN->value]));
        $target = clone(User::factory()->create(['role' => UserRole::STUDENT->value, 'is_active' => true]));
        
        $response = $this->actingAs($admin)->patchJson("/api/v1/admin/users/{$target->id}/status", [
            'is_active' => false
        ]);
        
        $response->assertStatus(200);
        $this->assertDatabaseHas('users', ['id' => $target->id, 'is_active' => false]);
    }

    public function test_super_admin_cannot_deactivate_self() {
        $admin = clone(User::factory()->create(['role' => UserRole::SUPER_ADMIN->value, 'is_active' => true]));
        
        $response = $this->actingAs($admin)->patchJson("/api/v1/admin/users/{$admin->id}/status", [
            'is_active' => false
        ]);
        
        $response->assertStatus(400);
        $response->assertJsonFragment(['detail' => 'Cannot deactivate your own account']);
    }
}
