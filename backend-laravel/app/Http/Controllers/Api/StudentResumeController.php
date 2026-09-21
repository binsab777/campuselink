<?php
namespace App\Http\Controllers\Api;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Services\FileStorageService;
class StudentResumeController extends Controller {
    public function upload(Request $request, FileStorageService $storage) {
        $request->validate(['resume' => 'required|file|mimes:pdf,doc,docx|max:5120']);
        $student = $request->user()->studentProfile;
        if ($student->resume_url) $storage->delete($student->resume_url);
        $url = $storage->upload($request->file('resume'), 'resumes', 'resume_' . $student->id . '.' . $request->file('resume')->extension());
        $student->update(['resume_url' => $url]);
        return response()->json(['resume_url' => $url]);
    }
}
