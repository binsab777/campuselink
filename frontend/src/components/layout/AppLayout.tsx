"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import ProtectedRoute from "@/components/ProtectedRoute";
import { StatusBadge } from "../ui/StatusBadge";
import { Button } from "../ui/Button";

export interface AppLayoutProps {
  children: React.ReactNode;
  allowedRoles?: string[];
}

export const AppLayout: React.FC<AppLayoutProps> = ({ children, allowedRoles = [] }) => {
  const { user, logout } = useAuth();
  const pathname = usePathname();

  const navLinks = [
    { href: "/dashboard", label: "Dashboard" },
    // Student links
    { href: "/dashboard/profile", label: "My Profile", roles: ["STUDENT"] },
    { href: "/dashboard/jobs", label: "Jobs & Drives", roles: ["STUDENT"] },
    { href: "/dashboard/readiness", label: "Readiness & Gaps", roles: ["STUDENT"] },
    // Recruiter link
    { href: "/dashboard/recruiter", label: "Recruiter Portal", roles: ["RECRUITER"] },
    // Placement Officer & Admin links
    { href: "/dashboard/students", label: "Student Directory", roles: ["PLACEMENT_OFFICER", "SUPER_ADMIN"] },
    { href: "/dashboard/companies", label: "Corporate Partners", roles: ["PLACEMENT_OFFICER", "SUPER_ADMIN"] },
    { href: "/dashboard/recruiter", label: "Placement Operations", roles: ["PLACEMENT_OFFICER", "SUPER_ADMIN"] },
    { href: "/dashboard/admin/skills", label: "Master Skills", roles: ["PLACEMENT_OFFICER", "SUPER_ADMIN"] },
    // Admin specific
    { href: "/dashboard/admin/users", label: "User Accounts", roles: ["SUPER_ADMIN"] },
  ];

  return (
    <ProtectedRoute allowedRoles={allowedRoles}>
      <div className="min-h-screen bg-gray-50 flex flex-col text-gray-900">
        {/* Top Navbar */}
        <header className="bg-white border-b border-gray-200 sticky top-0 z-30 shadow-xs">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16 items-center">
              {/* Brand Logo & Nav */}
              <div className="flex items-center gap-8">
                <Link href="/dashboard" className="flex items-center gap-2">
                  <span className="text-xl font-black tracking-tight text-blue-600">CAMPUS<span className="text-gray-900">LINK</span></span>
                </Link>

                <nav className="hidden md:flex items-center space-x-1">
                  {navLinks.map((link) => {
                    if (link.roles && user && !link.roles.includes(user.role)) {
                      return null;
                    }
                    const isActive = pathname === link.href;
                    return (
                      <Link
                        key={link.href}
                        href={link.href}
                        className={`px-3 py-2 rounded-md text-sm font-medium transition ${
                          isActive
                            ? "bg-blue-50 text-blue-700 font-semibold"
                            : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                        }`}
                      >
                        {link.label}
                      </Link>
                    );
                  })}
                </nav>
              </div>

              {/* User profile & Logout */}
              <div className="flex items-center gap-4">
                {user && (
                  <div className="hidden sm:flex flex-col text-right">
                    <span className="text-xs font-semibold text-gray-900">{user.email}</span>
                    <div className="mt-0.5">
                      <StatusBadge status={user.role} size="sm" />
                    </div>
                  </div>
                )}
                <Button
                  variant="outline"
                  size="sm"
                  onClick={logout}
                  className="text-xs text-rose-600 hover:text-rose-700 hover:bg-rose-50 border-rose-200"
                >
                  Logout
                </Button>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
      </div>
    </ProtectedRoute>
  );
};
