"use client";

import React, { forwardRef } from "react";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  hasError?: boolean;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className = "", hasError = false, disabled = false, ...props }, ref) => {
    return (
      <input
        ref={ref}
        disabled={disabled}
        className={`w-full px-3 py-2 text-sm text-gray-900 bg-white border rounded-lg transition focus:outline-none focus:ring-2 disabled:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed ${
          hasError
            ? "border-rose-500 focus:ring-rose-500 focus:border-rose-500 text-rose-900 bg-rose-50/20"
            : "border-gray-300 focus:ring-blue-500 focus:border-blue-500"
        } ${className}`}
        {...props}
      />
    );
  }
);

Input.displayName = "Input";
