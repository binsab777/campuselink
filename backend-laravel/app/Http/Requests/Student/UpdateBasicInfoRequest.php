<?php
namespace App\Http\Requests\Student;
use Illuminate\Foundation\Http\FormRequest;
class UpdateBasicInfoRequest extends FormRequest {
    public function authorize() { return true; }
    public function rules() {
        return [
            'first_name' => 'sometimes|string|max:100',
            'last_name' => 'sometimes|string|max:100',
            'phone' => 'sometimes|nullable|string|max:20',
            'dob' => 'sometimes|nullable|date',
            'gender' => 'sometimes|nullable|string',
            'branch' => 'sometimes|string',
            'graduation_year' => 'sometimes|integer',
            'cgpa' => 'sometimes|nullable|numeric|min:0|max:10',
            'backlogs_current' => 'sometimes|integer|min:0',
            'backlogs_history' => 'sometimes|integer|min:0',
        ];
    }
}
