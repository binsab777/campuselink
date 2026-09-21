<?php
namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use App\Models\Student;
use App\Enums\UserRole;

class FileController extends Controller {
    public function download(Request $request, $directory, $filename) {
        $path = $directory . '/' . $filename;
        if (!Storage::disk('local')->exists($path)) {
            abort(404);
        }

        $user = $request->user();

        // Check authorization based on directory
        if ($directory === 'resumes') {
            // Find student by looking at the filename (e.g. resume_1.pdf)
            // Or just check if the user is a recruiter, PO, admin, or the owner.
            if ($user->role === UserRole::STUDENT->value) {
                $student = $user->studentProfile;
                // Basic check: is this their resume?
                // The URL is like /api/v1/files/resumes/resume_1.pdf
                // We stored it as resume_ID.extension. So check if it matches the student ID.
                if (strpos($filename, 'resume_' . $student->id . '.') !== 0) {
                    abort(403, "Unauthorized access to this resume");
                }
            }
        }

        return Storage::disk('local')->download($path);
    }
}
