<?php
namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\Student;
use App\Models\Job;
use App\Services\ReadinessScoringService;
use App\Services\SkillGapService;

class ReadinessController extends Controller
{
    public function __construct(
        private ReadinessScoringService $readinessService,
        private SkillGapService $skillGapService
    ) {}

    public function me(Request $request)
    {
        $student = $request->user()->studentProfile;
        if (!$student) abort(404, 'Student profile not found');
        return response()->json($this->readinessService->calculateReadiness($student));
    }

    public function recalculate(Request $request)
    {
        // For now, recalculate just delegates to calculateReadiness
        return $this->me($request);
    }

    public function gaps(Request $request, $jobId)
    {
        $student = $request->user()->studentProfile;
        $job = Job::findOrFail($jobId);
        return response()->json($this->skillGapService->analyzeSkillGaps($student, $job));
    }

    public function analyze(Request $request, $jobId)
    {
        return $this->gaps($request, $jobId); // delegates for now
    }

    public function studentReadiness($id)
    {
        $student = Student::findOrFail($id);
        return response()->json($this->readinessService->calculateReadiness($student));
    }

    public function studentGaps($s_id, $j_id)
    {
        $student = Student::findOrFail($s_id);
        $job = Job::findOrFail($j_id);
        return response()->json($this->skillGapService->analyzeSkillGaps($student, $job));
    }
}
