"use client";

import React, { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { FormField } from "@/components/forms/FormField";
import { FormError } from "@/components/forms/FormError";

export default function LoginPage() {
  const [email, setEmail] = useState("student1@college.edu");
  const [password, setPassword] = useState("stu123");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const form = new URLSearchParams();
      form.append("username", email.trim());
      form.append("password", password);

      const { apiClient } = await import("@/services/apiClient");
      const data = await apiClient.post<any>("/api/v1/auth/login", {
        username: email.trim(),
        password
      });
      login(data.access_token, data.refresh_token);
    } catch (err: any) {
      setError(err?.message || "Network error: Cannot reach backend server.");
      setLoading(false);
    }
  };

  const fillCredentials = (demoEmail: string, demoPass: string) => {
    setEmail(demoEmail);
    setPassword(demoPass);
    setError("");
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 p-4">
      <div className="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border border-gray-200">
        <div className="text-center mb-6">
          <span className="text-2xl font-black tracking-tight text-blue-600">CAMPUS<span className="text-gray-900">LINK</span></span>
          <h2 className="text-xl font-bold mt-2 text-gray-800">Sign in to your account</h2>
          <p className="text-xs text-gray-500 mt-0.5">Campus placement & employability management</p>
        </div>

        <FormError error={error} className="mb-4" onDismiss={() => setError("")} />

        <form onSubmit={handleLogin} className="space-y-4">
          <FormField label="Email Address" required>
            <Input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@college.edu"
              required
            />
          </FormField>

          <FormField label="Password" required>
            <Input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </FormField>

          <Button
            type="submit"
            loading={loading}
            className="w-full py-2.5 mt-2"
          >
            Sign In
          </Button>
        </form>

        <div className="mt-6 pt-6 border-t border-gray-100">
          <p className="text-2xs font-bold uppercase tracking-wider text-gray-400 mb-2">
            Quick Demo Accounts
          </p>
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => fillCredentials("student1@college.edu", "stu123")}
              className="text-xs bg-blue-50 hover:bg-blue-100 text-blue-700 px-3 py-1.5 rounded-lg font-medium transition cursor-pointer"
            >
              Student Demo
            </button>
            <button
              type="button"
              onClick={() => fillCredentials("recruiter1@comp1.com", "rec123")}
              className="text-xs bg-purple-50 hover:bg-purple-100 text-purple-700 px-3 py-1.5 rounded-lg font-medium transition cursor-pointer"
            >
              Recruiter Demo
            </button>
            <button
              type="button"
              onClick={() => fillCredentials("admin@campuslink.com", "admin123")}
              className="text-xs bg-gray-100 hover:bg-gray-200 text-gray-800 px-3 py-1.5 rounded-lg font-medium transition cursor-pointer"
            >
              Admin Demo
            </button>
          </div>

          <div className="mt-4 text-center text-xs text-gray-500">
            <span>Don&apos;t have an account? </span>
            <a href="/register" className="font-semibold text-blue-600 hover:underline">
              Create an account
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
