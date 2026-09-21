<?php

namespace App\Enums;

enum SkillSource: string
{
    case STUDENT = 'STUDENT';
    case RESUME = 'RESUME';
    case ASSESSMENT = 'ASSESSMENT';
    case CERTIFICATION = 'CERTIFICATION';
    case VERIFIED = 'VERIFIED';
    case AI_EXTRACTED = 'AI_EXTRACTED';
}
