<?php

namespace App\Enums;

enum UserRole: string
{
    case SUPER_ADMIN = 'SUPER_ADMIN';
    case PLACEMENT_OFFICER = 'PLACEMENT_OFFICER';
    case RECRUITER = 'RECRUITER';
    case STUDENT = 'STUDENT';
    case MENTOR = 'MENTOR';
}
