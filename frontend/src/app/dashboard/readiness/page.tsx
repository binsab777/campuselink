"use client";

import React, { useEffect, useState, useCallback } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { LoadingState } from "@/components/feedback/LoadingState";
import { ErrorState } from "@/components/feedback/ErrorState";
import { Toast } from "@/components/feedback/Toast";

import { ReadinessScoreCard } from "@/features/readiness/ReadinessScoreCard";
import { DimensionsBreakdownCard } from "@/features/readiness/DimensionsBreakdownCard";
import { StrengthsWeaknessesCard } from "@/features/readiness/StrengthsWeaknessesCard";
import { SkillGapTable } from "@/features/readiness/SkillGapTable";

import { ReadinessData, SkillGapAnalysis } from "@/features/readiness/types";
import { readinessApi } from "@/services/readinessApi";
import { parseApiError } from "@/services/apiClient";

export default function ReadinessPage() {
  const [readiness, setReadiness] = useState<ReadinessData | null>(null);
  const [loading, setLoading] = useState(true);
  const [recalculating, setRecalculating] = useState(false);
  const [error, setError] = useState("");
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  // Skill gap state
  const [jobs, setJobs] = useState<any[]>([]);
  const [selectedJobId, setSelectedJobId] = useState<number | null>(null);
  const [skillGap, setSkillGap] = useState<SkillGapAnalysis | null>(null);
  const [loadingGap, setLoadingGap] = useState(false);

  const fetchReadiness = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const data = await readinessApi.getReadinessMe();
      setReadiness(data);
    } catch (err: any) {
      const parsed = parseApiError(err);
      setError(parsed.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchJobs = useCallback(async () => {
    try {
      const data = await readinessApi.getAvailableJobs();
      setJobs(data);
      if (data && data.length > 0 && !selectedJobId) {
        setSelectedJobId(data[0].id);
      }
    } catch {
      // Jobs might be empty or restricted
    }
  }, [selectedJobId]);

  useEffect(() => {
    fetchReadiness();
    fetchJobs();
  }, [fetchReadiness, fetchJobs]);

  const handleRecalculate = async () => {
    setRecalculating(true);
    try {
      const updated = await readinessApi.recalculateReadiness();
      setReadiness(updated);
      setToastMessage("Readiness score recalculated successfully.");
      if (selectedJobId) {
        handleSelectJob(selectedJobId);
      }
    } catch (err: any) {
      setToastMessage(parseApiError(err).message);
    } finally {
      setRecalculating(false);
    }
  };

  const handleSelectJob = async (jobId: number) => {
    setSelectedJobId(jobId);
    setLoadingGap(true);
    try {
      const gapData = await readinessApi.getSkillGap(jobId);
      setSkillGap(gapData);
    } catch (err: any) {
      setToastMessage(parseApiError(err).message);
    } finally {
      setLoadingGap(false);
    }
  };

  // Automatically trigger skill-gap fetch when selectedJobId changes
  useEffect(() => {
    if (selectedJobId) {
      handleSelectJob(selectedJobId);
    }
  }, [selectedJobId]);

  return (
    <AppLayout allowedRoles={["STUDENT", "SUPER_ADMIN", "PLACEMENT_OFFICER"]}>
      <PageHeader
        title="Placement Readiness & Skill-Gap Analysis"
        subtitle="Transparent evaluation of student profile readiness across 7 core pillars with target job gap detection."
        backHref="/dashboard"
        backLabel="Back to Dashboard"
      />

      <Toast message={toastMessage} onDismiss={() => setToastMessage(null)} />

      {loading ? (
        <LoadingState message="Evaluating student placement readiness dimensions..." />
      ) : error ? (
        <ErrorState message={error} onRetry={fetchReadiness} />
      ) : readiness ? (
        <div className="space-y-8">
          {/* 1. Overall Score & Model Version */}
          <ReadinessScoreCard
            readiness={readiness}
            onRecalculate={handleRecalculate}
            recalculating={recalculating}
          />

          {/* 2. 7-Dimension Breakdown */}
          <DimensionsBreakdownCard readiness={readiness} />

          {/* 3. Strengths & Weaknesses */}
          <StrengthsWeaknessesCard readiness={readiness} />

          {/* 4. Target Job Skill Gap Analysis */}
          <SkillGapTable
            jobs={jobs}
            selectedJobId={selectedJobId}
            onSelectJob={handleSelectJob}
            skillGap={skillGap}
            loading={loadingGap}
          />
        </div>
      ) : null}
    </AppLayout>
  );
}
