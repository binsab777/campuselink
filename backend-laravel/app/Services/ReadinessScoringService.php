<?php
namespace App\Services;

use App\Models\Student;
use App\Models\StudentScore;
use App\Enums\ReadinessLevel;

class ReadinessScoringService
{
    private const WEIGHTS = [
        'academic' => 0.20,
        'technical' => 0.30,
        'projects' => 0.15,
        'certifications' => 0.10,
        'assessments' => 0.10,
        'communication' => 0.10,
        'interview' => 0.05
    ];

    private const PROFICIENCY_SCORES = [
        'BEGINNER' => 25.0,
        'INTERMEDIATE' => 50.0,
        'ADVANCED' => 75.0,
        'EXPERT' => 100.0,
    ];

    public function calculateReadiness(Student $student)
    {
        $student->loadMissing(['skills.skill', 'projects', 'certifications', 'assessments']);
        
        $academic = $this->normalizeAcademic($student);
        $technical = $this->normalizeTechnicalSkills($student);
        $projects = $this->normalizeProjects($student);
        $certs = $this->normalizeCertifications($student);
        $assessments = $this->normalizeAssessments($student);
        
        // Use defaults for missing optional metrics to maintain denominator, or re-weight.
        // The python implementation handles missing ones by falling back to averages or 0 depending.
        // Assuming simple sum for parity, treating missing communication/interview as 0 or skipped.
        $comm = $this->normalizeCommunication($student);
        $interview = $this->normalizeInterview($student);

        $totalScore = 0.0;
        $activeWeights = 0.0;

        $metrics = [
            'academic' => $academic,
            'technical' => $technical,
            'projects' => $projects,
            'certifications' => $certs,
            'assessments' => $assessments,
            'communication' => $comm,
            'interview' => $interview
        ];

        foreach ($metrics as $key => $result) {
            if ($result['score'] !== null) {
                $totalScore += $result['score'] * self::WEIGHTS[$key];
                $activeWeights += self::WEIGHTS[$key];
            }
        }

        $finalScore = $activeWeights > 0 ? ($totalScore / $activeWeights) : 0.0;
        $level = $this->determineLevel($finalScore);

        $explanation = [
            'version' => 'v1.0',
            'overall_score' => round($finalScore, 2),
            'readiness_level' => $level->value,
            'dimensions' => [],
            'strengths' => [],
            'weaknesses' => [],
            'data_quality' => [
                'available_dimensions' => [],
                'weights_redistributed' => false
            ]
        ];

        foreach ($metrics as $key => $result) {
            if ($result['score'] !== null) {
                $explanation['dimensions'][$key] = round($result['score'], 2);
                $explanation['strengths'] = array_merge($explanation['strengths'], $result['strengths']);
                $explanation['weaknesses'] = array_merge($explanation['weaknesses'], $result['weaknesses']);
                $explanation['data_quality']['available_dimensions'][] = $key;
            }
        }
        
        $explanation['data_quality']['weights_redistributed'] = count($explanation['data_quality']['available_dimensions']) < 7;

        StudentScore::updateOrCreate(
            ['student_id' => $student->id, 'score_type' => 'READINESS_V1'],
            [
                'score_value' => $finalScore,
                'model_version' => 'v1.0',
                'explanation_data' => $explanation
            ]
        );

        return $explanation;
    }

    private function determineLevel(float $score): ReadinessLevel
    {
        if ($score >= 80.0) return ReadinessLevel::HIGHLY_EMPLOYABLE;
        if ($score >= 60.0) return ReadinessLevel::READY;
        if ($score >= 40.0) return ReadinessLevel::DEVELOPING;
        return ReadinessLevel::NOT_READY;
    }

    private function normalizeAcademic(Student $student): array
    {
        $strengths = []; $weaknesses = [];
        if ($student->cgpa === null) {
            $weaknesses[] = "Academic CGPA record is missing.";
            return ['score' => 0.0, 'strengths' => $strengths, 'weaknesses' => $weaknesses];
        }

        $base = min(100.0, max(0.0, ($student->cgpa / 10.0) * 100.0));
        
        $active_backlogs = $student->backlogs_current ?? 0;
        $hist_backlogs = $student->backlogs_history ?? 0;
        
        $metadata = $student->profile_metadata ?? [];
        $active_backlogs = $metadata['active_backlogs'] ?? $active_backlogs;
        $hist_backlogs = $metadata['backlogs_history'] ?? $hist_backlogs;

        $penalty = ($active_backlogs * 15.0) + ($hist_backlogs * 5.0);
        $final = max(0.0, min(100.0, $base - $penalty));

        if ($student->cgpa >= 8.5 && $active_backlogs == 0) {
            $strengths[] = sprintf("Outstanding academic record (CGPA %.2f) with zero backlogs.", $student->cgpa);
        } elseif ($student->cgpa >= 7.5 && $active_backlogs == 0) {
            $strengths[] = sprintf("Consistent academic performance (CGPA %.2f) with clear record.", $student->cgpa);
        }

        if ($active_backlogs > 0) {
            $weaknesses[] = "{$active_backlogs} active backlog(s) negatively impact placement eligibility.";
        }
        if ($student->cgpa < 6.5) {
            $weaknesses[] = sprintf("CGPA %.2f is below standard competitive placement thresholds.", $student->cgpa);
        }

        return ['score' => $final, 'strengths' => $strengths, 'weaknesses' => $weaknesses];
    }

    private function normalizeTechnicalSkills(Student $student): array
    {
        $strengths = []; $weaknesses = [];
        $techSkills = $student->skills->filter(function($s) {
            return !$s->skill || $s->skill->category !== 'Soft Skill';
        });

        if ($techSkills->isEmpty()) {
            $weaknesses[] = "No technical skills registered on profile.";
            return ['score' => 0.0, 'strengths' => $strengths, 'weaknesses' => $weaknesses];
        }

        $scores = [];
        foreach ($techSkills as $ss) {
            $score = self::PROFICIENCY_SCORES[$ss->proficiency_level->value] ?? 25.0;
            if ($ss->source && in_array($ss->source->value, ['ASSESSMENT', 'CERTIFICATION', 'VERIFIED'])) {
                $score = min(100.0, $score + 10.0);
            }
            $scores[] = $score;
        }

        $avg = array_sum($scores) / count($scores);
        $breadth = min(1.0, 0.45 + (0.15 * count($techSkills)));
        $final = max(0.0, min(100.0, $avg * $breadth));

        if (count($techSkills) >= 4) {
            $strengths[] = "Strong breadth of technical skills.";
        }
        if ($final > 75.0) {
            $strengths[] = "High technical proficiency levels demonstrated.";
        }

        return ['score' => $final, 'strengths' => $strengths, 'weaknesses' => $weaknesses];
    }

    private function normalizeProjects(Student $student): array
    {
        $strengths = []; $weaknesses = [];
        $count = $student->projects->count();
        
        if ($count === 0) {
            $weaknesses[] = "No applied projects registered.";
            return ['score' => 0.0, 'strengths' => $strengths, 'weaknesses' => $weaknesses];
        }

        $base = min(100.0, 40.0 + ($count * 20.0));
        
        if ($count >= 3) {
            $strengths[] = "Excellent portfolio with multiple applied projects.";
        } else {
            $weaknesses[] = "Limited project portfolio. Adding more projects increases readiness.";
        }

        return ['score' => $base, 'strengths' => $strengths, 'weaknesses' => $weaknesses];
    }

    private function normalizeCertifications(Student $student): array
    {
        $strengths = []; $weaknesses = [];
        $count = $student->certifications->count();
        
        if ($count === 0) {
            $weaknesses[] = "No industry certifications.";
            return ['score' => 0.0, 'strengths' => $strengths, 'weaknesses' => $weaknesses];
        }

        $base = min(100.0, 50.0 + ($count * 25.0));
        $strengths[] = "Verified industry certifications enhance employability.";
        
        return ['score' => $base, 'strengths' => $strengths, 'weaknesses' => $weaknesses];
    }

    private function normalizeAssessments(Student $student): array
    {
        $strengths = []; $weaknesses = [];
        
        if ($student->assessments->isEmpty()) {
            return ['score' => null, 'strengths' => $strengths, 'weaknesses' => $weaknesses];
        }

        $scores = [];
        foreach ($student->assessments as $a) {
            if ($a->max_score > 0) {
                $scores[] = ($a->score / $a->max_score) * 100.0;
            }
        }

        if (empty($scores)) {
            return ['score' => null, 'strengths' => $strengths, 'weaknesses' => $weaknesses];
        }

        $avg = array_sum($scores) / count($scores);
        if ($avg >= 80.0) {
            $strengths[] = "Strong performance in standardized assessments.";
        } elseif ($avg < 60.0) {
            $weaknesses[] = "Assessment scores suggest areas for improvement.";
        }

        return ['score' => $avg, 'strengths' => $strengths, 'weaknesses' => $weaknesses];
    }

    private function normalizeCommunication(Student $student): array
    {
        $commSkills = $student->skills->filter(function($s) {
            return $s->skill && $s->skill->name === 'Communication';
        });
        
        if ($commSkills->isEmpty()) {
            return ['score' => null, 'strengths' => [], 'weaknesses' => []];
        }
        
        $ss = $commSkills->first();
        $score = self::PROFICIENCY_SCORES[$ss->proficiency_level->value] ?? 50.0;
        return ['score' => $score, 'strengths' => [], 'weaknesses' => []];
    }

    private function normalizeInterview(Student $student): array
    {
        // Placeholder for interview score logic, returning null if empty
        return ['score' => null, 'strengths' => [], 'weaknesses' => []];
    }
}
