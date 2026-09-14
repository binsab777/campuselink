export interface ComponentBreakdown {
  academic: number;
  technical: number;
  projects: number;
  certifications: number;
  assessments: number;
  communication: number;
  interview: number;
}

export interface ReadinessData {
  overall_score: number;
  readiness_level: string;
  components: ComponentBreakdown;
  configured_weights: Record<string, number>;
  effective_weights: Record<string, number>;
  strengths: string[];
  weaknesses: string[];
  data_quality: {
    completeness_ratio: number;
    available_dimensions: string[];
    missing_dimensions: string[];
    weights_redistributed: boolean;
  };
  model_version: string;
  calculated_at: string;
}

export interface SkillGapItem {
  skill_id: number;
  skill_name: string;
  required_proficiency: string;
  student_proficiency: string | null;
  severity: string;
  is_mandatory: boolean;
  recommendation: string;
}

export interface SkillGapAnalysis {
  job_id: number;
  job_title: string;
  company_name: string | null;
  job_readiness_score: number;
  global_readiness_score: number;
  mandatory_skills_score: number;
  preferred_skills_score: number;
  matched_count: number;
  partial_count: number;
  missing_count: number;
  matched_skills: SkillGapItem[];
  partial_skills: SkillGapItem[];
  missing_skills: SkillGapItem[];
  gaps: any[];
}
