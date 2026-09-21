<?php
namespace App\Http\Controllers\Api;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\Skill;
use App\Models\StudentSkill;
use App\Models\JobRequirement;

class SkillController extends Controller {
    public function index(Request $request) {
        $query = Skill::withCount(['studentSkills as student_count', 'jobRequirements as job_count']);
        if ($request->has('category')) $query->where('category', $request->category);
        if ($request->has('query')) {
            $q = strtolower($request->input('query'));
            $query->whereRaw('LOWER(name) like ?', ['%' . $q . '%']);
        }
        $query->orderBy('category', 'asc')->orderBy('name', 'asc');
        return response()->json($query->get());
    }
    
    public function store(Request $request) {
        $validated = $request->validate([
            'name' => 'required|string|unique:skills,name',
            'category' => 'required|string',
            'description' => 'nullable|string'
        ]);
        $skill = Skill::create($validated);
        return response()->json($skill, 201);
    }
    
    public function update(Request $request, $id) {
        $skill = Skill::findOrFail($id);
        $validated = $request->validate([
            'name' => 'sometimes|string|unique:skills,name,'.$id,
            'category' => 'sometimes|string',
            'description' => 'nullable|string'
        ]);
        $skill->update($validated);
        return response()->json($skill);
    }
    
    public function destroy($id) {
        $skill = Skill::findOrFail($id);
        
        $studentUsage = StudentSkill::where('skill_id', $id)->exists();
        $jobUsage = class_exists(JobRequirement::class) ? JobRequirement::where('skill_id', $id)->exists() : false;
        
        if ($studentUsage || $jobUsage) {
            return response()->json(['detail' => 'Cannot delete skill as it is being used by students or job requirements'], 400);
        }
        
        $skill->delete();
        return response()->json(null, 204);
    }
}
