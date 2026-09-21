<?php
namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\Student;
use App\Http\Resources\StudentResource;
use App\Http\Resources\FullStudentProfileResource;
use App\Http\Resources\AcademicHistoryResource;
use App\Http\Requests\Student\UpdateBasicInfoRequest;
use App\Services\ReadinessScoringService;
use Illuminate\Support\Facades\Storage;
use App\Enums\UserRole;

class StudentController extends Controller
{
    public function __construct(private ReadinessScoringService $readinessService) {}

    private function getStudent(Request $request): Student
    {
        $student = $request->user()->studentProfile;
        if (!$student) {
            abort(404, 'Student profile not found');
        }
        return $student;
    }

    public function getProfile(Request $request)
    {
        return new StudentResource($this->getStudent($request));
    }

    public function getFullProfile(Request $request)
    {
        $student = $this->getStudent($request);
        \Illuminate\Support\Facades\Log::info("Inside getFullProfile: method_exists: " . (method_exists($student, 'assessments') ? 'YES' : 'NO'));
        \Illuminate\Support\Facades\Log::info("Student class: " . get_class($student));
        $student->load(['academicHistory', 'skills.skill', 'projects', 'certifications', 'assessments']);
        return new FullStudentProfileResource($student);
    }

    public function updateBasicInfo(UpdateBasicInfoRequest $request)
    {
        $student = $this->getStudent($request);
        $student->update($request->validated());
        return new StudentResource($student->fresh());
    }

    public function updateLinks(Request $request)
    {
        $student = $this->getStudent($request);
        $data = $request->validate([
            'profile_metadata' => 'required|array'
        ]);
        
        $currentMeta = $student->profile_metadata ?? [];
        if (is_string($currentMeta)) {
            $currentMeta = json_decode($currentMeta, true) ?? [];
        }
        
        $mergedMeta = array_merge($currentMeta, $data['profile_metadata']);
        $student->update(['profile_metadata' => $mergedMeta]);
        
        return new StudentResource($student->fresh());
    }

    public function getReadiness(Request $request)
    {
        $student = $this->getStudent($request);
        return response()->json($this->readinessService->calculateReadiness($student));
    }

    public function getAcademicHistory(Request $request)
    {
        return AcademicHistoryResource::collection($this->getStudent($request)->academicHistory);
    }

    public function uploadResume(Request $request) {
        $student = $this->getStudent($request);
        $request->validate(['file' => 'required|file|mimes:pdf,doc,docx|max:5120']);
        
        $file = $request->file('file');
        $filename = 'student_' . $student->id . '_resume_' . time() . '.' . $file->getClientOriginalExtension();
        
        // Remove old resume if exists
        if ($student->resume_url) {
            $oldPath = str_replace('/api/v1/students/' . $student->id . '/resume/download', '', $student->resume_url);
            // Wait, we need a better way to store the actual path. 
            // In DB, let's store the route in resume_url, but where is the physical path?
            // We can infer physical path or store it in another column, but we can't change DB schema easily.
            // Let's just use a fixed predictable path in private storage and overwrite it.
        }
        
        $filename = 'student_' . $student->id . '_resume.' . $file->getClientOriginalExtension();
        // Delete all possible extensions for this student to ensure clean replace
        foreach(['pdf', 'doc', 'docx'] as $ext) {
            Storage::disk('local')->delete('resumes/student_' . $student->id . '_resume.' . $ext);
        }

        $path = $file->storeAs('resumes', $filename, 'local');
        
        $student->update(['resume_url' => '/api/v1/students/' . $student->id . '/resume/download']);
        return response()->json(['message' => 'Resume uploaded successfully', 'resume_url' => $student->resume_url]);
    }

    public function deleteResume(Request $request) {
        $student = $this->getStudent($request);
        if (!$student->resume_url) return response()->json(['detail' => 'No resume found to delete'], 400);
        
        foreach(['pdf', 'doc', 'docx'] as $ext) {
            Storage::disk('local')->delete('resumes/student_' . $student->id . '_resume.' . $ext);
        }
        
        $student->update(['resume_url' => null]);
        return response()->json(null, 204);
    }
    
    public function downloadResume(Request $request, $id) {
        $student = Student::findOrFail($id);
        if (!$student->resume_url) return response()->json(['detail' => 'Not found'], 404);
        
        $user = $request->user();
        $authorized = false;
        
        if ($user->role === UserRole::STUDENT->value && $user->studentProfile && $user->studentProfile->id == $id) {
            $authorized = true;
        } elseif (in_array($user->role, [UserRole::SUPER_ADMIN->value, UserRole::PLACEMENT_OFFICER->value])) {
            $authorized = true;
        } elseif ($user->role === UserRole::RECRUITER->value) {
            $recruiter = $user->recruiterProfile;
            // Check if student applied to recruiter's jobs or drives
            $inDrive = \App\Models\DriveCandidate::where('student_id', $id)
                ->whereHas('drive', function($q) use ($recruiter) {
                    $q->where('company_id', $recruiter->company_id);
                })->exists();
            $inJob = \App\Models\Application::where('student_id', $id)
                ->whereHas('job', function($q) use ($recruiter) {
                    $q->where('company_id', $recruiter->company_id);
                })->exists();
            if ($inDrive || $inJob) $authorized = true;
        }
        
        if (!$authorized) return response()->json(['detail' => 'Unauthorized'], 403);
        
        // Find file
        $file = null;
        foreach(['pdf', 'doc', 'docx'] as $ext) {
            if (Storage::disk('local')->exists('resumes/student_' . $id . '_resume.' . $ext)) {
                $file = 'resumes/student_' . $id . '_resume.' . $ext;
                break;
            }
        }
        
        if (!$file) return response()->json(['detail' => 'File missing'], 404);
        
        return Storage::disk('local')->download($file);
    }
    
    public function completeness(Request $request) {
        $student = $this->getStudent($request);
        $student->load(['academicHistory', 'skills', 'projects', 'certifications']);
        
        $completed_sections = [];
        $missing_sections = [];
        
        if ($student->first_name && $student->last_name && $student->dob) {
            $completed_sections[] = 'Basic Info';
        } else {
            $missing_sections[] = 'Basic Info';
        }
        
        if ($student->phone) {
            $completed_sections[] = 'Contact Info';
        } else {
            $missing_sections[] = 'Contact Info';
        }
        
        if ($student->branch && $student->graduation_year) {
            $completed_sections[] = 'Academics';
        } else {
            $missing_sections[] = 'Academics';
        }
        
        if ($student->resume_url) {
            $completed_sections[] = 'Resume';
        } else {
            $missing_sections[] = 'Resume';
        }
        
        if ($student->skills->count() > 0) {
            $completed_sections[] = 'Skills';
        } else {
            $missing_sections[] = 'Skills';
        }
        
        if ($student->projects->count() > 0) {
            $completed_sections[] = 'Projects';
        } else {
            $missing_sections[] = 'Projects';
        }
        
        $meta = is_string($student->profile_metadata) ? json_decode($student->profile_metadata, true) : ($student->profile_metadata ?? []);
        
        if (isset($meta['bio']) && !empty($meta['bio'])) {
            $completed_sections[] = 'Bio';
        } else {
            $missing_sections[] = 'Bio';
        }
        
        if (isset($meta['linkedin_url']) && !empty($meta['linkedin_url'])) {
            $completed_sections[] = 'LinkedIn';
        } else {
            $missing_sections[] = 'LinkedIn';
        }
        
        $total = count($completed_sections) + count($missing_sections);
        $percentage = $total > 0 ? (int) round((count($completed_sections) / $total) * 100) : 0;
        
        return response()->json([
            'percentage' => $percentage,
            'completed_sections' => $completed_sections,
            'missing_sections' => $missing_sections
        ]);
    }

    public function drives(Request $request) {
        $student = $this->getStudent($request);
        $candidates = \App\Models\DriveCandidate::with(['drive.company', 'drive.job'])->where('student_id', $student->id)->get();
        return response()->json($candidates->map(function ($c) {
            return [
                'candidate_id' => $c->id,
                'drive_id' => $c->drive_id,
                'drive_name' => $c->drive->name,
                'company_name' => $c->drive->company->name,
                'job_title' => $c->drive->job ? $c->drive->job->title : null,
                'date' => $c->drive->start_date ? date('Y-m-d', strtotime($c->drive->start_date)) : null,
                'start_time' => $c->drive->start_time,
                'end_time' => $c->drive->end_time,
                'mode' => $c->drive->mode,
                'venue' => $c->drive->venue,
                'drive_status' => $c->drive->status,
                'eligibility_status' => $c->status !== 'WITHDRAWN' ? true : false,
                'registration_status' => $c->status,
                'shortlist_status' => $c->status === 'SHORTLISTED',
                'registration_timestamp' => $c->registered_at ? $c->registered_at->toIso8601String() : null
            ];
        }));
    }
}
