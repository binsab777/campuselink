"use client";

import React from "react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { ReadinessData } from "./types";

export interface ReadinessScoreCardProps {
  readiness: ReadinessData | null;
  onRecalculate: () => void;
  recalculating: boolean;
}

export const ReadinessScoreCard: React.FC<ReadinessScoreCardProps> = ({
  readiness,
  onRecalculate,
  recalculating,
}) => {
  if (!readiness) return null;

  const score = Math.round(readiness.overall_score || 0);

  const getScoreColor = (sc: number) => {
    if (sc >= 75) return "text-emerald-600";
    if (sc >= 50) return "text-amber-600";
    return "text-rose-600";
  };

  return (
    <Card
      title="Overall Placement Readiness Score"
      subtitle="Transparent, explainable 7-dimension employability rating calculated by the deterministic readiness engine."
      action={
        <Button
          size="sm"
          onClick={onRecalculate}
          loading={recalculating}
          className="bg-emerald-600 hover:bg-emerald-700 focus:ring-emerald-500"
        >
          Recalculate Score
        </Button>
      }
      className="border-emerald-100 bg-gradient-to-br from-white to-emerald-50/20"
    >
      <div className="flex flex-col sm:flex-row items-center justify-between gap-6">
        <div className="flex items-center gap-6">
          {/* Circular Score Badge */}
          <div className="relative flex items-center justify-center w-28 h-28 rounded-full border-4 border-emerald-500 bg-emerald-50/40 shadow-inner">
            <span className={`text-4xl font-extrabold ${getScoreColor(score)}`}>
              {score}
            </span>
            <span className="absolute bottom-3 text-2xs font-semibold uppercase tracking-wider text-gray-500">
              / 100
            </span>
          </div>

          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-semibold text-gray-600">Readiness Tier:</span>
              <StatusBadge status={readiness.readiness_level} size="md" />
            </div>
            <p className="text-xs text-gray-500">
              Model: <span className="font-mono text-gray-700">{readiness.model_version}</span>
            </p>
            <p className="text-xs text-gray-500 mt-0.5">
              Last Evaluated: {new Date(readiness.calculated_at).toLocaleString()}
            </p>
          </div>
        </div>

        {/* Data Quality Indicator */}
        <div className="w-full sm:w-auto p-4 bg-white border border-gray-200 rounded-xl text-xs space-y-1">
          <span className="font-bold text-gray-800 block">Data Completeness & Reliability</span>
          <p className="text-gray-600">
            Available Dimensions: <span className="font-semibold text-gray-900">{readiness.data_quality?.available_dimensions?.length || 0} / 7</span>
          </p>
          <p className="text-gray-600">
            Weights Redistributed: <span className="font-semibold text-gray-900">{readiness.data_quality?.weights_redistributed ? "Yes (Fair scoring)" : "No (All active)"}</span>
          </p>
        </div>
      </div>
    </Card>
  );
};
