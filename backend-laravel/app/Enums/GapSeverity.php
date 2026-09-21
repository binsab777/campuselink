<?php

namespace App\Enums;

enum GapSeverity: string
{
    case NONE = 'NONE';
    case LOW = 'LOW';
    case MEDIUM = 'MEDIUM';
    case HIGH = 'HIGH';
    case CRITICAL = 'CRITICAL';
}
