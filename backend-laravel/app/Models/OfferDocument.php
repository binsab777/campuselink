<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class OfferDocument extends Model {
    use HasFactory;
    protected $guarded = ['id'];
    protected $casts = [
        'verified_at' => 'datetime',
    ];

    public function offer() { return $this->belongsTo(Offer::class); }
}