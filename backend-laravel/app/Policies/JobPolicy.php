<?php
namespace App\Policies;
use App\Models\User;
use App\Models\Job;
use App\Enums\UserRole;

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
