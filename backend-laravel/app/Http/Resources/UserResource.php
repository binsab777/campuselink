<?php
namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource {
    public function toArray($request) {
        return [
            'id' => $this->id,
            'email' => $this->email,
            'role' => $this->role,
            'is_active' => $this->is_active,
        ];
    }
}
