"use client";

import React, { useEffect, useState } from "react";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { LoadingState } from "@/components/feedback/LoadingState";
import { recruitersApi } from "@/services/recruitersApi";

export interface CandidateProfileModalProps {
  isOpen: boolean;
  onClose: () => void;
  studentId: number | null;
}

export const CandidateProfileModal: React.FC<CandidateProfileModalProps> = ({
  isOpen,
  onClose,
  studentId,
}) => {
  const [profile, setProfile] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (isOpen && studentId) {
      setLoading(true);
      setError("");
      recruitersApi
        .getCandidateProfile(studentId)
        .then((data) => setProfile(data))
        .catch((err) => setError(err?.message || "Failed to load candidate profile."))
        .finally(() => setLoading(false));
    } else {
      setProfile(null);
    }
  }, [isOpen, studentId]);

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={profile ? `${profile.first_name} ${profile.last_name}` : "Candidate Profile"}
      subtitle={profile ? `Identifier: ${profile.student_identifier} • Department: ${profile.branch}` : ""}
      size="2xl"
      footer={
        <Button variant="outline" size="sm" onClick={onClose}>
          Close Profile
        </Button>
      }
    >
      {loading ? (
        <LoadingState message="Loading candidate credentials and academic records..." />
      ) : error ? (
        <div className="p-4 bg-rose-50 border border-rose-200 text-rose-700 text-xs rounded-lg">
          {error}
        </div>
      ) : profile ? (
        <div className="space-y-6">
          {/* Academic & Contact Summary */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs bg-gray-50 p-4 rounded-xl">
            <div>
              <span className="text-gray-400 block text-2xs">CGPA:</span>
              <span className="font-bold text-blue-600 text-sm">{profile.cgpa} / 10.0</span>
            </div>
            <div>
              <span className="text-gray-400 block text-2xs">Active Backlogs:</span>
              <span className={`font-bold text-sm ${profile.backlogs_current > 0 ? "text-rose-600" : "text-emerald-600"}`}>
                {profile.backlogs_current}
              </span>
            </div>
            <div>
              <span className="text-gray-400 block text-2xs">Graduation:</span>
              <span className="font-semibold text-gray-800 text-sm">{profile.graduation_year || "—"}</span>
            </div>
            <div>
              <span className="text-gray-400 block text-2xs">Contact Phone:</span>
              <span className="font-semibold text-gray-800 text-sm">{profile.phone || "—"}</span>
            </div>
          </div>

          {/* Resume View */}
          {profile.resume_url && (
            <div className="p-3.5 bg-emerald-50 border border-emerald-200 rounded-xl flex items-center justify-between">
              <div className="flex items-center gap-2 text-xs text-emerald-900 font-semibold">
                <span>📄 Candidate Resume Available</span>
              </div>
              <a
                href={`http://localhost:8000${profile.resume_url}`}
                target="_blank"
                rel="noreferrer"
                className="text-xs font-bold text-emerald-700 hover:underline inline-flex items-center gap-1"
              >
                <span>Open Resume PDF</span>
                <span>&nearr;</span>
              </a>
            </div>
          )}

          {/* Bio */}
          {profile.profile_metadata?.bio && (
            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-gray-700 mb-1">
                Candidate Bio
              </h4>
              <p className="text-xs text-gray-700 leading-relaxed bg-white p-3 border border-gray-100 rounded-lg">
                {profile.profile_metadata.bio}
              </p>
            </div>
          )}

          {/* Technical Skills */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">
              Verified Skills ({profile.skills?.length || 0})
            </h4>
            {profile.skills && profile.skills.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {profile.skills.map((s: any) => (
                  <div key={s.id} className="p-2 bg-gray-50 border border-gray-200 rounded-lg flex items-center gap-2 text-xs">
                    <span className="font-semibold text-gray-900">{s.skill_name}</span>
                    <StatusBadge status={s.proficiency_level} size="sm" />
                    <span className="text-2xs text-gray-400">{s.months_experience} mo</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-gray-400">No skills listed.</p>
            )}
          </div>

          {/* Projects */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">
              Applied Projects ({profile.projects?.length || 0})
            </h4>
            {profile.projects && profile.projects.length > 0 ? (
              <div className="space-y-2">
                {profile.projects.map((p: any) => (
                  <div key={p.id} className="p-3 bg-white border border-gray-200 rounded-lg text-xs">
                    <div className="flex justify-between items-center mb-1">
                      <span className="font-bold text-gray-900">{p.title}</span>
                      {p.project_url && (
                        <a href={p.project_url} target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">
                          Code &rarr;
                        </a>
                      )}
                    </div>
                    <p className="text-gray-600">{p.description}</p>
                    {p.technologies && (
                      <span className="text-2xs text-gray-400 block mt-1">Tech: {p.technologies}</span>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-gray-400">No projects recorded.</p>
            )}
          </div>

          {/* Certifications */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">
              Certifications ({profile.certifications?.length || 0})
            </h4>
            {profile.certifications && profile.certifications.length > 0 ? (
              <div className="divide-y divide-gray-100 border border-gray-200 rounded-lg overflow-hidden text-xs">
                {profile.certifications.map((c: any) => (
                  <div key={c.id} className="p-2.5 bg-white flex justify-between items-center">
                    <div>
                      <span className="font-semibold text-gray-900 block">{c.name}</span>
                      <span className="text-2xs text-gray-500">Issuer: {c.issuing_org}</span>
                    </div>
                    {c.credential_id && (
                      <span className="text-2xs font-mono text-gray-400">{c.credential_id}</span>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-gray-400">No certifications recorded.</p>
            )}
          </div>
        </div>
      ) : null}
    </Modal>
  );
};
