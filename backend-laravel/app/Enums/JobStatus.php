<?php

namespace App\Enums;

enum JobStatus: string
{
    case DRAFT = 'DRAFT';
    case PUBLISHED = 'PUBLISHED';
    case CLOSED = 'CLOSED';
    case CANCELLED = 'CANCELLED';
}
