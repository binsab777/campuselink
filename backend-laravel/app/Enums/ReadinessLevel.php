<?php

namespace App\Enums;

enum ReadinessLevel: string
{
    case NOT_READY = 'NOT_READY';
    case DEVELOPING = 'DEVELOPING';
    case READY = 'READY';
    case HIGHLY_EMPLOYABLE = 'HIGHLY_EMPLOYABLE';
}
