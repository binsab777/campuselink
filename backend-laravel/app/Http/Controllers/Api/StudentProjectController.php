<?php
namespace App\Http\Controllers\Api;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\StudentProject;

class StudentProjectController extends Controller {
    public function index(Request $request) {
        return $request->user()->studentProfile->projects()->get();
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
