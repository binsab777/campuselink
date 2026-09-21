<?php
namespace Database\Factories;
use App\Models\Student;
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;
class StudentFactory extends Factory {
    protected $model = Student::class;
    public function definition() {
        return [
            'user_id' => User::factory(),
            'student_identifier' => 'STU' . $this->faker->unique()->numberBetween(1000, 9999),
            'first_name' => $this->faker->firstName,
            'last_name' => $this->faker->lastName,
            'branch' => 'Computer Science',
            'graduation_year' => 2025,
            'cgpa' => $this->faker->randomFloat(2, 6, 9.9),
            'backlogs_current' => 0,
            'backlogs_history' => 0,
            'phone' => $this->faker->phoneNumber,
        ];
    }
}
