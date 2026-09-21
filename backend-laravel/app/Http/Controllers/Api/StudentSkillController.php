<?php
namespace App\Http\Controllers\Api;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\Skill;
use App\Enums\ProficiencyLevel;
use Illuminate\Validation\Rule;

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
            'source' => 'STUDENT'
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
