"use client";

import React, { useEffect, useState, useCallback } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { Modal } from "@/components/ui/Modal";
import { Select } from "@/components/ui/Select";
import { FormField } from "@/components/forms/FormField";
import { LoadingState } from "@/components/feedback/LoadingState";
import { ErrorState } from "@/components/feedback/ErrorState";
import { EmptyState } from "@/components/feedback/EmptyState";
import { Toast } from "@/components/feedback/Toast";
import { adminApi, AdminUserItem } from "@/services/adminApi";
import { useAuth } from "@/context/AuthContext";
import { parseApiError } from "@/services/apiClient";

export default function AdminUsersPage() {
  const { user: currentUser } = useAuth();
  const [users, setUsers] = useState<AdminUserItem[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  // Filters
  const [searchQuery, setSearchQuery] = useState("");
  const [roleFilter, setRoleFilter] = useState("ALL");

  // Role Edit Modal
  const [editingUser, setEditingUser] = useState<AdminUserItem | null>(null);
  const [newRole, setNewRole] = useState<string>("STUDENT");
  const [savingRole, setSavingRole] = useState(false);

  // Status toggle loading state
  const [togglingId, setTogglingId] = useState<number | null>(null);

  const fetchUsers = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const res = await adminApi.getUsers({
        query: searchQuery.trim() || undefined,
        role: roleFilter !== "ALL" ? roleFilter : undefined,
        limit: 100,
      });
      setUsers(res.users);
      setTotal(res.total);
    } catch (err: any) {
      setError(parseApiError(err).message);
    } finally {
      setLoading(false);
    }
  }, [searchQuery, roleFilter]);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  const handleToggleStatus = async (userItem: AdminUserItem) => {
    setTogglingId(userItem.id);
    try {
      const newStatus = !userItem.is_active;
      await adminApi.updateUserStatus(userItem.id, newStatus);
      setToastMessage(`Account for ${userItem.email} has been ${newStatus ? "activated" : "deactivated"}.`);
      setUsers((prev) =>
        prev.map((u) => (u.id === userItem.id ? { ...u, is_active: newStatus } : u))
      );
    } catch (err: any) {
      setToastMessage(parseApiError(err).message);
    } finally {
      setTogglingId(null);
    }
  };

  const handleSaveRole = async () => {
    if (!editingUser) return;
    setSavingRole(true);
    try {
      await adminApi.updateUserRole(editingUser.id, newRole);
      setToastMessage(`Role for ${editingUser.email} updated to ${newRole}.`);
      setUsers((prev) =>
        prev.map((u) => (u.id === editingUser.id ? { ...u, role: newRole as any } : u))
      );
      setEditingUser(null);
    } catch (err: any) {
      setToastMessage(parseApiError(err).message);
    } finally {
      setSavingRole(false);
    }
  };

  const isSuperAdmin = currentUser?.role === "SUPER_ADMIN";

  return (
    <AppLayout allowedRoles={["SUPER_ADMIN", "PLACEMENT_OFFICER"]}>
      <PageHeader
        title="User Accounts & Access Control"
        subtitle="Authorize system access, inspect role distribution, and manage account activation."
        backHref="/dashboard"
        backLabel="Back to Dashboard"
      />

      <Toast message={toastMessage} onDismiss={() => setToastMessage(null)} />

      {/* Role Change Modal */}
      {editingUser && (
        <Modal
          isOpen={true}
          onClose={() => setEditingUser(null)}
          title="Modify Account Role"
          subtitle={`Account: ${editingUser.email}`}
          footer={
            <div className="flex justify-end gap-2">
              <Button variant="outline" size="sm" onClick={() => setEditingUser(null)}>
                Cancel
              </Button>
              <Button
                variant="primary"
                size="sm"
                onClick={handleSaveRole}
                loading={savingRole}
              >
                Save Role
              </Button>
            </div>
          }
        >
          <div className="space-y-4">
            <FormField
              label="Assigned System Role"
              helperText="Changing a user's role alters their permissions immediately on their next authentication."
            >
              <Select
                value={newRole}
                onChange={(e) => setNewRole(e.target.value)}
                options={[
                  { value: "STUDENT", label: "STUDENT (Campus Candidate)" },
                  { value: "RECRUITER", label: "RECRUITER (Corporate Hiring Team)" },
                  { value: "PLACEMENT_OFFICER", label: "PLACEMENT_OFFICER (College Placement Team)" },
                  { value: "SUPER_ADMIN", label: "SUPER_ADMIN (System Administrator)" },
                  { value: "MENTOR", label: "MENTOR (Academic Advisor)" },
                ]}
              />
            </FormField>
          </div>
        </Modal>
      )}

      {/* Filters Bar */}
      <Card className="mb-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex-1 max-w-md">
            <input
              type="text"
              placeholder="Search by email..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-3.5 py-2 text-xs rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-gray-500">Role:</span>
            <select
              value={roleFilter}
              onChange={(e) => setRoleFilter(e.target.value)}
              className="px-3 py-1.5 text-xs rounded-lg border border-gray-300 bg-white font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="ALL">All Roles</option>
              <option value="STUDENT">Students</option>
              <option value="RECRUITER">Recruiters</option>
              <option value="PLACEMENT_OFFICER">Placement Officers</option>
              <option value="SUPER_ADMIN">Super Admins</option>
            </select>
          </div>
        </div>
      </Card>

      {/* Main Content Table */}
      {loading ? (
        <LoadingState message="Loading registered users..." />
      ) : error ? (
        <ErrorState message={error} onRetry={fetchUsers} />
      ) : users.length === 0 ? (
        <EmptyState
          title="No users match the search criteria"
          description="Try broadening your search term or selecting a different role filter."
        />
      ) : (
        <Card padding="none">
          <div className="p-4 border-b border-gray-200 flex justify-between items-center bg-gray-50/50">
            <span className="text-xs font-bold text-gray-700">
              Total Accounts: <span className="text-blue-600">{total}</span>
            </span>
            <span className="text-2xs text-gray-400 font-medium">
              Role permissions strictly enforced via backend JWT RBAC
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-200 text-gray-600 font-semibold uppercase text-2xs tracking-wider">
                  <th className="p-3.5">User / Account</th>
                  <th className="p-3.5">Role</th>
                  <th className="p-3.5">Status</th>
                  <th className="p-3.5">Linked Profile</th>
                  <th className="p-3.5">Registered</th>
                  <th className="p-3.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-gray-50/70 transition-colors">
                    <td className="p-3.5">
                      <div className="font-bold text-gray-900">{u.email}</div>
                      <div className="text-2xs text-gray-400 font-mono">UID #{u.id}</div>
                    </td>
                    <td className="p-3.5">
                      <StatusBadge status={u.role} size="sm" />
                    </td>
                    <td className="p-3.5">
                      {u.is_active ? (
                        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-2xs font-bold bg-emerald-100 text-emerald-800">
                          Active
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-2xs font-bold bg-rose-100 text-rose-800">
                          Deactivated
                        </span>
                      )}
                    </td>
                    <td className="p-3.5">
                      {u.student_profile ? (
                        <div>
                          <span className="font-semibold text-gray-800">
                            {u.student_profile.first_name} {u.student_profile.last_name}
                          </span>
                          <span className="text-2xs text-blue-600 block">
                            {u.student_profile.student_identifier} • {u.student_profile.branch}
                          </span>
                        </div>
                      ) : u.recruiter_profile ? (
                        <div>
                          <span className="font-semibold text-gray-800">
                            {u.recruiter_profile.company_name || "Company Assigned"}
                          </span>
                          <span className="text-2xs text-purple-600 block">
                            Recruiter Profile #{u.recruiter_profile.id}
                          </span>
                        </div>
                      ) : (
                        <span className="text-gray-400">—</span>
                      )}
                    </td>
                    <td className="p-3.5 text-gray-500">
                      {u.created_at ? new Date(u.created_at).toLocaleDateString() : "—"}
                    </td>
                    <td className="p-3.5 text-right">
                      <div className="flex items-center justify-end gap-2">
                        {isSuperAdmin && (
                          <Button
                            variant="outline"
                            size="sm"
                            className="text-2xs h-7 px-2"
                            onClick={() => {
                              setEditingUser(u);
                              setNewRole(u.role);
                            }}
                          >
                            Role
                          </Button>
                        )}
                        <Button
                          variant="outline"
                          size="sm"
                          className={`text-2xs h-7 px-2 ${
                            u.is_active
                              ? "text-rose-600 hover:text-rose-700 hover:bg-rose-50 border-rose-200"
                              : "text-emerald-600 hover:text-emerald-700 hover:bg-emerald-50 border-emerald-200"
                          }`}
                          loading={togglingId === u.id}
                          onClick={() => handleToggleStatus(u)}
                          disabled={u.id === currentUser?.id}
                        >
                          {u.is_active ? "Deactivate" : "Activate"}
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}
    </AppLayout>
  );
}
