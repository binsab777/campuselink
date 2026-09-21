<?php
namespace Tests\Feature\Admin;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use App\Models\User;
use App\Models\Skill;
use App\Enums\UserRole;

class SkillParityTest extends TestCase {
    use RefreshDatabase;
    
    public function test_officer_can_create_and_list_skills() {
        $officer = clone(User::factory()->create(['role' => UserRole::PLACEMENT_OFFICER->value]));
        
        $response = $this->actingAs($officer)->postJson('/api/v1/skills', [
            'name' => 'Python',
            'category' => 'Programming',
            'description' => 'Python programming language'
        ]);
        $response->assertStatus(201);
        
        $listResponse = $this->actingAs($officer)->getJson('/api/v1/skills');
        $listResponse->assertStatus(200);
    }

    public function test_student_cannot_create_skills() {
        $student = clone(User::factory()->create(['role' => UserRole::STUDENT->value]));
        $response = $this->actingAs($student)->postJson('/api/v1/skills', [
            'name' => 'Java', 'category' => 'Programming'
        ]);
        $response->assertStatus(403);
    }
}
