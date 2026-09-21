import os

http_components = {
    # Resources (Response models)
    "app/Http/Resources/StudentResource.php": """<?php
namespace App\\Http\\Resources;
use Illuminate\\Http\\Resources\\Json\\JsonResource;

class StudentResource extends JsonResource {
    public function toArray($request) {
        return [
            'id' => $this->id,
            'user_id' => $this->user_id,
            'student_identifier' => $this->student_identifier,
            'first_name' => $this->first_name,
            'last_name' => $this->last_name,
            'branch' => $this->branch,
            'graduation_year' => $this->graduation_year,
            'cgpa' => $this->cgpa ? (float) $this->cgpa : null,
            'backlogs_current' => $this->backlogs_current,
            'backlogs_history' => $this->backlogs_history,
            'phone' => $this->phone,
            'dob' => $this->dob ? $this->dob->format('Y-m-d\\TH:i:s') : null,
            'gender' => $this->gender,
            'profile_picture_url' => $this->profile_picture_url,
            'resume_url' => $this->resume_url,
            'profile_metadata' => $this->profile_metadata,
        ];
    }
}
""",
    
    "app/Http/Resources/FullStudentProfileResource.php": """<?php
namespace App\\Http\\Resources;
use Illuminate\\Http\\Resources\\Json\\JsonResource;

class FullStudentProfileResource extends JsonResource {
    public function toArray($request) {
        return [
            'basic_info' => new StudentResource($this),
            'academic_history' => AcademicHistoryResource::collection($this->whenLoaded('academicHistory')),
            'skills' => StudentSkillResource::collection($this->whenLoaded('skills')),
            'projects' => StudentProjectResource::collection($this->whenLoaded('projects')),
            'certifications' => StudentCertificationResource::collection($this->whenLoaded('certifications')),
            'assessments' => StudentAssessmentResource::collection($this->whenLoaded('assessments')),
        ];
    }
}
""",
    "app/Http/Resources/AcademicHistoryResource.php": """<?php
namespace App\\Http\\Resources;
use Illuminate\\Http\\Resources\\Json\\JsonResource;

class AcademicHistoryResource extends JsonResource {
    public function toArray($request) {
        return parent::toArray($request);
    }
}
""",
    "app/Http/Resources/StudentSkillResource.php": """<?php
namespace App\\Http\\Resources;
use Illuminate\\Http\\Resources\\Json\\JsonResource;

class StudentSkillResource extends JsonResource {
    public function toArray($request) {
        $arr = parent::toArray($request);
        $arr['skill_name'] = $this->whenLoaded('skill', fn() => $this->skill->name);
        return $arr;
    }
}
""",
    "app/Http/Resources/StudentProjectResource.php": """<?php
namespace App\\Http\\Resources;
use Illuminate\\Http\\Resources\\Json\\JsonResource;
class StudentProjectResource extends JsonResource {
    public function toArray($request) { return parent::toArray($request); }
}
""",
    "app/Http/Resources/StudentCertificationResource.php": """<?php
namespace App\\Http\\Resources;
use Illuminate\\Http\\Resources\\Json\\JsonResource;
class StudentCertificationResource extends JsonResource {
    public function toArray($request) { return parent::toArray($request); }
}
""",
    "app/Http/Resources/StudentAssessmentResource.php": """<?php
namespace App\\Http\\Resources;
use Illuminate\\Http\\Resources\\Json\\JsonResource;
class StudentAssessmentResource extends JsonResource {
    public function toArray($request) { return parent::toArray($request); }
}
""",

    # Form Requests (Validators)
    "app/Http/Requests/Student/UpdateBasicInfoRequest.php": """<?php
namespace App\\Http\\Requests\\Student;
use Illuminate\\Foundation\\Http\\FormRequest;
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
""",
}

for path, content in http_components.items():
    os.makedirs(os.path.dirname(f"app/{path}".replace("app/app", "app")), exist_ok=True)
    with open(f"app/{path}".replace("app/app", "app"), 'w') as f:
        f.write(content)

print("HTTP layer generated.")
