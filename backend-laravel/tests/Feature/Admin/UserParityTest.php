<?php
namespace Tests\Feature\Admin;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use App\Models\User;
use App\Enums\UserRole;

class UserParityTest extends TestCase {
    use RefreshDatabase;
    
    public function test_super_admin_can_list_users() {
        $admin = clone(User::factory()->create(['role' => UserRole::SUPER_ADMIN->value]));
        User::factory()->count(3)->create(['role' => UserRole::STUDENT->value]);
        
        $response = $this->actingAs($admin)->getJson('/api/v1/admin/users');
        $response->assertStatus(200);
        $response->assertJsonStructure(['total', 'users']);
        $this->assertGreaterThanOrEqual(4, $response->json('total'));
        $this->assertGreaterThanOrEqual(4, count($response->json('users')));
    }
    
    public function test_super_admin_can_paginate_users() {
        $admin = clone(User::factory()->create(['role' => UserRole::SUPER_ADMIN->value]));
        User::factory()->count(10)->create(['role' => UserRole::STUDENT->value]);
        
        $response = $this->actingAs($admin)->getJson('/api/v1/admin/users?limit=5&offset=2');
        $response->assertStatus(200);
        $this->assertGreaterThanOrEqual(11, $response->json('total'));
        $this->assertCount(5, $response->json('users'));
    }

    public function test_super_admin_can_filter_and_search_users() {
        $admin = clone(User::factory()->create(['role' => UserRole::SUPER_ADMIN->value]));
        User::factory()->create(['role' => UserRole::STUDENT->value, 'email' => 'special_student_test@example.com']);
        
        $response = $this->actingAs($admin)->getJson('/api/v1/admin/users?role=STUDENT&query=special');
        $response->assertStatus(200);
        $this->assertEquals(1, $response->json('total'));
        $this->assertCount(1, $response->json('users'));
        $this->assertEquals('special_student_test@example.com', $response->json('users.0.email'));
    }
    
    public function test_student_cannot_access_admin_users() {
        $student = clone(User::factory()->create(['role' => UserRole::STUDENT->value]));
        $response = $this->actingAs($student)->getJson('/api/v1/admin/users');
        $response->assertStatus(403);
    }
}
