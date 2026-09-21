<?php
namespace App\Http\Controllers\Api;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\User;
use App\Models\Skill;
use App\Models\Student;
use App\Models\Company;
use Illuminate\Support\Facades\DB;

class AdminController extends Controller {
    public function index(Request $request) {
        $query = User::with(['studentProfile', 'recruiterProfile.company']);
        if ($request->has('role')) $query->where('role', $request->role);
        if ($request->has('is_active')) $query->where('is_active', $request->boolean('is_active'));
        if ($request->has('query')) {
            $searchTerm = $request->input('query');
            $operator = DB::connection()->getDriverName() === 'pgsql' ? 'ILIKE' : 'LIKE';
            $query->where('email', $operator, "%{$searchTerm}%");
        }
        
        $total = $query->count();
        $users = $query->offset($request->input('offset', 0))->limit($request->input('limit', 50))->get();
        return response()->json([
            'total' => $total, 
            'users' => $users->map(function ($u) {
                return [
                    'id' => $u->id,
                    'email' => $u->email,
                    'role' => $u->role,
                    'is_active' => $u->is_active,
                    'created_at' => $u->created_at,
                    'student_profile' => $u->studentProfile,
                    'recruiter_profile' => $u->recruiterProfile
                ];
            })
        ]);
    }
    
    public function status(Request $request, $id) {
        $validated = $request->validate(['is_active' => 'required|boolean']);
        $user = User::findOrFail($id);
        if ($user->id === $request->user()->id && !$validated['is_active']) {
            return response()->json(['detail' => 'Cannot deactivate your own account'], 400); // Wait, FastAPI throws 400? Yes!
        }
        $user->is_active = $validated['is_active'];
        $user->save();
        return response()->json(['id' => $user->id, 'email' => $user->email, 'is_active' => $user->is_active]);
    }
    
    public function show(Request $request, $id) {
        $user = User::with([
            'studentProfile.academicHistory',
            'studentProfile.skills.skill',
            'studentProfile.projects',
            'studentProfile.certifications',
            'studentProfile.assessments',
            'studentProfile.applications',
            'studentProfile.scores',
            'studentProfile.offers',
            'recruiterProfile.company',
            'recruiterProfile.jobs.requirements',
            'recruiterProfile.jobs.applications'
        ])->findOrFail($id);

        return response()->json($user);
    }
}
