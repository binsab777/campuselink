<?php
namespace App\Http\Requests\Auth;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rules\Enum;
use App\Enums\UserRole;

class RegisterRequest extends FormRequest {
    public function authorize() { return true; }
    public function rules() {
        return [
            'email' => 'required|email|unique:users,email',
            'password' => 'required|min:8',
            'role' => ['required', new Enum(UserRole::class)],
            // Student specific
            'first_name' => 'required_if:role,STUDENT|string|max:100',
            'last_name' => 'required_if:role,STUDENT|string|max:100',
            'branch' => 'required_if:role,STUDENT|string|max:100',
            'graduation_year' => 'required_if:role,STUDENT|integer|min:2020|max:2030',
            // Recruiter specific
            'company_name' => 'required_if:role,RECRUITER|string|max:100',
            'contact_name' => 'required_if:role,RECRUITER|string|max:100',
            'contact_phone' => 'nullable|string|max:20',
        ];
    }
}
