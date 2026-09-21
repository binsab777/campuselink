<?php
namespace App\Services;

use App\Models\Student;
use App\Models\Job;
use App\Models\SkillGap;
use App\Enums\GapSeverity;

class SkillGapService
{
    private const PROFICIENCY_LEVELS = [
        'BEGINNER' => 1,
        'INTERMEDIATE' => 2,
        'ADVANCED' => 3,
        'EXPERT' => 4,
    ];

    public function analyzeSkillGaps(Student $student, Job $job)
    {
        $student->load('skills.skill');
        $job->load('requirements.skill');

        $studentSkills = $student->skills->keyBy('skill_id');
        $gaps = [];

        foreach ($job->requirements as $req) {
            $reqLevel = self::PROFICIENCY_LEVELS[$req->required_proficiency->value];
            $studentSkill = $studentSkills->get($req->skill_id);
            $studentLevel = $studentSkill ? self::PROFICIENCY_LEVELS[$studentSkill->proficiency_level->value] : 0;
            
            $diff = $reqLevel - $studentLevel;
            $severity = GapSeverity::NONE;

            if ($diff > 0) {
                if ($studentLevel === 0) {
                    $severity = $req->is_mandatory ? GapSeverity::CRITICAL : GapSeverity::HIGH;
                } else {
                    $severity = $diff >= 2 ? GapSeverity::HIGH : GapSeverity::MEDIUM;
                }
            }

            if ($severity !== GapSeverity::NONE) {
                $gaps[] = [
                    'skill_id' => $req->skill_id,
                    'severity' => $severity,
                    'current' => $studentLevel,
                    'required' => $reqLevel,
                    'is_mandatory' => $req->is_mandatory,
                    'recommendation' => $this->generateRecommendation($req->skill->name, $req->required_proficiency->value, $severity)
                ];
            }
        }

        // Persist gaps
        SkillGap::where('student_id', $student->id)->where('job_id', $job->id)->delete();
        $savedGaps = [];

        foreach ($gaps as $gap) {
            $savedGaps[] = SkillGap::create([
                'student_id' => $student->id,
                'job_id' => $job->id,
                'skill_id' => $gap['skill_id'],
                'gap_severity' => $gap['severity']->value,
                'current_level' => $gap['current'],
                'required_level' => $gap['required'],
                'is_mandatory' => $gap['is_mandatory'],
                'recommendation' => $gap['recommendation'],
            ]);
        }

        return $savedGaps;
    }

    private function generateRecommendation($skillName, $reqProf, $severity)
    {
        if ($severity === GapSeverity::CRITICAL) {
            return "Critical missing skill: \{$skillName\}. Requires immediate foundational learning.";
        } elseif ($severity === GapSeverity::HIGH) {
            return "High gap in \{$skillName\}. Significant upskilling required to reach \{$reqProf\}.";
        }
        return "Moderate gap in \{$skillName\}. Needs practical experience to improve proficiency.";
    }
}
