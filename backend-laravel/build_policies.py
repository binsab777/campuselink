import os

policies = {
    "StudentPolicy.php": """<?php
namespace App\\Policies;
use App\\Models\\User;
use App\\Models\\Student;
use App\\Enums\\UserRole;

class StudentPolicy {
    public function view(User $user, Student $student) {
        if ($user->role === UserRole::SUPER_ADMIN->value || $user->role === UserRole::PLACEMENT_OFFICER->value) return true;
        if ($user->role === UserRole::STUDENT->value) return $user->id === $student->user_id;
        return false;
    }
    public function update(User $user, Student $student) {
        return $user->id === $student->user_id;
    }
}
""",
    "RecruiterPolicy.php": """<?php
namespace App\\Policies;
use App\\Models\\User;
use App\\Models\\Recruiter;
use App\\Enums\\UserRole;

class RecruiterPolicy {
    public function view(User $user, Recruiter $recruiter) {
        if ($user->role === UserRole::SUPER_ADMIN->value || $user->role === UserRole::PLACEMENT_OFFICER->value) return true;
        return $user->id === $recruiter->user_id;
    }
    public function update(User $user, Recruiter $recruiter) {
        return $user->id === $recruiter->user_id;
    }
}
""",
    "JobPolicy.php": """<?php
namespace App\\Policies;
use App\\Models\\User;
use App\\Models\\Job;
use App\\Enums\\UserRole;

class JobPolicy {
    public function update(User $user, Job $job) {
        if ($user->role === UserRole::SUPER_ADMIN->value) return true;
        if ($user->role === UserRole::RECRUITER->value) {
            return $user->recruiterProfile && $user->recruiterProfile->company_id === $job->company_id;
        }
        return false;
    }
    public function viewCandidates(User $user, Job $job) {
        if (in_array($user->role, [UserRole::SUPER_ADMIN->value, UserRole::PLACEMENT_OFFICER->value])) return true;
        if ($user->role === UserRole::RECRUITER->value) {
            return $user->recruiterProfile && $user->recruiterProfile->company_id === $job->company_id;
        }
        return false;
    }
}
"""
}

os.makedirs("app/Policies", exist_ok=True)
for name, content in policies.items():
    with open(f"app/Policies/{name}", 'w') as f:
        f.write(content)
print("Policies generated.")
