import os

def create_controller(name, content):
    path = f'app/Http/Controllers/Api/{name}.php'
    with open(path, 'w') as f:
        f.write(content)

# Generate Student CRUD controllers
create_controller('StudentSkillController', """<?php
namespace App\\Http\\Controllers\\Api;
use App\\Http\\Controllers\\Controller;
use Illuminate\\Http\\Request;
use App\\Models\\StudentSkill;
use Illuminate\\Validation\\Rule;
use App\\Enums\\ProficiencyLevel;

class StudentSkillController extends Controller {
    public function store(Request $request) {
        $student = $request->user()->studentProfile;
        $validated = $request->validate([
            'skill_id' => 'required|exists:skills,id',
            'proficiency_level' => ['required', Rule::enum(ProficiencyLevel::class)],
            'years_experience' => 'nullable|numeric|min:0',
        ]);
        
        $skill = $student->skills()->create($validated);
        return response()->json($skill, 201);
    }

    public function destroy(Request $request, $id) {
        $student = $request->user()->studentProfile;
        $student->skills()->where('id', $id)->delete();
        return response()->json(null, 204);
    }
}
""")

create_controller('StudentProjectController', """<?php
namespace App\\Http\\Controllers\\Api;
use App\\Http\\Controllers\\Controller;
use Illuminate\\Http\\Request;
use App\\Models\\StudentProject;

class StudentProjectController extends Controller {
    public function store(Request $request) {
        $student = $request->user()->studentProfile;
        $validated = $request->validate([
            'title' => 'required|string|max:255',
            'description' => 'required|string',
            'technologies' => 'nullable|array',
            'github_url' => 'nullable|url',
        ]);
        
        $project = $student->projects()->create($validated);
        return response()->json($project, 201);
    }

    public function destroy(Request $request, $id) {
        $student = $request->user()->studentProfile;
        $student->projects()->where('id', $id)->delete();
        return response()->json(null, 204);
    }
}
""")

# Route appender
with open('routes/api.php', 'r') as f:
    routes = f.read()

inject = """
        Route::post('/me/skills', [\\App\\Http\\Controllers\\Api\\StudentSkillController::class, 'store']);
        Route::delete('/me/skills/{id}', [\\App\\Http\\Controllers\\Api\\StudentSkillController::class, 'destroy']);
        Route::post('/me/projects', [\\App\\Http\\Controllers\\Api\\StudentProjectController::class, 'store']);
        Route::delete('/me/projects/{id}', [\\App\\Http\\Controllers\\Api\\StudentProjectController::class, 'destroy']);
"""

routes = routes.replace("Route::post('/me/resume', [StudentResumeController::class, 'upload']);", "Route::post('/me/resume', [StudentResumeController::class, 'upload']);" + inject)

with open('routes/api.php', 'w') as f:
    f.write(routes)
