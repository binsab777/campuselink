"use client";

import React, { useEffect, useState, useCallback } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { Tabs } from "@/components/ui/Tabs";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { LoadingState } from "@/components/feedback/LoadingState";
import { ErrorState } from "@/components/feedback/ErrorState";
import { EmptyState } from "@/components/feedback/EmptyState";
import { Toast } from "@/components/feedback/Toast";

import { CompanyModal } from "@/features/recruiters/CompanyModal";
import { JobModal } from "@/features/recruiters/JobModal";
import { JobRequirementsModal } from "@/features/recruiters/JobRequirementsModal";
import { DriveModal } from "@/features/recruiters/DriveModal";
import { EligibilitySandboxCard } from "@/features/recruiters/EligibilitySandboxCard";
import { JobPreviewModal } from "@/features/recruiters/JobPreviewModal";
import { CandidateManagementModal } from "@/features/recruiters/CandidateManagementModal";

import {
  CompanyData,
  JobData,
  DriveData,
  SkillItem,
  RecruiterProfile,
} from "@/features/recruiters/types";
import { recruitersApi, RecruiterDashboardMetrics } from "@/services/recruitersApi";
import { parseApiError } from "@/services/apiClient";

export default function RecruiterDashboard() {
  const [activeTab, setActiveTab] = useState<"company" | "jobs" | "drives">("company");
  const [profile, setProfile] = useState<RecruiterProfile | null>(null);
  const [jobs, setJobs] = useState<JobData[]>([]);
  const [drives, setDrives] = useState<DriveData[]>([]);
  const [skillsList, setSkillsList] = useState<SkillItem[]>([]);
  const [metrics, setMetrics] = useState<RecruiterDashboardMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  // Modals
  const [isCompanyModalOpen, setIsCompanyModalOpen] = useState(false);

  const [isJobModalOpen, setIsJobModalOpen] = useState(false);
  const [selectedJob, setSelectedJob] = useState<JobData | null>(null);

  const [isReqModalOpen, setIsReqModalOpen] = useState(false);
  const [selectedJobForReqs, setSelectedJobForReqs] = useState<JobData | null>(null);

  const [isDriveModalOpen, setIsDriveModalOpen] = useState(false);
  const [selectedDrive, setSelectedDrive] = useState<DriveData | null>(null);

  // Completeness Audit Additions: Preview & Candidate Management
  const [previewJob, setPreviewJob] = useState<JobData | null>(null);
  const [selectedDriveForCandidates, setSelectedDriveForCandidates] = useState<DriveData | null>(null);
  const [actionLoadingId, setActionLoadingId] = useState<string | null>(null);

  // Confirm delete dialog
  const [confirmDelete, setConfirmDelete] = useState<{
    isOpen: boolean;
    title: string;
    message: string;
    onConfirm: () => Promise<void>;
  }>({
    isOpen: false,
    title: "",
    message: "",
    onConfirm: async () => {},
  });
  const [deleting, setDeleting] = useState(false);

  const showToast = (msg: string) => {
    setToastMessage(msg);
  };

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [profileData, jobsData, drivesData, skillsData, metricsData] = await Promise.all([
        recruitersApi.getProfile(),
        recruitersApi.getJobs(),
        recruitersApi.getDrives(),
        recruitersApi.getSkills().catch(() => [] as SkillItem[]),
        recruitersApi.getDashboardMetrics().catch(() => null),
      ]);

      setProfile(profileData);
      setJobs(jobsData);
      setDrives(drivesData);
      setSkillsList(skillsData);
      setMetrics(metricsData);
    } catch (err: any) {
      const parsed = parseApiError(err);
      setError(parsed.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Quick Status Transition for Jobs
  const handleUpdateJobStatus = async (jobId: number, newStatus: "DRAFT" | "PUBLISHED" | "CLOSED") => {
    setActionLoadingId(`job-${jobId}`);
    try {
      await recruitersApi.updateJob(jobId, { status: newStatus });
      showToast(`Job status updated to ${newStatus}.`);
      await fetchData();
    } catch (err: any) {
      showToast(parseApiError(err).message);
    } finally {
      setActionLoadingId(null);
    }
  };

  // Quick Status Transition for Placement Drives
  const handleUpdateDriveStatus = async (
    driveId: number,
    newStatus: "DRAFT" | "PUBLISHED" | "REGISTRATION_OPEN" | "IN_PROGRESS" | "COMPLETED" | "CANCELLED"
  ) => {
    setActionLoadingId(`drive-${driveId}`);
    try {
      await recruitersApi.updateDrive(driveId, { status: newStatus });
      showToast(`Drive status updated to ${newStatus}.`);
      await fetchData();
    } catch (err: any) {
      showToast(parseApiError(err).message);
    } finally {
      setActionLoadingId(null);
    }
  };

  // Delete Job Handler
  const handleDeleteJob = (job: JobData) => {
    setConfirmDelete({
      isOpen: true,
      title: "Delete Job Posting",
      message: `Are you sure you want to permanently delete "${job.title}"? Any linked requirements will also be removed.`,
      onConfirm: async () => {
        setDeleting(true);
        try {
          await recruitersApi.deleteJob(job.id);
          showToast("Job posting deleted.");
          await fetchData();
        } catch (err: any) {
          showToast(parseApiError(err).message);
        } finally {
          setDeleting(false);
          setConfirmDelete((prev) => ({ ...prev, isOpen: false }));
        }
      },
    });
  };

  // Delete Drive Handler
  const handleDeleteDrive = (drive: DriveData) => {
    setConfirmDelete({
      isOpen: true,
      title: "Delete Placement Drive",
      message: `Are you sure you want to cancel and remove drive "${drive.name}"?`,
      onConfirm: async () => {
        setDeleting(true);
        try {
          await recruitersApi.deleteDrive(drive.id);
          showToast("Placement drive deleted.");
          await fetchData();
        } catch (err: any) {
          showToast(parseApiError(err).message);
        } finally {
          setDeleting(false);
          setConfirmDelete((prev) => ({ ...prev, isOpen: false }));
        }
      },
    });
  };

  return (
    <AppLayout allowedRoles={["RECRUITER", "SUPER_ADMIN", "PLACEMENT_OFFICER"]}>
      <PageHeader
        title="Recruiter Portal & Placement Operations"
        subtitle="Manage corporate profiles, job requisitions, skill criteria, and placement drive schedules."
        backHref="/dashboard"
        backLabel="Back to Dashboard"
      />

      <Toast message={toastMessage} onDismiss={() => setToastMessage(null)} />

      <ConfirmDialog
        isOpen={confirmDelete.isOpen}
        title={confirmDelete.title}
        message={confirmDelete.message}
        onClose={() => setConfirmDelete((prev) => ({ ...prev, isOpen: false }))}
        onConfirm={confirmDelete.onConfirm}
        loading={deleting}
      />

      {/* Recruiter Top Metrics Strip */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex flex-col justify-between">
          <span className="text-2xs font-bold text-gray-500 uppercase tracking-wider">
            Active Jobs
          </span>
          <div className="flex items-baseline justify-between mt-2">
            <span className="text-2xl font-black text-blue-600">
              {metrics?.active_jobs_count ?? jobs.filter((j) => j.status === "PUBLISHED").length}
            </span>
            <span className="text-2xs text-gray-400 font-medium">
              {jobs.length} Total Postings
            </span>
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex flex-col justify-between">
          <span className="text-2xs font-bold text-gray-500 uppercase tracking-wider">
            Upcoming Drives
          </span>
          <div className="flex items-baseline justify-between mt-2">
            <span className="text-2xl font-black text-emerald-600">
              {metrics?.upcoming_drives_count ?? drives.filter((d) => d.status !== "COMPLETED" && d.status !== "CANCELLED").length}
            </span>
            <span className="text-2xs text-gray-400 font-medium">
              {drives.length} Total Drives
            </span>
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex flex-col justify-between">
          <span className="text-2xs font-bold text-gray-500 uppercase tracking-wider">
            Total Candidates
          </span>
          <div className="flex items-baseline justify-between mt-2">
            <span className="text-2xl font-black text-indigo-600">
              {metrics?.total_candidates_count ?? 0}
            </span>
            <span className="text-2xs text-gray-400 font-medium">
              Across All Drives
            </span>
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex flex-col justify-between">
          <span className="text-2xs font-bold text-gray-500 uppercase tracking-wider">
            Shortlisted
          </span>
          <div className="flex items-baseline justify-between mt-2">
            <span className="text-2xl font-black text-purple-600">
              {metrics?.shortlisted_candidates_count ?? 0}
            </span>
            <span className="text-2xs text-gray-400 font-medium">
              Ready for Interviews
            </span>
          </div>
        </div>
      </div>

      <Tabs
        tabs={[
          { key: "company", label: "Company Profile" },
          { key: "jobs", label: "Job Postings", count: jobs.length },
          { key: "drives", label: "Placement Drives", count: drives.length },
        ]}
        activeKey={activeTab}
        onChange={(k: any) => setActiveTab(k)}
        className="mb-6"
      />

      {loading ? (
        <LoadingState message="Loading recruiter dashboard..." />
      ) : error ? (
        <ErrorState message={error} onRetry={fetchData} />
      ) : (
        <div className="space-y-8">
          {/* TAB 1: COMPANY */}
          {activeTab === "company" && (
            <div className="space-y-6">
              <Card
                title={profile?.company?.name || "Company Information"}
                subtitle="Primary profile details visible to college placement teams and students."
                action={
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setIsCompanyModalOpen(true)}
                  >
                    Edit Company
                  </Button>
                }
              >
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 text-xs">
                  <div className="p-3 bg-gray-50 rounded-lg">
                    <span className="text-gray-500 block">Industry</span>
                    <span className="text-sm font-semibold text-gray-900 mt-0.5 block">
                      {profile?.company?.industry || "—"}
                    </span>
                  </div>
                  <div className="p-3 bg-gray-50 rounded-lg">
                    <span className="text-gray-500 block">Company Size</span>
                    <span className="text-sm font-semibold text-gray-900 mt-0.5 block">
                      {profile?.company?.size ? `${profile.company.size} employees` : "—"}
                    </span>
                  </div>
                  <div className="p-3 bg-gray-50 rounded-lg">
                    <span className="text-gray-500 block">Website</span>
                    {profile?.company?.website ? (
                      <a
                        href={profile.company.website}
                        target="_blank"
                        rel="noreferrer"
                        className="text-sm font-semibold text-blue-600 hover:underline mt-0.5 block break-all"
                      >
                        {profile.company.website} &nearr;
                      </a>
                    ) : (
                      <span className="text-sm text-gray-400 mt-0.5 block">—</span>
                    )}
                  </div>
                  <div className="p-3 bg-gray-50 rounded-lg">
                    <span className="text-gray-500 block">Headquarters</span>
                    <span className="text-sm font-semibold text-gray-900 mt-0.5 block">
                      {profile?.company?.headquarters || "—"}
                    </span>
                  </div>
                </div>

                {profile?.company?.description && (
                  <div className="mt-4 p-4 bg-gray-50 rounded-lg text-xs">
                    <span className="font-bold text-gray-800 block mb-1">About Company</span>
                    <p className="text-gray-600 leading-relaxed">
                      {profile.company.description}
                    </p>
                  </div>
                )}
              </Card>

              {/* Recruiter Representative info */}
              <Card
                title="Your Representative Account"
                subtitle="Authorized coordinator credentials for campus placement communications."
              >
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
                  <div className="p-3 bg-gray-50 rounded-lg">
                    <span className="text-gray-500 block">Designation</span>
                    <span className="text-sm font-semibold text-gray-900 mt-0.5 block">
                      {profile?.designation || "Campus Talent Lead"}
                    </span>
                  </div>
                  <div className="p-3 bg-gray-50 rounded-lg">
                    <span className="text-gray-500 block">Phone</span>
                    <span className="text-sm font-semibold text-gray-900 mt-0.5 block">
                      {profile?.phone || "—"}
                    </span>
                  </div>
                  <div className="p-3 bg-gray-50 rounded-lg">
                    <span className="text-gray-500 block">Recruiter ID</span>
                    <span className="text-sm font-mono font-semibold text-gray-900 mt-0.5 block">
                      REC-{profile?.id}
                    </span>
                  </div>
                </div>
              </Card>
            </div>
          )}

          {/* TAB 2: JOBS */}
          {activeTab === "jobs" && (
            <div className="space-y-6">
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="text-lg font-bold text-gray-900">Job Requisitions</h3>
                  <p className="text-xs text-gray-500">
                    Publish roles, set strict eligibility rules, and configure required skill weights.
                  </p>
                </div>
                <Button
                  size="sm"
                  onClick={() => {
                    setSelectedJob(null);
                    setIsJobModalOpen(true);
                  }}
                >
                  + Create Job Posting
                </Button>
              </div>

              {jobs.length > 0 ? (
                <div className="space-y-4">
                  {jobs.map((job) => (
                    <Card key={job.id} padding="none">
                      <div className="p-6">
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-3">
                          <div>
                            <div className="flex items-center gap-2">
                              <h4 className="text-base font-bold text-gray-900">{job.title}</h4>
                              <StatusBadge status={job.status} size="sm" />
                            </div>
                            <p className="text-xs text-gray-500 mt-0.5">
                              {job.employment_type} • {job.remote_type || "On-site"} • {job.location || "Location not specified"}
                            </p>
                          </div>

                          <div className="flex items-center flex-wrap gap-2 shrink-0">
                            {/* Candidate Preview */}
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => setPreviewJob(job)}
                            >
                              Preview
                            </Button>

                            {/* Status transitions */}
                            {job.status === "DRAFT" && (
                              <Button
                                variant="primary"
                                size="sm"
                                className="bg-emerald-600 hover:bg-emerald-700 text-white"
                                loading={actionLoadingId === `job-${job.id}`}
                                onClick={() => handleUpdateJobStatus(job.id, "PUBLISHED")}
                              >
                                Publish
                              </Button>
                            )}

                            {job.status === "PUBLISHED" && (
                              <Button
                                variant="outline"
                                size="sm"
                                className="text-amber-700 hover:bg-amber-50"
                                loading={actionLoadingId === `job-${job.id}`}
                                onClick={() => handleUpdateJobStatus(job.id, "CLOSED")}
                              >
                                Close Job
                              </Button>
                            )}

                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => {
                                setSelectedJobForReqs(job);
                                setIsReqModalOpen(true);
                              }}
                            >
                              Skill Requirements ({job.requirements?.length || 0})
                            </Button>

                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => {
                                setSelectedJob(job);
                                setIsJobModalOpen(true);
                              }}
                            >
                              Edit
                            </Button>

                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleDeleteJob(job)}
                              className="text-rose-600 hover:text-rose-700 hover:bg-rose-50"
                            >
                              Delete
                            </Button>
                          </div>
                        </div>

                        <p className="text-xs text-gray-700 leading-relaxed mb-4 line-clamp-2">
                          {job.description}
                        </p>

                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs bg-gray-50 p-3 rounded-lg">
                          <div>
                            <span className="text-gray-500 block">Openings:</span>
                            <span className="font-semibold text-gray-900">{job.openings ?? "—"} vacancies</span>
                          </div>
                          <div>
                            <span className="text-gray-500 block">Compensation:</span>
                            <span className="font-semibold text-gray-900">{job.salary_range || "Competitive"}</span>
                          </div>
                          <div>
                            <span className="text-gray-500 block">Min CGPA:</span>
                            <span className="font-semibold text-blue-600">
                              {job.eligibility_config?.min_cgpa ? `${job.eligibility_config.min_cgpa} / 10.0` : "None"}
                            </span>
                          </div>
                          <div>
                            <span className="text-gray-500 block">Deadline:</span>
                            <span className="font-semibold text-gray-900">
                              {job.application_deadline ? new Date(job.application_deadline).toLocaleDateString() : "Rolling"}
                            </span>
                          </div>
                        </div>
                      </div>
                    </Card>
                  ))}
                </div>
              ) : (
                <EmptyState
                  title="No job postings created"
                  description="Publish your first campus job opening to begin accepting candidate registrations."
                  actionText="Create Job Posting"
                  onAction={() => {
                    setSelectedJob(null);
                    setIsJobModalOpen(true);
                  }}
                />
              )}

              {/* Eligibility Sandbox */}
              {jobs.length > 0 && <EligibilitySandboxCard jobs={jobs} />}
            </div>
          )}

          {/* TAB 3: DRIVES */}
          {activeTab === "drives" && (
            <div className="space-y-6">
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="text-lg font-bold text-gray-900">Placement Drives</h3>
                  <p className="text-xs text-gray-500">
                    Schedule on-campus and virtual hiring events, interview blocks, and candidate quotas.
                  </p>
                </div>
                <Button
                  size="sm"
                  disabled={jobs.length === 0}
                  onClick={() => {
                    setSelectedDrive(null);
                    setIsDriveModalOpen(true);
                  }}
                >
                  + Schedule Placement Drive
                </Button>
              </div>

              {jobs.length === 0 && (
                <div className="p-4 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-800">
                  ⚠️ You must create at least one job posting before scheduling a placement drive.
                </div>
              )}

              {drives.length > 0 ? (
                <div className="space-y-4">
                  {drives.map((drive) => {
                    const linkedJob = jobs.find((j) => j.id === drive.job_id);
                    return (
                      <Card key={drive.id} padding="none">
                        <div className="p-6">
                          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-3">
                            <div>
                              <div className="flex items-center gap-2">
                                <h4 className="text-base font-bold text-gray-900">{drive.name}</h4>
                                <StatusBadge status={drive.status} size="sm" />
                              </div>
                              <p className="text-xs text-blue-600 font-medium mt-0.5">
                                Linked Job: {linkedJob?.title || `Job #${drive.job_id}`}
                              </p>
                            </div>

                            <div className="flex items-center flex-wrap gap-2 shrink-0">
                              {/* Manage Registered Candidates */}
                              <Button
                                variant="primary"
                                size="sm"
                                className="bg-indigo-600 hover:bg-indigo-700 text-white"
                                onClick={() => setSelectedDriveForCandidates(drive)}
                              >
                                Manage Candidates
                              </Button>

                              {/* Drive Status Quick Transitions */}
                              {drive.status === "DRAFT" && (
                                <Button
                                  variant="outline"
                                  size="sm"
                                  className="text-blue-600 border-blue-200 hover:bg-blue-50"
                                  loading={actionLoadingId === `drive-${drive.id}`}
                                  onClick={() => handleUpdateDriveStatus(drive.id, "PUBLISHED")}
                                >
                                  Publish
                                </Button>
                              )}

                              {drive.status === "PUBLISHED" && (
                                <Button
                                  variant="outline"
                                  size="sm"
                                  className="text-emerald-600 border-emerald-200 hover:bg-emerald-50"
                                  loading={actionLoadingId === `drive-${drive.id}`}
                                  onClick={() => handleUpdateDriveStatus(drive.id, "REGISTRATION_OPEN")}
                                >
                                  Open Reg.
                                </Button>
                              )}

                              {drive.status === "REGISTRATION_OPEN" && (
                                <Button
                                  variant="outline"
                                  size="sm"
                                  className="text-amber-600 border-amber-200 hover:bg-amber-50"
                                  loading={actionLoadingId === `drive-${drive.id}`}
                                  onClick={() => handleUpdateDriveStatus(drive.id, "IN_PROGRESS")}
                                >
                                  Close Reg.
                                </Button>
                              )}

                              {drive.status === "IN_PROGRESS" && (
                                <Button
                                  variant="outline"
                                  size="sm"
                                  className="text-purple-600 border-purple-200 hover:bg-purple-50"
                                  loading={actionLoadingId === `drive-${drive.id}`}
                                  onClick={() => handleUpdateDriveStatus(drive.id, "COMPLETED")}
                                >
                                  Complete
                                </Button>
                              )}

                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => {
                                  setSelectedDrive(drive);
                                  setIsDriveModalOpen(true);
                                }}
                              >
                                Edit
                              </Button>

                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleDeleteDrive(drive)}
                                className="text-rose-600 hover:text-rose-700 hover:bg-rose-50"
                              >
                                Delete
                              </Button>
                            </div>
                          </div>

                          {drive.description && (
                            <p className="text-xs text-gray-700 leading-relaxed mb-4">
                              {drive.description}
                            </p>
                          )}

                          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs bg-gray-50 p-3 rounded-lg">
                            <div>
                              <span className="text-gray-500 block">Date & Timing:</span>
                              <span className="font-semibold text-gray-900">
                                {drive.date} ({drive.start_time} - {drive.end_time})
                              </span>
                            </div>
                            <div>
                              <span className="text-gray-500 block">Mode & Venue:</span>
                              <span className="font-semibold text-gray-900">
                                {drive.mode} • {drive.venue || "Campus Labs"}
                              </span>
                            </div>
                            <div>
                              <span className="text-gray-500 block">Candidate Capacity:</span>
                              <span className="font-semibold text-emerald-700">
                                {drive.capacity ?? "Unlimited"} seats
                              </span>
                            </div>
                            <div>
                              <span className="text-gray-500 block">Registration Deadline:</span>
                              <span className="font-semibold text-gray-900">
                                {drive.registration_deadline
                                  ? new Date(drive.registration_deadline).toLocaleDateString()
                                  : "Open until drive"}
                              </span>
                            </div>
                          </div>
                        </div>
                      </Card>
                    );
                  })}
                </div>
              ) : (
                <EmptyState
                  title="No placement drives scheduled"
                  description="Schedule an interview drive once your job requirements and eligibility rules are published."
                  actionText={jobs.length > 0 ? "Schedule Drive" : undefined}
                  onAction={() => {
                    setSelectedDrive(null);
                    setIsDriveModalOpen(true);
                  }}
                />
              )}
            </div>
          )}
        </div>
      )}

      {/* Feature Modals */}
      <CompanyModal
        isOpen={isCompanyModalOpen}
        onClose={() => setIsCompanyModalOpen(false)}
        company={profile?.company}
        onSuccess={() => {
          showToast("Company profile updated.");
          fetchData();
        }}
      />

      <JobModal
        isOpen={isJobModalOpen}
        onClose={() => setIsJobModalOpen(false)}
        job={selectedJob}
        onSuccess={() => {
          showToast(selectedJob ? "Job updated." : "Job posting published.");
          fetchData();
        }}
      />

      <JobRequirementsModal
        isOpen={isReqModalOpen}
        onClose={() => setIsReqModalOpen(false)}
        job={selectedJobForReqs}
        skillsList={skillsList}
        onSuccess={() => {
          showToast("Skill requirements updated.");
          fetchData();
        }}
      />

      <DriveModal
        isOpen={isDriveModalOpen}
        onClose={() => setIsDriveModalOpen(false)}
        drive={selectedDrive}
        jobs={jobs}
        onSuccess={() => {
          showToast(selectedDrive ? "Drive updated." : "Placement drive scheduled.");
          fetchData();
        }}
      />

      {/* Completeness Audit Feature Modals */}
      <JobPreviewModal
        isOpen={previewJob !== null}
        onClose={() => setPreviewJob(null)}
        job={previewJob}
        companyName={profile?.company?.name}
      />

      <CandidateManagementModal
        isOpen={selectedDriveForCandidates !== null}
        onClose={() => {
          setSelectedDriveForCandidates(null);
          fetchData();
        }}
        drive={selectedDriveForCandidates}
      />
    </AppLayout>
  );
}
