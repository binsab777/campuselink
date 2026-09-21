<?php
namespace Tests\Feature;
use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;
use App\Models\User;
use App\Models\Job;
use App\Enums\UserRole;
class JobTest extends TestCase {
    use RefreshDatabase;
    public function test_jobs_listed() {
        $user = User::factory()->create(['role' => UserRole::STUDENT->value]);
        $response = $this->actingAs($user)->getJson('/api/v1/jobs/available');
        $response->assertStatus(200);
    }
}
