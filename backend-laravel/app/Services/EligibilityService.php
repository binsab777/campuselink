<?php
namespace App\Services;

use App\Models\Student;
use App\Models\Job;

class EligibilityService
{
    public function checkHardEligibility(Student $student, Job $job)
    {
        $eligible = true;
        $reasons = [];
        $strengths = [];

        $config = $job->eligibility_config ?? [];
        
        if (isset($config['min_cgpa']) && $student->cgpa !== null) {
            if ($student->cgpa < $config['min_cgpa']) {
                $eligible = false;
                $reasons[] = "CGPA ({$student->cgpa}) is below required {$config['min_cgpa']}";
            } else {
                $strengths[] = "Meets CGPA requirements.";
            }
        }

        if (isset($config['max_active_backlogs'])) {
            $active = $student->backlogs_current ?? 0;
            if ($active > $config['max_active_backlogs']) {
                $eligible = false;
                $reasons[] = "Active backlogs ({$active}) exceed allowed {$config['max_active_backlogs']}";
            }
        }

        if (isset($config['allowed_branches']) && !empty($config['allowed_branches'])) {
            if (!in_array($student->branch, $config['allowed_branches'])) {
                $eligible = false;
                $reasons[] = "Branch ({$student->branch}) is not eligible.";
            }
        }

        return [
            'is_eligible' => $eligible,
            'passed_criteria' => $strengths,
            'failed_criteria' => $reasons
        ];
    }
}
