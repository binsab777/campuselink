<?php

namespace App\Enums;

enum DriveStatus: string
{
    case DRAFT = 'DRAFT';
    case PUBLISHED = 'PUBLISHED';
    case REGISTRATION_OPEN = 'REGISTRATION_OPEN';
    case REGISTRATION_CLOSED = 'REGISTRATION_CLOSED';
    case IN_PROGRESS = 'IN_PROGRESS';
    case COMPLETED = 'COMPLETED';
    case CANCELLED = 'CANCELLED';
}
