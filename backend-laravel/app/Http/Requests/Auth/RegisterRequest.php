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
            'password' => 'required|min:6',
            'role' => ['required', new Enum(UserRole::class)],
        ];
    }
}
