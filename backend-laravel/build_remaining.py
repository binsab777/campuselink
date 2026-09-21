import os

files = {
    # Services
    "app/Services/FileStorageService.php": """<?php
namespace App\\Services;
use Illuminate\\Http\\UploadedFile;
use Illuminate\\Support\\Facades\\Storage;

class FileStorageService {
    public function upload(UploadedFile $file, string $directory, string $filename = null) {
        if (!$file->isValid()) throw new \\Exception("Invalid file upload");
        $name = $filename ?? $file->hashName();
        $path = $file->storeAs($directory, $name, 'public');
        return Storage::url($path);
    }
    public function delete(string $url) {
        $path = str_replace('/storage/', '', parse_url($url, PHP_URL_PATH));
        if (Storage::disk('public')->exists($path)) {
            Storage::disk('public')->delete($path);
        }
    }
}
""",
    # Controllers
    "app/Http/Controllers/Api/StudentResumeController.php": """<?php
namespace App\\Http\\Controllers\\Api;
use App\\Http\\Controllers\\Controller;
use Illuminate\\Http\\Request;
use App\\Services\\FileStorageService;
class StudentResumeController extends Controller {
    public function upload(Request $request, FileStorageService $storage) {
        $request->validate(['resume' => 'required|file|mimes:pdf,doc,docx|max:5120']);
        $student = $request->user()->studentProfile;
        if ($student->resume_url) $storage->delete($student->resume_url);
        $url = $storage->upload($request->file('resume'), 'resumes', 'resume_' . $student->id . '.' . $request->file('resume')->extension());
        $student->update(['resume_url' => $url]);
        return response()->json(['resume_url' => $url]);
    }
}
""",
    "app/Http/Controllers/Api/AdminController.php": """<?php
namespace App\\Http\\Controllers\\Api;
use App\\Http\\Controllers\\Controller;
use Illuminate\\Http\\Request;
use App\\Models\\User;
use App\\Http\\Resources\\UserResource;
class AdminController extends Controller {
    public function index() { return UserResource::collection(User::all()); }
    public function activate(User $user) { $user->update(['is_active' => true]); return new UserResource($user); }
    public function deactivate(User $user) { $user->update(['is_active' => false]); return new UserResource($user); }
}
""",
    # Tests
    "tests/Feature/ResourceOwnershipTest.php": """<?php
namespace Tests\\Feature;
use Tests\\TestCase;
use Illuminate\\Foundation\\Testing\\RefreshDatabase;
use App\\Models\\User;
use App\\Models\\Student;
use App\\Enums\\UserRole;

class ResourceOwnershipTest extends TestCase {
    use RefreshDatabase;
    public function test_student_cannot_view_other_student_profile() {
        $user1 = User::factory()->create(['role' => UserRole::STUDENT->value]);
        $student1 = Student::factory()->create(['user_id' => $user1->id]);
        
        $user2 = User::factory()->create(['role' => UserRole::STUDENT->value]);
        Student::factory()->create(['user_id' => $user2->id]);
        
        // This is hitting a custom endpoint for demonstration or we can just test the policy directly
        $policy = new \\App\\Policies\\StudentPolicy();
        $this->assertTrue($policy->view($user1, $student1));
        
        $student2 = Student::where('user_id', $user2->id)->first();
        $this->assertFalse($policy->view($user1, $student2));
    }

    public function test_admin_can_view_any_student() {
        $admin = User::factory()->create(['role' => UserRole::SUPER_ADMIN->value]);
        $student = Student::factory()->create();
        
        $policy = new \\App\\Policies\\StudentPolicy();
        $this->assertTrue($policy->view($admin, $student));
    }
}
""",
    "tests/Feature/FastApiParityTest.php": """<?php
namespace Tests\\Feature;
use Tests\\TestCase;
use Illuminate\\Foundation\\Testing\\RefreshDatabase;
use App\\Models\\User;
use App\\Models\\Student;
use App\\Enums\\UserRole;
class FastApiParityTest extends TestCase {
    use RefreshDatabase;
    public function test_api_error_contracts() {
        // 401
        $response = $this->getJson('/api/v1/students/me');
        $response->assertStatus(401)->assertJson(['message' => 'Unauthenticated.']); // Laravel default
        
        // 422
        $response = $this->postJson('/api/v1/auth/register', []);
        $response->assertStatus(422)->assertJsonStructure(['message', 'errors' => ['email', 'password', 'role']]);
    }
}
"""
}

for filepath, content in files.items():
    os.makedirs(os.path.dirname(f"d:/xampp/htdocs/campuslink/backend-laravel/{filepath}"), exist_ok=True)
    with open(f"d:/xampp/htdocs/campuslink/backend-laravel/{filepath}", 'w') as f:
        f.write(content)

print("Remaining files generated.")
