<?php
namespace Database\Factories;
use App\Models\Job;
use App\Models\Company;
use App\Enums\JobStatus;
use Illuminate\Database\Eloquent\Factories\Factory;
class JobFactory extends Factory {
    protected $model = Job::class;
    public function definition() {
        return [
            'company_id' => Company::factory(),
            'title' => $this->faker->jobTitle,
            'description' => $this->faker->paragraph,
            'employment_type' => 'Full-time',
            'location' => $this->faker->city,
            'salary_range' => '$80k - $120k',
            'status' => JobStatus::PUBLISHED->value,
            'eligibility_config' => ['min_cgpa' => 7.0, 'allowed_branches' => ['Computer Science', 'IT']],
        ];
    }
}
