"use client";

import React, { useEffect, useState, useCallback } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { Tabs } from "@/components/ui/Tabs";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { Modal } from "@/components/ui/Modal";
import { LoadingState } from "@/components/feedback/LoadingState";
import { ErrorState } from "@/components/feedback/ErrorState";
import { EmptyState } from "@/components/feedback/EmptyState";
import { Toast } from "@/components/feedback/Toast";
import { FormError } from "@/components/forms/FormError";

import { studentsApi } from "@/services/studentsApi";
import { parseApiError } from "@/services/apiClient";

export default function JobsPage() {
  const [activeTab, setActiveTab] = useState<"jobs" | "drives" | "my-drives">("jobs");
  const [jobs, setJobs] = useState<any[]>([]);
  const [drives, setDrives] = useState<any[]>([]);
  const [myDrives, setMyDrives] = useState<any[]>([]);
  const [profile, setProfile] = useState<any>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  // Job Detail & Eligibility Modal
  const [selectedJob, setSelectedJob] = useState<any | null>(null);
  const [eligibilityData, setEligibilityData] = useState<any | null>(null);
  const [loadingEligibility, setLoadingEligibility] = useState(false);

  // Drive Registration state
  const [registeringDriveId, setRegisteringDriveId] = useState<number | null>(null);
  const [registrationError, setRegistrationError] = useState("");

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [jobsData, drivesData, myDrivesData, profData] = await Promise.all([
        studentsApi.getAvailableJobs(),
        studentsApi.getAvailableDrives(),
        studentsApi.getMyRegisteredDrives().catch(() => []),
        studentsApi.getProfile().catch(() => null),
      ]);
      setJobs(jobsData);
      setDrives(drivesData);
      setMyDrives(myDrivesData);
      setProfile(profData);
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

  // Open Job Details & Check Eligibility
  const handleOpenJobDetails = async (job: any) => {
    setSelectedJob(job);
    setEligibilityData(null);
    setLoadingEligibility(true);
    try {
      const data = await studentsApi.checkMyJobEligibility(job.id);
      setEligibilityData(data);
    } catch (err: any) {
      console.error("Eligibility check error", err);
    } finally {
      setLoadingEligibility(false);
    }
  };

  // Register for Drive
  const handleRegisterForDrive = async (drive: any) => {
    if (!profile?.basic_info?.id) {
      setToastMessage("Please complete your student profile before registering.");
      return;
    }
    setRegisteringDriveId(drive.id);
    setRegistrationError("");
    try {
      await studentsApi.registerForDrive(drive.id, profile.basic_info.id);
      setToastMessage(`Successfully registered for ${drive.name}!`);
      await fetchData();
    } catch (err: any) {
      const parsed = parseApiError(err);
      setRegistrationError(parsed.message);
      setToastMessage(parsed.message);
    } finally {
      setRegisteringDriveId(null);
    }
  };

  const [withdrawingDriveId, setWithdrawingDriveId] = useState<number | null>(null);
  const [applyingJobId, setApplyingJobId] = useState<number | null>(null);

  const handleWithdrawDrive = async (driveId: number) => {
    setWithdrawingDriveId(driveId);
    try {
      await studentsApi.withdrawDrive(driveId);
      setToastMessage("Drive registration withdrawn.");
      await fetchData();
    } catch (err: any) {
      setToastMessage(parseApiError(err).message);
    } finally {
      setWithdrawingDriveId(null);
    }
  };

  const handleDirectApply = async (jobId: number) => {
    setApplyingJobId(jobId);
    try {
      const res = await studentsApi.applyToJob(jobId);
      setToastMessage(res.message || "Application submitted successfully!");
      setSelectedJob(null);
      await fetchData();
    } catch (err: any) {
      setToastMessage(parseApiError(err).message);
    } finally {
      setApplyingJobId(null);
    }
  };

  const isAlreadyRegistered = (driveId: number) => {
    return myDrives.some((d) => d.drive_id === driveId && d.registration_status !== "WITHDRAWN");
  };

  return (
    <AppLayout allowedRoles={["STUDENT", "SUPER_ADMIN", "PLACEMENT_OFFICER"]}>
      <PageHeader
        title="Placement Opportunities & Drives"
        subtitle="Discover verified corporate job openings, check your eligibility in real time, and register for placement drives."
        backHref="/dashboard"
        backLabel="Back to Dashboard"
      />

      <Toast message={toastMessage} onDismiss={() => setToastMessage(null)} />

      <Tabs
        tabs={[
          { key: "jobs", label: "Available Jobs", count: jobs.length },
          { key: "drives", label: "Placement Drives", count: drives.length },
          { key: "my-drives", label: "My Registrations", count: myDrives.length },
        ]}
        activeKey={activeTab}
        onChange={(k: any) => setActiveTab(k)}
        className="mb-6"
      />

      {loading ? (
        <LoadingState message="Loading placement opportunities..." />
      ) : error ? (
        <ErrorState message={error} onRetry={fetchData} />
      ) : (
        <div className="space-y-6">
          {/* TAB 1: AVAILABLE JOBS */}
          {activeTab === "jobs" && (
            <div>
              {jobs.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {jobs.map((job) => (
                    <Card key={job.id} padding="none" className="hover:border-blue-300 transition shadow-xs">
                      <div className="p-6 flex flex-col h-full justify-between">
                        <div>
                          <div className="flex items-start justify-between gap-2 mb-2">
                            <div>
                              <span className="text-2xs font-bold uppercase tracking-wider text-blue-600 block">
                                {job.company_name}
                              </span>
                              <h3 className="text-base font-bold text-gray-900 mt-0.5">{job.title}</h3>
                            </div>
                            <StatusBadge status={job.employment_type} size="sm" variant="info" />
                          </div>

                          <p className="text-xs text-gray-600 line-clamp-3 mb-4 leading-relaxed">
                            {job.description}
                          </p>

                          <div className="grid grid-cols-2 gap-2 text-xs bg-gray-50 p-3 rounded-lg mb-4">
                            <div>
                              <span className="text-gray-400 block text-2xs">Location:</span>
                              <span className="font-semibold text-gray-800">{job.location || "Flexible"}</span>
                            </div>
                            <div>
                              <span className="text-gray-400 block text-2xs">Work Mode:</span>
                              <span className="font-semibold text-gray-800">{job.remote_type || "On-site"}</span>
                            </div>
                            <div>
                              <span className="text-gray-400 block text-2xs">Compensation:</span>
                              <span className="font-semibold text-emerald-700">{job.salary_range || "Competitive"}</span>
                            </div>
                            <div>
                              <span className="text-gray-400 block text-2xs">Vacancies:</span>
                              <span className="font-semibold text-gray-800">{job.openings ?? "—"} openings</span>
                            </div>
                          </div>

                          {job.requirements && job.requirements.length > 0 && (
                            <div className="mb-4">
                              <span className="text-2xs font-bold uppercase tracking-wider text-gray-500 block mb-1.5">
                                Required Skills
                              </span>
                              <div className="flex flex-wrap gap-1">
                                {job.requirements.slice(0, 4).map((r: any) => (
                                  <span
                                    key={r.id}
                                    className="px-2 py-0.5 rounded text-2xs font-medium bg-gray-100 text-gray-700"
                                  >
                                    {r.skill_name} ({r.required_proficiency})
                                  </span>
                                ))}
                                {job.requirements.length > 4 && (
                                  <span className="px-2 py-0.5 rounded text-2xs text-gray-400">
                                    +{job.requirements.length - 4} more
                                  </span>
                                )}
                              </div>
                            </div>
                          )}
                        </div>

                        <div className="pt-3 border-t border-gray-100 flex items-center justify-between">
                          <span className="text-2xs text-gray-400">
                            Deadline: {job.application_deadline ? new Date(job.application_deadline).toLocaleDateString() : "Rolling"}
                          </span>
                          <Button
                            size="sm"
                            variant="primary"
                            onClick={() => handleOpenJobDetails(job)}
                          >
                            Check Eligibility & Details &rarr;
                          </Button>
                        </div>
                      </div>
                    </Card>
                  ))}
                </div>
              ) : (
                <EmptyState
                  title="No active job postings found"
                  description="Companies have not published any open job requisitions yet. Please check back soon."
                />
              )}
            </div>
          )}

          {/* TAB 2: PLACEMENT DRIVES */}
          {activeTab === "drives" && (
            <div className="space-y-4">
              {registrationError && (
                <FormError error={registrationError} onDismiss={() => setRegistrationError("")} />
              )}

              {drives.length > 0 ? (
                <div className="space-y-4">
                  {drives.map((drive) => {
                    const registered = isAlreadyRegistered(drive.id);
                    const isDeadlinePassed = drive.registration_deadline && new Date() > new Date(drive.registration_deadline);

                    return (
                      <Card key={drive.id} padding="none">
                        <div className="p-6">
                          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-3">
                            <div>
                              <div className="flex items-center gap-2">
                                <h3 className="text-base font-bold text-gray-900">{drive.name}</h3>
                                <StatusBadge status={drive.status} size="sm" />
                              </div>
                              <p className="text-xs text-blue-600 font-medium mt-0.5">
                                Company: {drive.company_name} {drive.job_title ? `• Job: ${drive.job_title}` : ""}
                              </p>
                            </div>

                            <div className="flex items-center gap-2 shrink-0">
                              {registered ? (
                                <span className="px-3 py-1.5 rounded-lg text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
                                  ✓ Registered
                                </span>
                              ) : isDeadlinePassed ? (
                                <span className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-gray-100 text-gray-500">
                                  Registration Closed
                                </span>
                              ) : (
                                <Button
                                  size="sm"
                                  loading={registeringDriveId === drive.id}
                                  onClick={() => handleRegisterForDrive(drive)}
                                >
                                  Register for Drive
                                </Button>
                              )}
                            </div>
                          </div>

                          {drive.description && (
                            <p className="text-xs text-gray-700 leading-relaxed mb-4">
                              {drive.description}
                            </p>
                          )}

                          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs bg-gray-50 p-3 rounded-lg">
                            <div>
                              <span className="text-gray-400 block text-2xs">Drive Date:</span>
                              <span className="font-semibold text-gray-800">
                                {drive.date ? new Date(drive.date).toLocaleDateString() : "TBD"}
                              </span>
                            </div>
                            <div>
                              <span className="text-gray-400 block text-2xs">Mode & Venue:</span>
                              <span className="font-semibold text-gray-800">
                                {drive.mode} • {drive.venue || "Campus Labs"}
                              </span>
                            </div>
                            <div>
                              <span className="text-gray-400 block text-2xs">Seats Available:</span>
                              <span className="font-semibold text-emerald-700">
                                {drive.capacity ? `${drive.registered_count} / ${drive.capacity}` : "Open"}
                              </span>
                            </div>
                            <div>
                              <span className="text-gray-400 block text-2xs">Registration Deadline:</span>
                              <span className="font-semibold text-gray-800">
                                {drive.registration_deadline
                                  ? new Date(drive.registration_deadline).toLocaleDateString()
                                  : "Open"}
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
                  title="No upcoming placement drives"
                  description="Interview drives and recruitment events scheduled by companies will appear here."
                />
              )}
            </div>
          )}

          {/* TAB 3: MY REGISTRATIONS */}
          {activeTab === "my-drives" && (
            <div>
              {myDrives.length > 0 ? (
                <div className="space-y-4">
                  {myDrives.map((item) => (
                    <Card key={item.candidate_id} padding="none">
                      <div className="p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                        <div>
                          <div className="flex items-center gap-2">
                            <h3 className="text-base font-bold text-gray-900">{item.drive_name}</h3>
                            <StatusBadge status={item.registration_status} size="sm" />
                            {item.shortlist_status && (
                              <span className="px-2 py-0.5 rounded-full text-2xs font-black bg-purple-100 text-purple-800 border border-purple-300">
                                Shortlisted ⭐
                              </span>
                            )}
                          </div>
                          <p className="text-xs text-gray-500 mt-1">
                            {item.company_name} • Role: <strong className="text-gray-700">{item.job_title}</strong>
                          </p>
                          <div className="flex items-center gap-4 text-xs text-gray-500 mt-2">
                            <span>Date: <strong>{item.date ? new Date(item.date).toLocaleDateString() : "TBD"}</strong></span>
                            <span>Venue: <strong>{item.venue || item.mode}</strong></span>
                            <span>Registered on: <strong>{item.registration_timestamp ? new Date(item.registration_timestamp).toLocaleDateString() : "—"}</strong></span>
                          </div>
                        </div>

                        <div className="text-right shrink-0 flex flex-col items-end gap-2">
                          <div>
                            <span className="text-2xs text-gray-400 block mb-1">Eligibility Status</span>
                            <StatusBadge
                              status={item.eligibility_status ? "ELIGIBLE" : "NOT_ELIGIBLE"}
                              size="md"
                            />
                          </div>
                          {item.registration_status !== "WITHDRAWN" && (
                            <Button
                              variant="outline"
                              size="sm"
                              className="text-rose-600 hover:text-rose-700 hover:bg-rose-50 border-rose-200 text-2xs h-7 px-2"
                              loading={withdrawingDriveId === item.drive_id}
                              onClick={() => handleWithdrawDrive(item.drive_id)}
                            >
                              Withdraw Registration
                            </Button>
                          )}
                        </div>
                      </div>
                    </Card>
                  ))}
                </div>
              ) : (
                <EmptyState
                  title="You have not registered for any drives yet"
                  description="Switch to the Placement Drives tab to discover and register for active campus recruitment drives."
                  actionText="Browse Placement Drives"
                  onAction={() => setActiveTab("drives")}
                />
              )}
            </div>
          )}
        </div>
      )}

      {/* JOB DETAIL & LIVE ELIGIBILITY MODAL */}
      {selectedJob && (
        <Modal
          isOpen={Boolean(selectedJob)}
          onClose={() => setSelectedJob(null)}
          title={selectedJob.title}
          subtitle={`Company: ${selectedJob.company_name}`}
          size="2xl"
          footer={
            <div className="flex items-center justify-between w-full">
              <Button variant="outline" size="sm" onClick={() => setSelectedJob(null)}>
                Close
              </Button>
              <Button
                variant="primary"
                size="sm"
                disabled={!eligibilityData?.eligible}
                loading={applyingJobId === selectedJob.id}
                onClick={() => handleDirectApply(selectedJob.id)}
              >
                Apply Directly for Job
              </Button>
            </div>
          }
        >
          <div className="space-y-6">
            {/* Live Eligibility Evaluation Box */}
            <div className="p-4 rounded-xl border bg-gray-50">
              <span className="text-2xs font-bold uppercase tracking-wider text-gray-500 block mb-2">
                Deterministic Eligibility Check
              </span>

              {loadingEligibility ? (
                <p className="text-xs text-gray-500">Checking your profile against job eligibility rules...</p>
              ) : eligibilityData ? (
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold text-gray-700">Evaluation Result:</span>
                      <StatusBadge
                        status={eligibilityData.eligible ? "ELIGIBLE" : "NOT_ELIGIBLE"}
                        size="md"
                      />
                    </div>
                    <span className="text-xs text-gray-500">
                      Your CGPA: <strong>{eligibilityData.student_cgpa}</strong> | Backlogs: <strong>{eligibilityData.student_backlogs}</strong>
                    </span>
                  </div>

                  {!eligibilityData.eligible && eligibilityData.reasons && eligibilityData.reasons.length > 0 && (
                    <div className="p-3 bg-rose-50 border border-rose-200 rounded-lg text-xs text-rose-700">
                      <strong className="block mb-1">You are currently ineligible for the following reason(s):</strong>
                      <ul className="list-disc pl-5 space-y-0.5">
                        {eligibilityData.reasons.map((r: string, i: number) => (
                          <li key={i}>{r}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {eligibilityData.eligible && (
                    <p className="text-xs text-emerald-700 font-medium">
                      ✓ Congratulations! Your profile satisfies all academic and backlog requirements for this role.
                    </p>
                  )}
                </div>
              ) : null}
            </div>

            {/* Description */}
            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">Role Overview</h4>
              <p className="text-xs text-gray-700 leading-relaxed whitespace-pre-line">
                {selectedJob.description}
              </p>
            </div>

            {/* Hard Eligibility Rules Config */}
            {selectedJob.eligibility_config && (
              <div className="p-4 bg-blue-50/50 border border-blue-100 rounded-xl">
                <h4 className="text-xs font-bold uppercase tracking-wider text-blue-900 mb-2">
                  Strict Eligibility Criteria
                </h4>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                  <div>
                    <span className="text-gray-500 block text-2xs">Minimum CGPA:</span>
                    <span className="font-bold text-gray-900">
                      {selectedJob.eligibility_config.min_cgpa ?? "None"}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-500 block text-2xs">Max Backlogs:</span>
                    <span className="font-bold text-gray-900">
                      {selectedJob.eligibility_config.max_backlogs ?? "None"}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-500 block text-2xs">Graduation Year:</span>
                    <span className="font-bold text-gray-900">
                      {selectedJob.eligibility_config.graduation_year ?? "All"}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-500 block text-2xs">Allowed Branches:</span>
                    <span className="font-bold text-gray-900">
                      {selectedJob.eligibility_config.allowed_branches?.join(", ") || "All Branches"}
                    </span>
                  </div>
                </div>
              </div>
            )}

            {/* Skill Requirements */}
            {selectedJob.requirements && selectedJob.requirements.length > 0 && (
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">
                  Skill Requirements ({selectedJob.requirements.length})
                </h4>
                <div className="divide-y divide-gray-100 border border-gray-200 rounded-lg overflow-hidden">
                  {selectedJob.requirements.map((r: any) => (
                    <div key={r.id} className="p-3 bg-white flex items-center justify-between text-xs">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-gray-900">{r.skill_name}</span>
                        <StatusBadge status={r.required_proficiency} size="sm" />
                        {r.is_mandatory ? (
                          <span className="px-2 py-0.5 rounded text-2xs font-bold bg-rose-50 text-rose-700 border border-rose-200">
                            Mandatory
                          </span>
                        ) : (
                          <span className="px-2 py-0.5 rounded text-2xs bg-gray-100 text-gray-600">
                            Preferred
                          </span>
                        )}
                      </div>
                      <span className="text-gray-500">Weight: {r.weight}x</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </Modal>
      )}
    </AppLayout>
  );
}
