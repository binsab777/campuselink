import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip())

# Projects Controller
write_file('app/Http/Controllers/Api/StudentProjectController.php', """<?php
namespace App\\Http\\Controllers\\Api;
use App\\Http\\Controllers\\Controller;
use Illuminate\\Http\\Request;
use App\\Models\\StudentProject;

class StudentProjectController extends Controller {
    public function index(Request $request) {
        return $request->user()->studentProfile->projects;
    }
    public function store(Request $request) {
        $validated = $request->validate(['title' => 'required|string', 'description' => 'required|string', 'technologies' => 'nullable|array', 'github_url' => 'nullable|url']);
        return response()->json($request->user()->studentProfile->projects()->create($validated), 201);
    }
    public function update(Request $request, $id) {
        $project = $request->user()->studentProfile->projects()->findOrFail($id);
        $project->update($request->validate(['title' => 'sometimes|string', 'description' => 'sometimes|string', 'technologies' => 'nullable|array', 'github_url' => 'nullable|url']));
        return response()->json($project);
    }
    public function destroy(Request $request, $id) {
        $request->user()->studentProfile->projects()->findOrFail($id)->delete();
        return response()->noContent();
    }
}
""")

# Certifications Controller
write_file('app/Http/Controllers/Api/StudentCertificationController.php', """<?php
namespace App\\Http\\Controllers\\Api;
use App\\Http\\Controllers\\Controller;
use Illuminate\\Http\\Request;

class StudentCertificationController extends Controller {
    public function index(Request $request) {
        return $request->user()->studentProfile->certifications;
    }
    public function store(Request $request) {
        $validated = $request->validate(['name' => 'required|string', 'issuing_organization' => 'required|string', 'issue_date' => 'required|date', 'credential_url' => 'nullable|url']);
        return response()->json($request->user()->studentProfile->certifications()->create($validated), 201);
    }
    public function update(Request $request, $id) {
        $cert = $request->user()->studentProfile->certifications()->findOrFail($id);
        $cert->update($request->validate(['name' => 'sometimes|string', 'issuing_organization' => 'sometimes|string', 'issue_date' => 'sometimes|date', 'credential_url' => 'nullable|url']));
        return response()->json($cert);
    }
    public function destroy(Request $request, $id) {
        $request->user()->studentProfile->certifications()->findOrFail($id)->delete();
        return response()->noContent();
    }
}
""")

# Recruiter Company Controller
write_file('app/Http/Controllers/Api/RecruiterCompanyController.php', """<?php
namespace App\\Http\\Controllers\\Api;
use App\\Http\\Controllers\\Controller;
use Illuminate\\Http\\Request;

class RecruiterCompanyController extends Controller {
    public function show(Request $request) {
        return $request->user()->recruiterProfile->company;
    }
    public function update(Request $request) {
        $company = $request->user()->recruiterProfile->company;
        $validated = $request->validate(['name' => 'sometimes|string', 'description' => 'sometimes|string', 'website' => 'nullable|url', 'industry' => 'nullable|string']);
        $company->update($validated);
        return response()->json($company);
    }
}
""")

# Recruiter Jobs Controller
write_file('app/Http/Controllers/Api/RecruiterJobController.php', """<?php
namespace App\\Http\\Controllers\\Api;
use App\\Http\\Controllers\\Controller;
use Illuminate\\Http\\Request;
use App\\Models\\Job;

class RecruiterJobController extends Controller {
    public function index(Request $request) {
        return $request->user()->recruiterProfile->company->jobs;
    }
    public function store(Request $request) {
        $validated = $request->validate([
            'title' => 'required|string', 'description' => 'required|string', 
            'type' => 'required|string', 'location' => 'nullable|string',
            'salary_min' => 'nullable|numeric', 'salary_max' => 'nullable|numeric',
            'deadline' => 'required|date'
        ]);
        $job = $request->user()->recruiterProfile->company->jobs()->create(array_merge($validated, ['status' => 'DRAFT', 'posted_by_id' => $request->user()->recruiterProfile->id]));
        return response()->json($job, 201);
    }
    public function show(Request $request, $id) {
        return $request->user()->recruiterProfile->company->jobs()->findOrFail($id);
    }
    public function update(Request $request, $id) {
        $job = $request->user()->recruiterProfile->company->jobs()->findOrFail($id);
        $job->update($request->validate(['title' => 'sometimes|string', 'description' => 'sometimes|string', 'status' => 'sometimes|string']));
        return response()->json($job);
    }
    public function destroy(Request $request, $id) {
        $request->user()->recruiterProfile->company->jobs()->findOrFail($id)->delete();
        return response()->noContent();
    }
}
""")

# Recruiter Drives Controller
write_file('app/Http/Controllers/Api/RecruiterDriveController.php', """<?php
namespace App\\Http\\Controllers\\Api;
use App\\Http\\Controllers\\Controller;
use Illuminate\\Http\\Request;

class RecruiterDriveController extends Controller {
    public function index(Request $request) {
        return $request->user()->recruiterProfile->company->drives;
    }
    public function store(Request $request) {
        $validated = $request->validate(['name' => 'required|string', 'date' => 'required|date']);
        $drive = $request->user()->recruiterProfile->company->drives()->create($validated);
        return response()->json($drive, 201);
    }
    public function update(Request $request, $id) {
        $drive = $request->user()->recruiterProfile->company->drives()->findOrFail($id);
        $drive->update($request->validate(['name' => 'sometimes|string']));
        return response()->json($drive);
    }
}
""")

write_file('app/Http/Controllers/Api/SkillController.php', """<?php
namespace App\\Http\\Controllers\\Api;
use App\\Http\\Controllers\\Controller;
use Illuminate\\Http\\Request;
use App\\Models\\Skill;

class SkillController extends Controller {
    public function index() { return Skill::all(); }
    public function store(Request $request) { return response()->json(Skill::create($request->validate(['name' => 'required|string', 'category' => 'required|string'])), 201); }
    public function update(Request $request, $id) { $s = Skill::findOrFail($id); $s->update($request->validate(['name' => 'sometimes|string', 'category' => 'sometimes|string'])); return response()->json($s); }
    public function destroy($id) { Skill::findOrFail($id)->delete(); return response()->noContent(); }
}
""")

write_file('app/Http/Controllers/Api/OfficerController.php', """<?php
namespace App\\Http\\Controllers\\Api;
use App\\Http\\Controllers\\Controller;
use Illuminate\\Http\\Request;
use App\\Models\\Student;
use App\\Models\\Company;

class OfficerController extends Controller {
    public function getStudents() { return Student::all(); }
    public function getStudent($id) { return Student::with(['skills.skill', 'projects', 'certifications'])->findOrFail($id); }
    public function getCompanies() { return Company::all(); }
    public function storeCompany(Request $request) { return response()->json(Company::create($request->validate(['name' => 'required|string', 'description' => 'required|string'])), 201); }
}
""")

print("Generated controllers!")
