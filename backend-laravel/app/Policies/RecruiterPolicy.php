<?php
namespace App\Policies;
use App\Models\User;
use App\Models\Recruiter;
use App\Enums\UserRole;

class RecruiterPolicy {
    public function view(User $user, Recruiter $recruiter) {
        if ($user->role === UserRole::SUPER_ADMIN->value || $user->role === UserRole::PLACEMENT_OFFICER->value) return true;
        return $user->id === $recruiter->user_id;
    }
    public function update(User $user, Recruiter $recruiter) {
        return $user->id === $recruiter->user_id;
    }
}
