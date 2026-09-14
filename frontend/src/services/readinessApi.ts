import { apiClient } from "./apiClient";
import { ReadinessData, SkillGapAnalysis } from "@/features/readiness/types";

export const readinessApi = {
  getReadinessMe: () => apiClient.get<ReadinessData>("/api/v1/readiness/me"),

  recalculateReadiness: () =>
    apiClient.post<ReadinessData>("/api/v1/readiness/me/recalculate"),

  getSkillGap: (jobId: number) =>
    apiClient.get<SkillGapAnalysis>(`/api/v1/readiness/me/jobs/${jobId}/skill-gaps`),

  getAvailableJobs: () =>
    apiClient.get<any[]>("/api/v1/jobs/available"),
};
