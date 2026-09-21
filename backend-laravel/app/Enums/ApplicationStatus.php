<?php

namespace App\Enums;

enum ApplicationStatus: string
{
    case APPLIED = 'APPLIED';
    case ELIGIBLE = 'ELIGIBLE';
    case SHORTLISTED = 'SHORTLISTED';
    case INTERVIEW = 'INTERVIEW';
    case SELECTED = 'SELECTED';
    case REJECTED = 'REJECTED';
    case WITHDRAWN = 'WITHDRAWN';
}
