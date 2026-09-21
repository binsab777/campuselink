<?php
namespace Tests\Feature\Officer;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use App\Models\User;
use App\Models\Student;
use App\Models\Company;
use App\Enums\UserRole;

class OfficerParityTest extends TestCase {
    use RefreshDatabase;
    
    public function test_officer_can_list_students_with_pagination() {
        $officer = clone(User::factory()->create(['role' => UserRole::PLACEMENT_OFFICER->value]));
        $studentUser = clone(User::factory()->create(['role' => UserRole::STUDENT->value]));
        Student::create(['user_id' => $studentUser->id, 'first_name' => 'Alice', 'last_name' => 'Smith', 'student_identifier' => 'STU999', 'branch' => 'ECE', 'graduation_year' => 2026]);
        
        $response = $this->actingAs($officer)->getJson('/api/v1/officer/students?branch=ECE&limit=10&offset=0');
        $response->assertStatus(200);
        $this->assertArrayHasKey('total', $response->json());
        $this->assertArrayHasKey('students', $response->json());
        $this->assertCount(1, $response->json('students'));
    }

    public function test_officer_can_create_company() {
        $officer = clone(User::factory()->create(['role' => UserRole::PLACEMENT_OFFICER->value]));
        $response = $this->actingAs($officer)->postJson('/api/v1/officer/companies', [
            'name' => 'Global Tech',
            'industry' => 'IT',
            'description' => 'Global technology solutions'
        ]);
        $response->assertStatus(201);
        $this->assertDatabaseHas('companies', ['name' => 'Global Tech']);
    }
}
