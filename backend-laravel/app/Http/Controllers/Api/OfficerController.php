<?php
namespace App\Http\Controllers\Api;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\Student;
use App\Models\Company;

class OfficerController extends Controller {
    public function students(Request $request) {
        $query = Student::query();
        if ($request->has('branch')) $query->where('branch', $request->branch);
        if ($request->has('graduation_year')) $query->where('graduation_year', $request->graduation_year);
        
        $total = $query->count();
        $limit = $request->input('limit', 50);
        $offset = $request->input('offset', 0);
        
        $students = $query->offset($offset)->limit($limit)->get();
        return response()->json(['total' => $total, 'students' => $students]);
    }
    
    public function student($id) {
        return Student::findOrFail($id);
    }
    
    public function companies(Request $request) {
        $query = Company::query();
        if ($request->has('industry')) $query->where('industry', $request->industry);
        
        $total = $query->count();
        $limit = $request->input('limit', 50);
        $offset = $request->input('offset', 0);
        
        $companies = $query->offset($offset)->limit($limit)->get();
        return response()->json(['total' => $total, 'companies' => $companies]);
    }
    
    public function storeCompany(Request $request) {
        $validated = $request->validate(['name' => 'required|string', 'industry' => 'nullable|string', 'description' => 'nullable|string']);
        $company = Company::create($validated);
        return response()->json($company, 201);
    }
}
