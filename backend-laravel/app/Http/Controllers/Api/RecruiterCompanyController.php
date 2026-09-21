<?php
namespace App\Http\Controllers\Api;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class RecruiterCompanyController extends Controller {
    public function show(Request $request) {
        return $request->user()->recruiterProfile->company;
    }
    public function update(Request $request) {
        $company = $request->user()->recruiterProfile->company;
        $validated = $request->validate(['name' => 'sometimes|string', 'description' => 'sometimes|string', 'website' => 'nullable|url', 'industry' => 'nullable|string']);
        $company->update($validated);
        return response()->json($company);
    }
}