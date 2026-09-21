<?php
namespace Tests\Feature\ApiParity;
use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;
use App\Models\User;
use App\Models\Recruiter;
use App\Models\Company;
use App\Enums\UserRole;

class RecruiterMeParityTest extends TestCase {
    use RefreshDatabase;
    public function test_recruiter_me() {
        $user = User::create(['email' => 'r@t.com', 'password_hash' => 'x', 'role' => UserRole::RECRUITER->value]);
        $company = Company::create(['name' => 'C']);
        Recruiter::create(['contact_email' => 'a@t.com', 'user_id' => $user->id, 'company_id' => $company->id, 'contact_name' => 'F L']);
        
        $this->actingAs($user)->getJson('/api/v1/recruiters/me')->assertStatus(200)->assertJsonFragment(['contact_name' => 'F L']);
    }
}
