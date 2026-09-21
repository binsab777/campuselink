<?php
namespace App\Http\Resources;
use Illuminate\Http\Resources\Json\JsonResource;

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
            'dob' => $this->dob ? $this->dob->format('Y-m-d\TH:i:s') : null,
            'gender' => $this->gender,
            'profile_picture_url' => $this->profile_picture_url,
            'resume_url' => $this->resume_url,
            'profile_metadata' => $this->profile_metadata,
        ];
    }
}
