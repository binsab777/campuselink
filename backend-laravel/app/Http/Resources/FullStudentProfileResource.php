<?php
namespace App\Http\Resources;
use Illuminate\Http\Resources\Json\JsonResource;

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
