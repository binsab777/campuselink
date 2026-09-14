"use client";

import React, { useEffect, useState, useCallback } from "react";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { LoadingState } from "@/components/feedback/LoadingState";
import { EmptyState } from "@/components/feedback/EmptyState";
import { CandidateProfileModal } from "./CandidateProfileModal";
import { DriveData } from "./types";
import { CandidateItem, recruitersApi } from "@/services/recruitersApi";

export interface CandidateManagementModalProps {
  isOpen: boolean;
  onClose: () => void;
  drive: DriveData | null;
}

export const CandidateManagementModal: React.FC<CandidateManagementModalProps> = ({
  isOpen,
  onClose,
  drive,
}) => {
  const [candidates, setCandidates] = useState<CandidateItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [evaluating, setEvaluating] = useState(false);
  const [evaluationSummary, setEvaluationSummary] = useState<{
    total: number;
    eligible: number;
    ineligible: number;
    breakdown: Record<string, number>;
  } | null>(null);

  // Filter & Search
  const [filter, setFilter] = useState<"ALL" | "ELIGIBLE" | "SHORTLISTED">("ALL");
  const [searchQuery, setSearchQuery] = useState("");

  // Candidate Profile Modal
  const [viewStudentId, setViewStudentId] = useState<number | null>(null);

  // Updating single candidate status
  const [updatingCandidateId, setUpdatingCandidateId] = useState<number | null>(null);

  const fetchCandidates = useCallback(async () => {
    if (!drive) return;
    setLoading(true);
    setError("");
    try {
      const data = await recruitersApi.getDriveCandidates(drive.id);
      setCandidates(data);
    } catch (err: any) {
      setError(err?.message || "Failed to load candidates for this drive.");
    } finally {
      setLoading(false);
    }
  }, [drive]);

  useEffect(() => {
    if (isOpen && drive) {
      fetchCandidates();
      setEvaluationSummary(null);
      setSearchQuery("");
      setFilter("ALL");
    } else {
      setCandidates([]);
      setEvaluationSummary(null);
    }
  }, [isOpen, drive, fetchCandidates]);

  const handleBulkEvaluate = async () => {
    if (!drive) return;
    setEvaluating(true);
    try {
      const res = await recruitersApi.bulkEvaluateEligibility(drive.id);
      setEvaluationSummary({
        total: res.total_candidates,
        eligible: res.eligible_count,
        ineligible: res.ineligible_count,
        breakdown: res.failure_breakdown,
      });
      await fetchCandidates();
    } catch (err: any) {
      alert(err?.message || "Bulk evaluation failed.");
    } finally {
      setEvaluating(false);
    }
  };

  const handleUpdateStatus = async (
    candidateId: number,
    shortlistStatus: boolean
  ) => {
    if (!drive) return;
    setUpdatingCandidateId(candidateId);
    try {
      await recruitersApi.updateCandidateStatus(drive.id, candidateId, {
        shortlist_status: shortlistStatus,
      });
      // Update locally
      setCandidates((prev) =>
        prev.map((c) =>
          c.id === candidateId ? { ...c, shortlist_status: shortlistStatus } : c
        )
      );
    } catch (err: any) {
      alert(err?.message || "Failed to update candidate status.");
    } finally {
      setUpdatingCandidateId(null);
    }
  };

  const filteredCandidates = candidates.filter((c) => {
    if (filter === "ELIGIBLE" && !c.eligibility_status) return false;
    if (filter === "SHORTLISTED" && !c.shortlist_status) return false;
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      const name = c.student_name?.toLowerCase() || "";
      const id = c.student_identifier?.toLowerCase() || "";
      const branch = c.branch?.toLowerCase() || "";
      return name.includes(query) || id.includes(query) || branch.includes(query);
    }
    return true;
  });

  const eligibleCount = candidates.filter((c) => c.eligibility_status).length;
  const shortlistedCount = candidates.filter((c) => c.shortlist_status).length;

  return (
    <>
      <Modal
        isOpen={isOpen}
        onClose={onClose}
        title={drive ? `Candidates: ${drive.name}` : "Drive Candidates"}
        subtitle={drive ? `Event Date: ${drive.date} • Mode: ${drive.mode} • Venue: ${drive.venue || "Campus"}` : ""}
        size="2xl"
        footer={
          <div className="flex items-center justify-between w-full">
            <span className="text-xs text-gray-500 font-medium">
              Showing {filteredCandidates.length} of {candidates.length} candidate(s)
            </span>
            <Button variant="outline" size="sm" onClick={onClose}>
              Close
            </Button>
          </div>
        }
      >
        <div className="space-y-4">
          {/* Summary & Actions Bar */}
          <div className="p-4 bg-gray-50 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs font-semibold text-gray-700">Candidates:</span>
              <span className="px-2.5 py-1 bg-white border border-gray-200 rounded-full text-xs font-bold text-gray-800">
                Total: {candidates.length}
              </span>
              <span className="px-2.5 py-1 bg-emerald-50 border border-emerald-200 rounded-full text-xs font-bold text-emerald-700">
                Eligible: {eligibleCount}
              </span>
              <span className="px-2.5 py-1 bg-purple-50 border border-purple-200 rounded-full text-xs font-bold text-purple-700">
                Shortlisted: {shortlistedCount}
              </span>
            </div>

            <Button
              size="sm"
              variant="outline"
              onClick={handleBulkEvaluate}
              loading={evaluating}
              disabled={candidates.length === 0}
              className="text-xs shrink-0 font-semibold"
            >
              ⚡ Evaluate All Eligibility
            </Button>
          </div>

          {/* Bulk evaluation feedback alert */}
          {evaluationSummary && (
            <div className="p-3.5 bg-blue-50 border border-blue-200 rounded-xl text-xs text-blue-900 space-y-1">
              <div className="font-bold flex items-center justify-between">
                <span>Evaluation Complete:</span>
                <span className="text-2xs font-normal text-blue-600">
                  {evaluationSummary.eligible} Eligible / {evaluationSummary.ineligible} Ineligible
                </span>
              </div>
              <p className="text-2xs text-blue-700">
                Evaluated {evaluationSummary.total} candidate(s) against linked job rules.
                {Object.keys(evaluationSummary.breakdown).length > 0 && (
                  <span className="block mt-1 font-semibold">
                    Ineligible reasons: {Object.entries(evaluationSummary.breakdown).map(([r, c]) => `${r}: ${c}`).join(", ")}
                  </span>
                )}
              </p>
            </div>
          )}

          {/* Filters & Search */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-center gap-1.5">
              <button
                type="button"
                onClick={() => setFilter("ALL")}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                  filter === "ALL"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                }`}
              >
                All ({candidates.length})
              </button>
              <button
                type="button"
                onClick={() => setFilter("ELIGIBLE")}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                  filter === "ELIGIBLE"
                    ? "bg-emerald-600 text-white"
                    : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                }`}
              >
                Eligible ({eligibleCount})
              </button>
              <button
                type="button"
                onClick={() => setFilter("SHORTLISTED")}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                  filter === "SHORTLISTED"
                    ? "bg-purple-600 text-white"
                    : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                }`}
              >
                Shortlisted ({shortlistedCount})
              </button>
            </div>

            <div className="relative">
              <input
                type="text"
                placeholder="Search candidate name, ID, branch..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full sm:w-64 px-3 py-1.5 text-xs rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>

          {/* Candidates List / Table */}
          {loading ? (
            <LoadingState message="Loading registered candidates..." />
          ) : error ? (
            <div className="p-4 bg-rose-50 border border-rose-200 text-rose-700 text-xs rounded-lg">
              {error}
            </div>
          ) : filteredCandidates.length === 0 ? (
            <EmptyState
              title="No candidates found"
              description={
                candidates.length === 0
                  ? "No students have registered for this placement drive yet."
                  : "No candidates match the selected filter criteria."
              }
            />
          ) : (
            <div className="overflow-x-auto border border-gray-200 rounded-xl">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="bg-gray-50 border-b border-gray-200 text-gray-600 font-semibold uppercase text-2xs tracking-wider">
                    <th className="p-3">Candidate</th>
                    <th className="p-3">Dept & CGPA</th>
                    <th className="p-3">Eligibility</th>
                    <th className="p-3">Shortlist Status</th>
                    <th className="p-3 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {filteredCandidates.map((c) => (
                    <tr key={c.id} className="hover:bg-gray-50/70 transition-colors">
                      <td className="p-3">
                        <div className="font-bold text-gray-900">{c.student_name}</div>
                        <div className="text-2xs font-mono text-gray-500">
                          {c.student_identifier}
                        </div>
                        {c.email && (
                          <div className="text-2xs text-gray-400">{c.email}</div>
                        )}
                      </td>
                      <td className="p-3">
                        <div className="font-medium text-gray-800">{c.branch}</div>
                        <div className="text-2xs text-blue-600 font-bold">
                          CGPA: {c.cgpa} / 10.0
                        </div>
                        {c.graduation_year && (
                          <div className="text-2xs text-gray-400">
                            Class of {c.graduation_year}
                          </div>
                        )}
                      </td>
                      <td className="p-3">
                        {c.eligibility_status ? (
                          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-2xs font-bold bg-emerald-100 text-emerald-800">
                            ✓ Eligible
                          </span>
                        ) : (
                          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-2xs font-bold bg-rose-100 text-rose-800">
                            ✗ Ineligible
                          </span>
                        )}
                        <div className="text-2xs text-gray-400 mt-0.5">
                          Status: {c.registration_status}
                        </div>
                      </td>
                      <td className="p-3">
                        {c.shortlist_status ? (
                          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-2xs font-bold bg-purple-100 text-purple-800">
                            ★ Shortlisted
                          </span>
                        ) : (
                          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-2xs font-medium bg-gray-100 text-gray-600">
                            Under Review
                          </span>
                        )}
                      </td>
                      <td className="p-3 text-right">
                        <div className="flex items-center justify-end gap-1.5">
                          <Button
                            variant="outline"
                            size="sm"
                            className="text-2xs h-7 px-2"
                            onClick={() => setViewStudentId(c.student_id)}
                          >
                            Profile
                          </Button>
                          {c.shortlist_status ? (
                            <Button
                              variant="outline"
                              size="sm"
                              className="text-2xs h-7 px-2 text-rose-600 hover:text-rose-700 hover:bg-rose-50"
                              loading={updatingCandidateId === c.id}
                              onClick={() => handleUpdateStatus(c.id, false)}
                            >
                              Reject
                            </Button>
                          ) : (
                            <Button
                              variant="primary"
                              size="sm"
                              className="text-2xs h-7 px-2 bg-purple-600 hover:bg-purple-700 text-white"
                              loading={updatingCandidateId === c.id}
                              onClick={() => handleUpdateStatus(c.id, true)}
                            >
                              Shortlist
                            </Button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </Modal>

      {/* Candidate Profile Modal */}
      <CandidateProfileModal
        isOpen={viewStudentId !== null}
        onClose={() => setViewStudentId(null)}
        studentId={viewStudentId}
      />
    </>
  );
};
