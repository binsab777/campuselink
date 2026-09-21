<?php
namespace App\Http\Controllers\Api;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\StudentAcademicHistory;
use Carbon\Carbon;

class StudentAcademicController extends Controller {
    public function index(Request $request) {
        $user = $request->user();
        $records = StudentAcademicHistory::where('student_id', $user->studentProfile->id)->get()->map(function($r) {
            return [
                'id' => $r->id,
                'qualification' => $r->qualification,
                'institution' => $r->institution,
                'specialization' => $r->specialization,
                'start_year' => $r->start_year,
                'end_year' => $r->end_year,
                'score_type' => $r->score_type,
                'score_value' => (float)$r->score_value
            ];
        });
        return response()->json($records);
    }
    
    public function store(Request $request) {
        $validated = $request->validate([
            'qualification' => 'required|string|min:1|max:100',
            'institution' => 'required|string|min:1|max:200',
            'specialization' => 'nullable|string|max:100',
            'start_year' => 'nullable|integer|min:1900|max:2100',
            'end_year' => 'nullable|integer|min:1900|max:2100',
            'score_value' => 'required|numeric|min:0',
            'score_type' => 'required|string|in:CGPA,PERCENTAGE,cgpa,percentage',
        ]);
        
        if (strtoupper($validated['score_type']) === 'CGPA' && $validated['score_value'] > 10.0) {
            return response()->json(['detail' => 'CGPA cannot exceed 10.0'], 400); // Or let validation handle it, FastAPI likely throws 422 if it's in schema, or custom. I will add basic check.
        }
        if (strtoupper($validated['score_type']) === 'PERCENTAGE' && $validated['score_value'] > 100.0) {
            return response()->json(['detail' => 'Percentage cannot exceed 100.0'], 400);
        }
        
        $user = $request->user();
        $record = StudentAcademicHistory::create([
            'student_id' => $user->studentProfile->id,
            'institution' => $validated['institution'],
            'qualification' => $validated['qualification'],
            'specialization' => $validated['specialization'] ?? null,
            'start_year' => $validated['start_year'] ?? null,
            'end_year' => $validated['end_year'] ?? null,
            'score_value' => (float)$validated['score_value'],
            'score_type' => strtoupper($validated['score_type'])
        ]);
        
        return response()->json([
            'id' => $record->id,
            'qualification' => $record->qualification,
            'institution' => $record->institution,
            'specialization' => $record->specialization,
            'start_year' => $record->start_year,
            'end_year' => $record->end_year,
            'score_type' => $record->score_type,
            'score_value' => (float)$record->score_value
        ]);
    }
    
    public function update(Request $request, $id) {
        $record = StudentAcademicHistory::where('id', $id)->where('student_id', $request->user()->studentProfile->id)->first();
        if (!$record) return response()->json(['detail' => 'Academic history not found'], 404);
        
        $validated = $request->validate([
            'qualification' => 'sometimes|string|min:1|max:100',
            'institution' => 'sometimes|string|min:1|max:200',
            'specialization' => 'nullable|string|max:100',
            'start_year' => 'nullable|integer|min:1900|max:2100',
            'end_year' => 'nullable|integer|min:1900|max:2100',
            'score_value' => 'sometimes|numeric|min:0',
            'score_type' => 'sometimes|string|in:CGPA,PERCENTAGE,cgpa,percentage',
        ]);
        
        if (isset($validated['institution'])) $record->institution = $validated['institution'];
        if (isset($validated['qualification'])) $record->qualification = $validated['qualification'];
        if (array_key_exists('specialization', $validated)) $record->specialization = $validated['specialization'];
        if (array_key_exists('start_year', $validated)) $record->start_year = $validated['start_year'];
        if (array_key_exists('end_year', $validated)) $record->end_year = $validated['end_year'];
        if (isset($validated['score_value'])) $record->score_value = (float)$validated['score_value'];
        if (isset($validated['score_type'])) $record->score_type = strtoupper($validated['score_type']);
        
        $record->save();
        return response()->json([
            'id' => $record->id,
            'qualification' => $record->qualification,
            'institution' => $record->institution,
            'specialization' => $record->specialization,
            'start_year' => $record->start_year,
            'end_year' => $record->end_year,
            'score_type' => $record->score_type,
            'score_value' => (float)$record->score_value
        ]);
    }
    
    public function destroy(Request $request, $id) {
        $record = StudentAcademicHistory::where('id', $id)->where('student_id', $request->user()->studentProfile->id)->first();
        if (!$record) return response()->json(['detail' => 'Academic history not found'], 404);
        $record->delete();
        return response()->json(null, 204);
    }
}
