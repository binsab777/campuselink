export interface CompanyData {
  id: number;
  name: string;
  industry?: string | null;
  size?: string | null;
  website?: string | null;
  headquarters?: string | null;
  description?: string | null;
}

export interface JobRequirementItem {
  id: number;
  job_id: number;
  skill_id: number;
  skill_name?: string;
  required_proficiency: "BEGINNER" | "INTERMEDIATE" | "ADVANCED" | "EXPERT";
  weight: number;
  is_mandatory: boolean;
  minimum_experience: number;
  notes?: string | null;
}

export interface SkillItem {
  id: number;
  name: string;
  category?: string | null;
}

export interface EligibilityConfig {
  min_cgpa?: number;
  max_backlogs?: number;
  graduation_year?: number;
  allowed_branches?: string[];
}

export interface JobData {
  id: number;
  company_id: number;
  title: string;
  description: string;
  employment_type: string;
  location?: string | null;
  remote_type?: string | null;
  salary_range?: string | null;
  openings?: number | null;
  application_deadline?: string | null;
  eligibility_config?: EligibilityConfig | null;
  status: "DRAFT" | "PUBLISHED" | "CLOSED" | "CANCELLED";
  requirements?: JobRequirementItem[];
}

export interface DriveData {
  id: number;
  company_id: number;
  job_id: number;
  name: string;
  description?: string | null;
  date: string;
  start_time: string;
  end_time: string;
  registration_start?: string | null;
  registration_deadline?: string | null;
  mode?: string | null;
  venue?: string | null;
  capacity?: number | null;
  coordinator_info?: string | null;
  notes?: string | null;
  status: "DRAFT" | "PUBLISHED" | "REGISTRATION_OPEN" | "IN_PROGRESS" | "COMPLETED" | "CANCELLED";
}

export interface RecruiterProfile {
  id: number;
  user_id: number;
  company_id: number;
  designation?: string | null;
  phone?: string | null;
  company?: CompanyData | null;
}
