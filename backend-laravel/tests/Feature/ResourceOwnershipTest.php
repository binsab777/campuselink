<?php
namespace Tests\Feature;
use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;
use App\Models\User;
use App\Models\Student;
use App\Enums\UserRole;

class ResourceOwnershipTest extends TestCase {
    use RefreshDatabase;
    public function test_student_cannot_view_other_student_profile() {
        $user1 = User::factory()->create(['role' => UserRole::STUDENT->value]);
        $student1 = Student::factory()->create(['user_id' => $user1->id]);
        
        $user2 = User::factory()->create(['role' => UserRole::STUDENT->value]);
        Student::factory()->create(['user_id' => $user2->id]);
        
        // This is hitting a custom endpoint for demonstration or we can just test the policy directly
        $policy = new \App\Policies\StudentPolicy();
        $this->assertTrue($policy->view($user1, $student1));
        
        $student2 = Student::where('user_id', $user2->id)->first();
        $this->assertFalse($policy->view($user1, $student2));
    }

    public function test_admin_can_view_any_student() {
        $admin = User::factory()->create(['role' => UserRole::SUPER_ADMIN->value]);
        $student = Student::factory()->create();
        
        $policy = new \App\Policies\StudentPolicy();
        $this->assertTrue($policy->view($admin, $student));
    }
}
