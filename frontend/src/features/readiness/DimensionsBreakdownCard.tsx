"use client";

import React from "react";
import { Card } from "@/components/ui/Card";
import { ReadinessData } from "./types";

export interface DimensionsBreakdownCardProps {
  readiness: ReadinessData | null;
}

export const DimensionsBreakdownCard: React.FC<DimensionsBreakdownCardProps> = ({ readiness }) => {
  if (!readiness) return null;

  const comps = readiness.components || {};

  const dimensions = [
    { key: "academic", label: "Academic Foundation", score: comps.academic },
    { key: "technical", label: "Technical Skills Mastery", score: comps.technical },
    { key: "projects", label: "Applied Projects", score: comps.projects },
    { key: "certifications", label: "Industry Certifications", score: comps.certifications },
    { key: "assessments", label: "Standardized Assessments", score: comps.assessments },
    { key: "communication", label: "Communication & Soft Skills", score: comps.communication },
    { key: "interview", label: "Mock Interviews & Aptitude", score: comps.interview },
  ];

  const getBarColor = (score: number) => {
    if (score >= 75) return "bg-emerald-500";
    if (score >= 50) return "bg-blue-500";
    if (score > 0) return "bg-amber-500";
    return "bg-gray-300";
  };

  return (
    <Card
      title="Multidimensional Breakdown (7 Core Dimensions)"
      subtitle="Examine your performance across each evaluated pillar and its dynamically normalized weight."
    >
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {dimensions.map((dim) => {
          const effectiveWeight = Math.round(((readiness.effective_weights || {})[dim.key] || 0) * 100);
          const score = Math.round(dim.score || 0);

          return (
            <div key={dim.key} className="p-4 bg-gray-50 border border-gray-100 rounded-xl space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold text-gray-800">{dim.label}</span>
                <span className="text-sm font-bold text-gray-900">{score} / 100</span>
              </div>

              <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                <div
                  className={`h-2 rounded-full transition-all duration-500 ${getBarColor(score)}`}
                  style={{ width: `${Math.min(100, Math.max(0, score))}%` }}
                />
              </div>

              <div className="flex items-center justify-between text-2xs text-gray-500 pt-0.5">
                <span>Effective Weight: <strong className="text-gray-700">{effectiveWeight}%</strong></span>
                <span>Configured: <strong className="text-gray-700">{Math.round(((readiness.configured_weights || {})[dim.key] || 0) * 100)}%</strong></span>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
};
