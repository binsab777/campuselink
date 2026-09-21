<?php
namespace App\Policies;
use App\Models\User;
use App\Models\Student;
use App\Enums\UserRole;

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
