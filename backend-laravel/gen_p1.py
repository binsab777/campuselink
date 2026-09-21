import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip())

# Generate API Resources to ensure camelCase/snake_case parity if needed
write_file('app/Http/Resources/SkillResource.php', """<?php
namespace App\\Http\\Resources;
use Illuminate\\Http\\Resources\\Json\\JsonResource;
class SkillResource extends JsonResource {
    public function toArray($request) {
        return parent::toArray($request);
    }
}
""")

write_file('app/Http/Resources/StudentProjectResource.php', """<?php
namespace App\\Http\\Resources;
use Illuminate\\Http\\Resources\\Json\\JsonResource;
class StudentProjectResource extends JsonResource {
    public function toArray($request) {
        return parent::toArray($request);
    }
}
""")

write_file('app/Http/Resources/StudentCertificationResource.php', """<?php
namespace App\\Http\\Resources;
use Illuminate\\Http\\Resources\\Json\\JsonResource;
class StudentCertificationResource extends JsonResource {
    public function toArray($request) {
        return parent::toArray($request);
    }
}
""")

# We need a big Controller for Student records
write_file('app/Http/Controllers/Api/StudentAcademicController.php', """<?php
namespace App\\Http\\Controllers\\Api;
use App\\Http\\Controllers\\Controller;
use Illuminate\\Http\\Request;
use App\\Http\\Resources\\AcademicHistoryResource;

class StudentAcademicController extends Controller {
    public function store(Request $request) {
        $student = $request->user()->studentProfile;
        $validated = $request->validate([
            'institution_name' => 'required|string',
            'degree' => 'required|string',
            'field_of_study' => 'nullable|string',
            'start_date' => 'required|date',
            'end_date' => 'nullable|date|after_or_equal:start_date',
            'score' => 'nullable|numeric',
            'score_type' => 'nullable|string'
        ]);
        $history = $student->academicHistory()->create($validated);
        return new AcademicHistoryResource($history);
    }

    public function update(Request $request, $id) {
        $student = $request->user()->studentProfile;
        $history = $student->academicHistory()->findOrFail($id);
        $validated = $request->validate([
            'institution_name' => 'sometimes|string',
            'degree' => 'sometimes|string',
            'field_of_study' => 'nullable|string',
            'start_date' => 'sometimes|date',
            'end_date' => 'nullable|date|after_or_equal:start_date',
            'score' => 'nullable|numeric',
            'score_type' => 'nullable|string'
        ]);
        $history->update($validated);
        return new AcademicHistoryResource($history);
    }

    public function destroy(Request $request, $id) {
        $student = $request->user()->studentProfile;
        $student->academicHistory()->findOrFail($id)->delete();
        return response()->noContent();
    }
}
""")

write_file('app/Http/Controllers/Api/StudentSkillController.php', """<?php
namespace App\\Http\\Controllers\\Api;
use App\\Http\\Controllers\\Controller;
use Illuminate\\Http\\Request;
use App\\Models\\Skill;
use App\\Enums\\ProficiencyLevel;
use Illuminate\\Validation\\Rule;

class StudentSkillController extends Controller {
    public function index(Request $request) {
        $student = $request->user()->studentProfile;
        $student->load('skills.skill');
        return $student->skills->map(function($ss) {
            return [
                'id' => $ss->id,
                'skill_id' => $ss->skill_id,
                'skill_name' => $ss->skill->name,
                'proficiency_level' => $ss->proficiency_level,
                'months_experience' => $ss->months_experience,
                'source' => $ss->source
            ];
        });
    }

    public function store(Request $request) {
        $student = $request->user()->studentProfile;
        $validated = $request->validate([
            'skill_name' => 'required|string',
            'proficiency_level' => ['required', Rule::enum(ProficiencyLevel::class)],
            'months_experience' => 'nullable|integer|min:0'
        ]);

        $skillName = strtoupper(trim($validated['skill_name']));
        $skill = Skill::firstOrCreate(['name' => $skillName], ['category' => 'GENERAL']);

        if ($student->skills()->where('skill_id', $skill->id)->exists()) {
            return response()->json(['message' => 'Skill already exists for student'], 409);
        }

        $studentSkill = $student->skills()->create([
            'skill_id' => $skill->id,
            'proficiency_level' => $validated['proficiency_level'],
            'months_experience' => $validated['months_experience'] ?? 0,
            'source' => 'MANUAL'
        ]);

        $studentSkill->load('skill');
        return response()->json([
            'id' => $studentSkill->id,
            'skill_id' => $studentSkill->skill_id,
            'skill_name' => $studentSkill->skill->name,
            'proficiency_level' => $studentSkill->proficiency_level,
            'months_experience' => $studentSkill->months_experience,
            'source' => $studentSkill->source
        ]);
    }

    public function update(Request $request, $id) {
        $student = $request->user()->studentProfile;
        $studentSkill = $student->skills()->findOrFail($id);
        $validated = $request->validate([
            'proficiency_level' => ['sometimes', Rule::enum(ProficiencyLevel::class)],
            'months_experience' => 'nullable|integer|min:0'
        ]);
        $studentSkill->update($validated);
        $studentSkill->load('skill');
        return response()->json([
            'id' => $studentSkill->id,
            'skill_id' => $studentSkill->skill_id,
            'skill_name' => $studentSkill->skill->name,
            'proficiency_level' => $studentSkill->proficiency_level,
            'months_experience' => $studentSkill->months_experience,
            'source' => $studentSkill->source
        ]);
    }

    public function destroy(Request $request, $id) {
        $student = $request->user()->studentProfile;
        $student->skills()->findOrFail($id)->delete();
        return response()->noContent();
    }
}
""")
