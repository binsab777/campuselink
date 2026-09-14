"use client";

import React, { forwardRef } from "react";

export interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "type"> {
  label?: React.ReactNode;
  description?: string;
  hasError?: boolean;
}

export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  ({ className = "", label, description, hasError = false, disabled = false, id, ...props }, ref) => {
    const inputId = id || (typeof label === "string" ? label.toLowerCase().replace(/\s+/g, "-") : undefined);

    return (
      <div className="flex items-start">
        <div className="flex items-center h-5">
          <input
            id={inputId}
            ref={ref}
            type="checkbox"
            disabled={disabled}
            className={`w-4 h-4 rounded text-blue-600 focus:ring-blue-500 transition cursor-pointer disabled:cursor-not-allowed ${
              hasError ? "border-rose-500" : "border-gray-300"
            } ${className}`}
            {...props}
          />
        </div>
        {(label || description) && (
          <div className="ml-2.5 text-sm">
            {label && (
              <label htmlFor={inputId} className={`font-medium cursor-pointer ${disabled ? "text-gray-400" : "text-gray-700"}`}>
                {label}
              </label>
            )}
            {description && <p className="text-xs text-gray-500">{description}</p>}
          </div>
        )}
      </div>
    );
  }
);

Checkbox.displayName = "Checkbox";
