<?php
namespace App\Http\Resources;
use Illuminate\Http\Resources\Json\JsonResource;

class StudentSkillResource extends JsonResource {
    public function toArray($request) {
        $arr = parent::toArray($request);
        $arr['skill_name'] = $this->whenLoaded('skill', fn() => $this->skill->name);
        return $arr;
    }
}
