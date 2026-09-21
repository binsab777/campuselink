<?php
namespace Database\Factories;
use App\Models\User;
use App\Enums\UserRole;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Facades\Hash;
class UserFactory extends Factory {
    protected $model = User::class;
    public function definition() {
        return [
            'email' => $this->faker->unique()->safeEmail,
            'password_hash' => Hash::make('password'),
            'role' => UserRole::STUDENT->value,
            'is_active' => true,
        ];
    }
}
