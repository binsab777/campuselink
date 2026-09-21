<?php
namespace App\Http\Controllers\Api;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class RecruiterDriveController extends Controller {
    public function index(Request $request) {
        return $request->user()->recruiterProfile->company->drives;
    }
    public function store(Request $request) {
        $validated = $request->validate([
            'name' => 'required|string|min:3|max:150',
            'description' => 'nullable|string|max:2000',
            'job_id' => 'required|integer|exists:jobs,id',
            'date' => 'required|date',
            'registration_start' => 'nullable|date',
            'registration_deadline' => 'nullable|date',
            'start_time' => 'required|date',
            'end_time' => 'required|date|after:start_time',
            'mode' => 'nullable|string|max:50',
            'venue' => 'nullable|string|max:200',
            'capacity' => 'nullable|integer|min:1',
            'coordinator_info' => 'nullable|string|max:200',
            'notes' => 'nullable|string|max:1000'
        ]);
        
        $job = $request->user()->recruiterProfile->company->jobs()->find($validated['job_id']);
        if (!$job) {
            return response()->json(['detail' => 'Invalid job ID: Job does not exist or does not belong to your company'], 400);
        }

        $validated['status'] = 'DRAFT';
        $drive = $request->user()->recruiterProfile->company->drives()->create($validated);
        return response()->json($drive, 201);
    }
    public function update(Request $request, $id) {
        $drive = $request->user()->recruiterProfile->company->drives()->findOrFail($id);
        $validated = $request->validate([
            'name' => 'sometimes|string|min:3|max:150',
            'description' => 'nullable|string|max:2000',
            'job_id' => 'sometimes|integer|exists:jobs,id',
            'date' => 'sometimes|date',
            'registration_start' => 'nullable|date',
            'registration_deadline' => 'nullable|date',
            'start_time' => 'sometimes|date',
            'end_time' => 'sometimes|date|after:start_time',
            'mode' => 'nullable|string|max:50',
            'venue' => 'nullable|string|max:200',
            'capacity' => 'nullable|integer|min:1',
            'coordinator_info' => 'nullable|string|max:200',
            'notes' => 'nullable|string|max:1000',
            'status' => 'sometimes|string'
        ]);
        
        if (isset($validated['job_id'])) {
            $job = $request->user()->recruiterProfile->company->jobs()->find($validated['job_id']);
            if (!$job) {
                return response()->json(['detail' => 'Invalid job ID: Job does not exist or does not belong to your company'], 400);
            }
        }
        
        if (isset($validated['status']) && $validated['status'] !== $drive->status) {
            if (in_array($drive->status, ['COMPLETED', 'CANCELLED']) && in_array($validated['status'], ['DRAFT', 'PUBLISHED', 'REGISTRATION_OPEN'])) {
                return response()->json(['detail' => 'Cannot reopen a completed or cancelled drive.'], 400);
            }
        }

        $drive->update($validated);
        return response()->json($drive);
    }
    public function destroy(Request $request, $id) {
        $drive = $request->user()->recruiterProfile->company->drives()->findOrFail($id);
        $drive->delete();
        return response()->json(null, 204);
    }
}
