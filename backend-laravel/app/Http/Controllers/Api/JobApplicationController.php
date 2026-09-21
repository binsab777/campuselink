<?php
namespace App\Http\Controllers\Api;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\Job;
use App\Models\Application;

class JobApplicationController extends Controller {
    public function apply(Request $request, $job_id) {
        $user = $request->user();
        if ($user->role !== 'STUDENT' || !$user->studentProfile) {
            return response()->json(['detail' => 'Only students can apply to jobs'], 403);
        }
        
        $job = Job::where('id', $job_id)->where('status', 'PUBLISHED')->first();
        if (!$job) {
            return response()->json(['detail' => 'Job opening not found or not published'], 404);
        }
        
        $existing = Application::where('job_id', $job_id)->where('student_id', $user->studentProfile->id)->first();
        if ($existing) {
            return response()->json([
                'message' => 'Already applied to this job',
                'application_id' => $existing->id,
                'status' => $existing->status
            ], 200);
        }
        
        $app = Application::create([
            'student_id' => $user->studentProfile->id,
            'job_id' => $job_id,
            'status' => 'APPLIED'
        ]);
        
        return response()->json([
            'message' => 'Application submitted successfully',
            'application_id' => $app->id,
            'status' => $app->status
        ], 201);
    }
}
