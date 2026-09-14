"use client";

import React from "react";
import Link from "next/link";
import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card } from "@/components/ui/Card";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { useAuth } from "@/context/AuthContext";

export default function DashboardPage() {
  const { user } = useAuth();

  return (
    <AppLayout>
      <PageHeader
        title="Command Center"
        subtitle="Access student profiles, employability intelligence, and corporate hiring workflows."
      />

      <div className="space-y-6">
        {/* Welcome card */}
        <Card className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white border-0 shadow-md">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <span className="text-xs uppercase font-bold tracking-wider text-blue-200">
                Connected Session
              </span>
              <h2 className="text-xl sm:text-2xl font-black mt-1">
                Welcome back, {user?.email}
              </h2>
              <p className="text-xs text-blue-100 mt-1 max-w-xl">
                CAMPUSLINK placement platform provides deterministic student readiness analytics, recruiter job management, and verified candidate tracking.
              </p>
            </div>
            <div className="shrink-0 bg-white/10 backdrop-blur-xs p-3 rounded-xl border border-white/20 text-right">
              <span className="text-2xs text-blue-200 uppercase font-semibold block">Active Role</span>
              <div className="mt-1">
                <StatusBadge status={user?.role || "STUDENT"} size="md" variant="purple" />
              </div>
            </div>
          </div>
        </Card>

        {/* Modules Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* STUDENT CARDS */}
          {user?.role === "STUDENT" && (
            <>
              <Link
                href="/dashboard/profile"
                className="group block p-6 bg-white border border-gray-200 rounded-xl hover:border-blue-500 hover:shadow-lg transition duration-200"
              >
                <div className="w-12 h-12 mb-4 rounded-xl bg-blue-50 flex items-center justify-center text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition">
                  <span className="text-2xl">🎓</span>
                </div>
                <h3 className="text-base font-bold text-gray-900 group-hover:text-blue-600 transition mb-1">
                  My Profile
                </h3>
                <p className="text-xs text-gray-500 leading-relaxed mb-4">
                  Comprehensive profile management for academic records, skills, capstone projects, certifications, and live profile completeness.
                </p>
                <span className="text-xs font-semibold text-blue-600 group-hover:translate-x-1 inline-flex items-center gap-1 transition-transform">
                  <span>Open Profile</span>
                  <span>&rarr;</span>
                </span>
              </Link>

              <Link
                href="/dashboard/jobs"
                className="group block p-6 bg-white border border-gray-200 rounded-xl hover:border-indigo-500 hover:shadow-lg transition duration-200"
              >
                <div className="w-12 h-12 mb-4 rounded-xl bg-indigo-50 flex items-center justify-center text-indigo-600 group-hover:bg-indigo-600 group-hover:text-white transition">
                  <span className="text-2xl">💼</span>
                </div>
                <h3 className="text-base font-bold text-gray-900 group-hover:text-indigo-600 transition mb-1">
                  Jobs & Placement Drives
                </h3>
                <p className="text-xs text-gray-500 leading-relaxed mb-4">
                  Browse published placement openings, check your real-time deterministic eligibility, and register for campus interview drives.
                </p>
                <span className="text-xs font-semibold text-indigo-600 group-hover:translate-x-1 inline-flex items-center gap-1 transition-transform">
                  <span>Browse Opportunities</span>
                  <span>&rarr;</span>
                </span>
              </Link>

              <Link
                href="/dashboard/readiness"
                className="group block p-6 bg-white border border-gray-200 rounded-xl hover:border-emerald-500 hover:shadow-lg transition duration-200"
              >
                <div className="w-12 h-12 mb-4 rounded-xl bg-emerald-50 flex items-center justify-center text-emerald-600 group-hover:bg-emerald-600 group-hover:text-white transition">
                  <span className="text-2xl">📊</span>
                </div>
                <h3 className="text-base font-bold text-gray-900 group-hover:text-emerald-600 transition mb-1">
                  Readiness & Skill Gaps
                </h3>
                <p className="text-xs text-gray-500 leading-relaxed mb-4">
                  Deterministic 7-dimension employability evaluation, dynamic weight normalization, identified strengths, and job-specific gap analysis.
                </p>
                <span className="text-xs font-semibold text-emerald-600 group-hover:translate-x-1 inline-flex items-center gap-1 transition-transform">
                  <span>Explore Readiness</span>
                  <span>&rarr;</span>
                </span>
              </Link>
            </>
          )}

          {/* RECRUITER CARDS */}
          {user?.role === "RECRUITER" && (
            <Link
              href="/dashboard/recruiter"
              className="group block p-6 bg-white border border-gray-200 rounded-xl hover:border-purple-500 hover:shadow-lg transition duration-200 md:col-span-2"
            >
              <div className="w-12 h-12 mb-4 rounded-xl bg-purple-50 flex items-center justify-center text-purple-600 group-hover:bg-purple-600 group-hover:text-white transition">
                <span className="text-2xl">💼</span>
              </div>
              <h3 className="text-base font-bold text-gray-900 group-hover:text-purple-600 transition mb-1">
                Recruiter Portal & Operations
              </h3>
              <p className="text-xs text-gray-500 leading-relaxed mb-4">
                Corporate profile management, job requisitions, skill requirements with weighted criteria, placement drives, candidate management, and bulk eligibility evaluation.
              </p>
              <span className="text-xs font-semibold text-purple-600 group-hover:translate-x-1 inline-flex items-center gap-1 transition-transform">
                <span>Open Recruiter Portal</span>
                <span>&rarr;</span>
              </span>
            </Link>
          )}

          {/* PLACEMENT OFFICER & SUPER ADMIN CARDS */}
          {(user?.role === "PLACEMENT_OFFICER" || user?.role === "SUPER_ADMIN") && (
            <>
              <Link
                href="/dashboard/students"
                className="group block p-6 bg-white border border-gray-200 rounded-xl hover:border-blue-500 hover:shadow-lg transition duration-200"
              >
                <div className="w-12 h-12 mb-4 rounded-xl bg-blue-50 flex items-center justify-center text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition">
                  <span className="text-2xl">🎓</span>
                </div>
                <h3 className="text-base font-bold text-gray-900 group-hover:text-blue-600 transition mb-1">
                  Student Directory
                </h3>
                <p className="text-xs text-gray-500 leading-relaxed mb-4">
                  Search students, filter by CGPA/department, inspect profiles, and review 7-dimension employability readiness scores.
                </p>
                <span className="text-xs font-semibold text-blue-600 group-hover:translate-x-1 inline-flex items-center gap-1 transition-transform">
                  <span>Browse Students</span>
                  <span>&rarr;</span>
                </span>
              </Link>

              <Link
                href="/dashboard/companies"
                className="group block p-6 bg-white border border-gray-200 rounded-xl hover:border-indigo-500 hover:shadow-lg transition duration-200"
              >
                <div className="w-12 h-12 mb-4 rounded-xl bg-indigo-50 flex items-center justify-center text-indigo-600 group-hover:bg-indigo-600 group-hover:text-white transition">
                  <span className="text-2xl">🏢</span>
                </div>
                <h3 className="text-base font-bold text-gray-900 group-hover:text-indigo-600 transition mb-1">
                  Corporate Partners
                </h3>
                <p className="text-xs text-gray-500 leading-relaxed mb-4">
                  Manage registered employers, company profiles, designated talent acquisition contacts, and active requisitions.
                </p>
                <span className="text-xs font-semibold text-indigo-600 group-hover:translate-x-1 inline-flex items-center gap-1 transition-transform">
                  <span>View Partners</span>
                  <span>&rarr;</span>
                </span>
              </Link>

              <Link
                href="/dashboard/recruiter"
                className="group block p-6 bg-white border border-gray-200 rounded-xl hover:border-purple-500 hover:shadow-lg transition duration-200"
              >
                <div className="w-12 h-12 mb-4 rounded-xl bg-purple-50 flex items-center justify-center text-purple-600 group-hover:bg-purple-600 group-hover:text-white transition">
                  <span className="text-2xl">💼</span>
                </div>
                <h3 className="text-base font-bold text-gray-900 group-hover:text-purple-600 transition mb-1">
                  Placement Operations
                </h3>
                <p className="text-xs text-gray-500 leading-relaxed mb-4">
                  Supervise campus hiring events, schedule placement drives, inspect job requirements, and run eligibility sandboxes.
                </p>
                <span className="text-xs font-semibold text-purple-600 group-hover:translate-x-1 inline-flex items-center gap-1 transition-transform">
                  <span>Open Operations</span>
                  <span>&rarr;</span>
                </span>
              </Link>

              <Link
                href="/dashboard/admin/skills"
                className="group block p-6 bg-white border border-gray-200 rounded-xl hover:border-emerald-500 hover:shadow-lg transition duration-200"
              >
                <div className="w-12 h-12 mb-4 rounded-xl bg-emerald-50 flex items-center justify-center text-emerald-600 group-hover:bg-emerald-600 group-hover:text-white transition">
                  <span className="text-2xl">🗂️</span>
                </div>
                <h3 className="text-base font-bold text-gray-900 group-hover:text-emerald-600 transition mb-1">
                  Master Skills Catalog
                </h3>
                <p className="text-xs text-gray-500 leading-relaxed mb-4">
                  Standardized canonical skills taxonomy ensuring clean match data across students and job requisitions.
                </p>
                <span className="text-xs font-semibold text-emerald-600 group-hover:translate-x-1 inline-flex items-center gap-1 transition-transform">
                  <span>Manage Catalog</span>
                  <span>&rarr;</span>
                </span>
              </Link>

              {user?.role === "SUPER_ADMIN" && (
                <Link
                  href="/dashboard/admin/users"
                  className="group block p-6 bg-white border border-gray-200 rounded-xl hover:border-amber-500 hover:shadow-lg transition duration-200"
                >
                  <div className="w-12 h-12 mb-4 rounded-xl bg-amber-50 flex items-center justify-center text-amber-600 group-hover:bg-amber-600 group-hover:text-white transition">
                    <span className="text-2xl">🛡️</span>
                  </div>
                  <h3 className="text-base font-bold text-gray-900 group-hover:text-amber-600 transition mb-1">
                    User Accounts & RBAC
                  </h3>
                  <p className="text-xs text-gray-500 leading-relaxed mb-4">
                    Inspect registered user accounts, assign system roles, and activate or deactivate platform access.
                  </p>
                  <span className="text-xs font-semibold text-amber-600 group-hover:translate-x-1 inline-flex items-center gap-1 transition-transform">
                    <span>Manage Users</span>
                    <span>&rarr;</span>
                  </span>
                </Link>
              )}
            </>
          )}
        </div>
      </div>
    </AppLayout>
  );
}
