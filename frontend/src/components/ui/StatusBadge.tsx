"use client";

import React from "react";

export type BadgeVariant = "info" | "success" | "warning" | "danger" | "neutral" | "purple";

export interface StatusBadgeProps {
  status: string;
  variant?: "auto" | BadgeVariant;
  size?: "sm" | "md";
  className?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  status,
  variant = "auto",
  size = "md",
  className = "",
}) => {
  const normalized = status ? status.toUpperCase().replace(/\s+/g, "_") : "";

  let resolvedVariant: BadgeVariant = "neutral";
  if (variant !== "auto") {
    resolvedVariant = variant;
  } else {
    switch (normalized) {
      case "PUBLISHED":
      case "REGISTRATION_OPEN":
      case "COMPLETED":
      case "VERIFIED":
      case "READY":
      case "ELIGIBLE":
      case "ACTIVE":
      case "EXPERT":
        resolvedVariant = "success";
        break;
      case "IN_PROGRESS":
      case "INTERMEDIATE":
      case "DEVELOPING":
      case "MEDIUM":
        resolvedVariant = "info";
        break;
      case "DRAFT":
      case "PENDING":
      case "BEGINNER":
      case "LOW":
      case "EXPLORING":
        resolvedVariant = "warning";
        break;
      case "CLOSED":
      case "CANCELLED":
      case "NOT_ELIGIBLE":
      case "REJECTED":
      case "HIGH":
      case "CRITICAL":
        resolvedVariant = "danger";
        break;
      case "ADVANCED":
      case "SUPER_ADMIN":
      case "PLACEMENT_OFFICER":
      case "RECRUITER":
        resolvedVariant = "purple";
        break;
      default:
        resolvedVariant = "neutral";
    }
  }

  const variantStyles: Record<BadgeVariant, string> = {
    success: "bg-emerald-50 text-emerald-700 border-emerald-200",
    info: "bg-blue-50 text-blue-700 border-blue-200",
    warning: "bg-amber-50 text-amber-700 border-amber-200",
    danger: "bg-rose-50 text-rose-700 border-rose-200",
    purple: "bg-purple-50 text-purple-700 border-purple-200",
    neutral: "bg-gray-100 text-gray-700 border-gray-200",
  };

  const sizeStyles = {
    sm: "px-2 py-0.5 text-xs",
    md: "px-2.5 py-1 text-xs",
  };

  const formattedLabel = status ? status.replace(/_/g, " ") : "";

  return (
    <span
      className={`inline-flex items-center font-semibold rounded-full border ${variantStyles[resolvedVariant]} ${sizeStyles[size]} ${className}`}
    >
      {formattedLabel}
    </span>
  );
};
