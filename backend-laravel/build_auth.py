import os

files = {
    "app/Http/Requests/Auth/RegisterRequest.php": """<?php
namespace App\\Http\\Requests\\Auth;

use Illuminate\\Foundation\\Http\\FormRequest;
use Illuminate\\Validation\\Rules\\Enum;
use App\\Enums\\UserRole;

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
""",
    "app/Http/Requests/Auth/LoginRequest.php": """<?php
namespace App\\Http\\Requests\\Auth;

use Illuminate\\Foundation\\Http\\FormRequest;

class LoginRequest extends FormRequest {
    public function authorize() { return true; }
    public function rules() {
        return [
            'username' => 'required|email',
            'password' => 'required|string',
        ];
    }
}
""",
    "app/Http/Resources/UserResource.php": """<?php
namespace App\\Http\\Resources;

use Illuminate\\Http\\Resources\\Json\\JsonResource;

class UserResource extends JsonResource {
    public function toArray($request) {
        return [
            'id' => $this->id,
            'email' => $this->email,
            'role' => $this->role,
            'is_active' => $this->is_active,
        ];
    }
}
""",
    "app/Http/Controllers/Api/AuthController.php": """<?php
namespace App\\Http\\Controllers\\Api;

use App\\Http\\Controllers\\Controller;
use App\\Http\\Requests\\Auth\\RegisterRequest;
use App\\Http\\Requests\\Auth\\LoginRequest;
use App\\Http\\Resources\\UserResource;
use App\\Models\\User;
use App\\Models\\Student;
use App\\Models\\Company;
use App\\Models\\Recruiter;
use App\\Enums\\UserRole;
use Illuminate\\Support\\Facades\\Hash;
use Illuminate\\Support\\Facades\\DB;
use Illuminate\\Http\\Request;
use Illuminate\\Validation\\ValidationException;

class AuthController extends Controller {
    public function register(RegisterRequest $request) {
        $validated = $request->validated();

        return DB::transaction(function () use ($validated) {
            $user = User::create([
                'email' => $validated['email'],
                'password_hash' => Hash::make($validated['password']),
                'role' => $validated['role'],
            ]);

            if ($validated['role'] === UserRole::STUDENT->value) {
                Student::create([
                    'user_id' => $user->id,
                    'student_identifier' => 'STU' . str_pad($user->id, 4, '0', STR_PAD_LEFT),
                    'first_name' => $validated['first_name'],
                    'last_name' => $validated['last_name'],
                    'branch' => $validated['branch'],
                    'graduation_year' => $validated['graduation_year'],
                ]);
            } elseif ($validated['role'] === UserRole::RECRUITER->value) {
                $company = Company::firstOrCreate(
                    ['name' => $validated['company_name']],
                    ['description' => '', 'industry' => 'Technology']
                );
                
                Recruiter::create([
                    'user_id' => $user->id,
                    'company_id' => $company->id,
                    'contact_name' => $validated['contact_name'],
                    'contact_email' => $validated['email'],
                    'contact_phone' => $validated['contact_phone'] ?? null,
                ]);
            }

            // FastAPI returns {"message": "...", "user": {...}} 
            return response()->json([
                'message' => 'User registered successfully',
                'user' => new UserResource($user)
            ], 201);
        });
    }

    public function login(LoginRequest $request) {
        $user = User::where('email', $request->username)->first();

        if (!$user || !Hash::check($request->password, $user->password_hash)) {
            // Replicate FastAPI OAuth2PasswordRequestForm 400 error behavior
            return response()->json(['detail' => 'Incorrect email or password'], 400);
        }

        if (!$user->is_active) {
            return response()->json(['detail' => 'Inactive user'], 400);
        }

        $token = $user->createToken('auth_token')->plainTextToken;

        return response()->json([
            'access_token' => $token,
            'token_type' => 'bearer',
            'user' => new UserResource($user)
        ]);
    }

    public function me(Request $request) {
        return new UserResource($request->user());
    }
}
""",
}

for filepath, content in files.items():
    os.makedirs(os.path.dirname(f"d:/xampp/htdocs/campuslink/backend-laravel/{filepath}"), exist_ok=True)
    with open(f"d:/xampp/htdocs/campuslink/backend-laravel/{filepath}", 'w') as f:
        f.write(content)

print("Auth Controller, Requests, and Resources generated.")
