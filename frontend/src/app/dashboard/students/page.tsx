"use client";

import React, { useEffect, useState, useCallback } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Modal } from "@/components/ui/Modal";
import { LoadingState } from "@/components/feedback/LoadingState";
import { ErrorState } from "@/components/feedback/ErrorState";
import { EmptyState } from "@/components/feedback/EmptyState";
import { adminApi, OfficerStudentItem } from "@/services/adminApi";
import { parseApiError } from "@/services/apiClient";

export default function OfficerStudentsPage() {
  const [students, setStudents] = useState<OfficerStudentItem[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Filters
  const [searchQuery, setSearchQuery] = useState("");
  const [branchFilter, setBranchFilter] = useState("ALL");
  const [minCgpa, setMinCgpa] = useState<string>("");

  // Detail Modal
  const [selectedStudentId, setSelectedStudentId] = useState<number | null>(null);
  const [studentDetail, setStudentDetail] = useState<any | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);

  const fetchStudents = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const res = await adminApi.getStudents({
        query: searchQuery.trim() || undefined,
        branch: branchFilter !== "ALL" ? branchFilter : undefined,
        min_cgpa: minCgpa ? parseFloat(minCgpa) : undefined,
        limit: 100,
      });
      setStudents(res.students);
      setTotal(res.total);
    } catch (err: any) {
      setError(parseApiError(err).message);
    } finally {
      setLoading(false);
    }
  }, [searchQuery, branchFilter, minCgpa]);

  useEffect(() => {
    fetchStudents();
  }, [fetchStudents]);

  const handleOpenDetail = async (studentId: number) => {
    setSelectedStudentId(studentId);
    setLoadingDetail(true);
    try {
      const detail = await adminApi.getStudentDetails(studentId);
      setStudentDetail(detail);
    } catch (err: any) {
      alert(parseApiError(err).message);
      setSelectedStudentId(null);
    } finally {
      setLoadingDetail(false);
    }
  };

  const branches = Array.from(
    new Set(students.map((s) => s.branch).filter(Boolean) as string[])
  ).sort();

  return (
    <AppLayout allowedRoles={["SUPER_ADMIN", "PLACEMENT_OFFICER"]}>
      <PageHeader
        title="Student Placement Directory"
        subtitle="Search candidates, monitor academic credentials, and review 7-dimension employability readiness scores."
        backHref="/dashboard"
        backLabel="Back to Dashboard"
      />

      {/* Filter Bar */}
      <Card className="mb-6">
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 items-center">
          <div className="sm:col-span-2">
            <input
              type="text"
              placeholder="Search candidate name, roll number, email..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-3.5 py-2 text-xs rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <select
              value={branchFilter}
              onChange={(e) => setBranchFilter(e.target.value)}
              className="w-full px-3 py-2 text-xs rounded-lg border border-gray-300 bg-white font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="ALL">All Departments</option>
              {branches.map((b) => (
                <option key={b} value={b}>
                  {b}
                </option>
              ))}
            </select>
          </div>

          <div>
            <select
              value={minCgpa}
              onChange={(e) => setMinCgpa(e.target.value)}
              className="w-full px-3 py-2 text-xs rounded-lg border border-gray-300 bg-white font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Any CGPA</option>
              <option value="6.0">CGPA ≥ 6.0</option>
              <option value="7.0">CGPA ≥ 7.0</option>
              <option value="8.0">CGPA ≥ 8.0</option>
              <option value="9.0">CGPA ≥ 9.0</option>
            </select>
          </div>
        </div>
      </Card>

      {/* Main Student Directory Table */}
      {loading ? (
        <LoadingState message="Loading student candidate directory..." />
      ) : error ? (
        <ErrorState message={error} onRetry={fetchStudents} />
      ) : students.length === 0 ? (
        <EmptyState
          title="No candidates match your search"
          description="Try relaxing your CGPA threshold or selecting all departments."
        />
      ) : (
        <Card padding="none">
          <div className="p-4 border-b border-gray-200 flex justify-between items-center bg-gray-50/50">
            <span className="text-xs font-bold text-gray-700">
              Total Candidates: <span className="text-blue-600">{total}</span>
            </span>
            <span className="text-2xs text-gray-400 font-medium">
              Click &quot;Profile&quot; to inspect credentials, project portfolio, and readiness breakdown
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-200 text-gray-600 font-semibold uppercase text-2xs tracking-wider">
                  <th className="p-3.5">Candidate</th>
                  <th className="p-3.5">Department</th>
                  <th className="p-3.5">Academic Standing</th>
                  <th className="p-3.5">Readiness Score</th>
                  <th className="p-3.5">Resume</th>
                  <th className="p-3.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {students.map((s) => (
                  <tr key={s.id} className="hover:bg-gray-50/70 transition-colors">
                    <td className="p-3.5">
                      <div className="font-bold text-gray-900">
                        {s.first_name} {s.last_name}
                      </div>
                      <div className="text-2xs text-gray-500 font-mono">
                        {s.student_identifier} • Class of {s.graduation_year}
                      </div>
                      {s.email && <div className="text-2xs text-gray-400">{s.email}</div>}
                    </td>
                    <td className="p-3.5 font-medium text-gray-800">
                      {s.branch}
                    </td>
                    <td className="p-3.5">
                      <div className="font-bold text-blue-600">
                        CGPA: {s.cgpa} / 10.0
                      </div>
                      <div className="text-2xs text-gray-500 mt-0.5">
                        {s.backlogs_current > 0 ? (
                          <span className="text-rose-600 font-semibold">
                            {s.backlogs_current} active backlogs
                          </span>
                        ) : (
                          <span className="text-emerald-600">0 backlogs</span>
                        )}
                      </div>
                    </td>
                    <td className="p-3.5">
                      {s.readiness_score !== null && s.readiness_score !== undefined ? (
                        <span
                          className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-black ${
                            s.readiness_score >= 75
                              ? "bg-emerald-100 text-emerald-800"
                              : s.readiness_score >= 50
                              ? "bg-blue-100 text-blue-800"
                              : "bg-amber-100 text-amber-800"
                          }`}
                        >
                          {Math.round(s.readiness_score)}%
                        </span>
                      ) : (
                        <span className="text-2xs text-gray-400 font-medium">
                          Not Evaluated
                        </span>
                      )}
                    </td>
                    <td className="p-3.5">
                      {s.resume_url ? (
                        <a
                          href={`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001"}${s.resume_url.replace("/api/v1", "")}`}
                          target="_blank"
                          rel="noreferrer"
                          className="text-2xs font-bold text-blue-600 hover:underline"
                        >
                          PDF &nearr;
                        </a>
                      ) : (
                        <span className="text-2xs text-gray-300">None</span>
                      )}
                    </td>
                    <td className="p-3.5 text-right">
                      <Button
                        variant="outline"
                        size="sm"
                        className="text-2xs h-7 px-2"
                        onClick={() => handleOpenDetail(s.id)}
                      >
                        Inspect Profile
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {/* Student Detail Modal */}
      {selectedStudentId && (
        <Modal
          isOpen={true}
          onClose={() => {
            setSelectedStudentId(null);
            setStudentDetail(null);
          }}
          title={studentDetail ? `${studentDetail.first_name} ${studentDetail.last_name}` : "Student Profile"}
          subtitle={studentDetail ? `Roll Number: ${studentDetail.student_identifier} • Department: ${studentDetail.branch}` : ""}
          size="2xl"
          footer={
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                setSelectedStudentId(null);
                setStudentDetail(null);
              }}
            >
              Close
            </Button>
          }
        >
          {loadingDetail || !studentDetail ? (
            <LoadingState message="Loading candidate credentials and readiness evaluation..." />
          ) : (
            <div className="space-y-6 text-xs">
              {/* Top Banner: Academic Summary */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-gray-50 p-4 rounded-xl">
                <div>
                  <span className="text-gray-400 block text-2xs">CGPA:</span>
                  <span className="font-bold text-blue-600 text-sm">
                    {studentDetail.cgpa} / 10.0
                  </span>
                </div>
                <div>
                  <span className="text-gray-400 block text-2xs">Backlogs:</span>
                  <span
                    className={`font-bold text-sm ${
                      studentDetail.backlogs_current > 0 ? "text-rose-600" : "text-emerald-600"
                    }`}
                  >
                    {studentDetail.backlogs_current} active
                  </span>
                </div>
                <div>
                  <span className="text-gray-400 block text-2xs">Graduation:</span>
                  <span className="font-semibold text-gray-800 text-sm">
                    Class of {studentDetail.graduation_year}
                  </span>
                </div>
                <div>
                  <span className="text-gray-400 block text-2xs">Contact Phone:</span>
                  <span className="font-semibold text-gray-800 text-sm">
                    {studentDetail.phone || "—"}
                  </span>
                </div>
              </div>

              {/* Readiness Evaluation Card */}
              {studentDetail.readiness && (
                <div className="p-4 bg-blue-50/50 border border-blue-200 rounded-xl space-y-3">
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-2xs uppercase font-bold text-blue-600 tracking-wider">
                        Employability Engine Evaluation
                      </span>
                      <h4 className="text-base font-bold text-gray-900 mt-0.5">
                        Readiness Score: {Math.round(studentDetail.readiness.readiness_score)}%
                      </h4>
                    </div>
                    <span className="px-3 py-1 bg-white border border-blue-200 rounded-full text-xs font-bold text-blue-700">
                      Level: {studentDetail.readiness.readiness_level}
                    </span>
                  </div>

                  {/* Dimension Breakdown */}
                  {studentDetail.readiness.dimensions && (
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2 border-t border-blue-100">
                      {studentDetail.readiness.dimensions.map((d: any) => (
                        <div key={d.name} className="bg-white p-2.5 rounded-lg border border-blue-100">
                          <span className="text-2xs text-gray-500 block truncate">{d.name}</span>
                          <span className="font-bold text-gray-900 text-xs">
                            {Math.round(d.score)}%
                          </span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* Skills */}
              <div>
                <h4 className="font-bold text-gray-900 mb-2">Verified Skills ({studentDetail.skills.length})</h4>
                {studentDetail.skills.length === 0 ? (
                  <p className="text-gray-400 text-2xs">No skills listed.</p>
                ) : (
                  <div className="flex flex-wrap gap-2">
                    {studentDetail.skills.map((sk: any) => (
                      <span
                        key={sk.id}
                        className="px-2.5 py-1 bg-gray-100 text-gray-800 rounded-lg text-2xs font-medium"
                      >
                        {sk.name} • <span className="font-bold text-blue-600">{sk.proficiency_level}</span>
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {/* Projects */}
              <div>
                <h4 className="font-bold text-gray-900 mb-2">Projects ({studentDetail.projects.length})</h4>
                {studentDetail.projects.length === 0 ? (
                  <p className="text-gray-400 text-2xs">No projects documented.</p>
                ) : (
                  <div className="space-y-2">
                    {studentDetail.projects.map((p: any) => (
                      <div key={p.id} className="p-3 bg-gray-50 rounded-lg border border-gray-100">
                        <div className="font-bold text-gray-900">{p.title}</div>
                        {p.description && <p className="text-gray-600 text-2xs mt-1">{p.description}</p>}
                        {p.technologies && (
                          <div className="text-2xs text-blue-600 font-medium mt-1">
                            Tech: {p.technologies}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </Modal>
      )}
    </AppLayout>
  );
}
