import { api } from "@/api/client";
import type { User } from "@/api/auth";
import type {
  AdminAuthSession,
  AdminAuthSessionPage,
  AdminAuthSessionQuery,
  AdminExceptionLog,
  AdminExceptionLogDetail,
  AdminExceptionLogPage,
  AdminExceptionLogQuery,
  AdminExceptionOverview,
  AdminLoginEvent,
  AdminLoginEventPage,
  AdminLoginEventQuery,
  AdminOverview,
  AdminRegistrationPeriod,
  AdminSecurityOverview,
  AdminUser,
  AdminUserPage,
  AdminUserQuery,
  AuthFailureReason,
  AuthOutcome,
  AuthSessionStatus,
  LoginSecuritySettings,
  PasswordPolicySettings,
  RegistrationSettings
} from "./types";

export type {
  AdminOverview,
  AdminSecurityOverview,
  AdminLoginEvent,
  AdminLoginEventPage,
  AdminLoginEventQuery,
  AdminAuthSession,
  AdminAuthSessionPage,
  AdminAuthSessionQuery,
  AdminExceptionLog,
  AdminExceptionLogDetail,
  AdminExceptionLogPage,
  AdminExceptionLogQuery,
  AdminExceptionOverview,
  AdminRegistrationPeriod,
  AdminUser,
  AdminUserPage,
  AdminUserQuery,
  AuthFailureReason,
  AuthOutcome,
  AuthSessionStatus,
  LoginSecuritySettings,
  PasswordPolicySettings,
  RegistrationSettings
};

export const adminApi = {
  me(): Promise<User> {
    return api.get("/admin/auth/me").then(r => r.data);
  },

  overview(): Promise<AdminOverview> {
    return api.get("/admin/overview").then(r => r.data);
  },

  securityOverview(): Promise<AdminSecurityOverview> {
    return api.get("/admin/security/overview").then(r => r.data);
  },

  loginEvents(query: AdminLoginEventQuery): Promise<AdminLoginEventPage> {
    return api
      .get("/admin/security/login-events", { params: query })
      .then(r => r.data);
  },

  authSessions(query: AdminAuthSessionQuery): Promise<AdminAuthSessionPage> {
    return api
      .get("/admin/security/sessions", { params: query })
      .then(r => r.data);
  },

  exceptionOverview(): Promise<AdminExceptionOverview> {
    return api.get("/admin/exceptions/overview").then(r => r.data);
  },

  exceptionLogs(query: AdminExceptionLogQuery): Promise<AdminExceptionLogPage> {
    return api.get("/admin/exceptions", { params: query }).then(r => r.data);
  },

  exceptionLog(exceptionId: string): Promise<AdminExceptionLogDetail> {
    return api.get(`/admin/exceptions/${exceptionId}`).then(r => r.data);
  },

  registrationSettings(): Promise<RegistrationSettings> {
    return api.get("/admin/settings/registration").then(r => r.data);
  },

  updateRegistrationSettings(
    dailyRegistrationLimit: number
  ): Promise<RegistrationSettings> {
    return api
      .patch("/admin/settings/registration", {
        daily_registration_limit: dailyRegistrationLimit
      })
      .then(r => r.data);
  },

  loginSecuritySettings(): Promise<LoginSecuritySettings> {
    return api.get("/admin/settings/login-security").then(r => r.data);
  },

  updateLoginSecuritySettings(
    failedLoginAttemptLimit: number,
    lockoutDurationMinutes: number
  ): Promise<LoginSecuritySettings> {
    return api
      .patch("/admin/settings/login-security", {
        failed_login_attempt_limit: failedLoginAttemptLimit,
        lockout_duration_minutes: lockoutDurationMinutes
      })
      .then(r => r.data);
  },

  passwordPolicySettings(): Promise<PasswordPolicySettings> {
    return api.get("/admin/settings/password-policy").then(r => r.data);
  },

  updatePasswordPolicySettings(
    minimumLength: number,
    maximumLength: number
  ): Promise<PasswordPolicySettings> {
    return api
      .patch("/admin/settings/password-policy", {
        minimum_length: minimumLength,
        maximum_length: maximumLength
      })
      .then(r => r.data);
  },

  users(query: AdminUserQuery): Promise<AdminUserPage> {
    return api.get("/admin/users", { params: query }).then(r => r.data);
  },

  user(userId: string): Promise<AdminUser> {
    return api.get(`/admin/users/${userId}`).then(r => r.data);
  },

  setUserActive(userId: string, isActive: boolean): Promise<AdminUser> {
    return api
      .patch(`/admin/users/${userId}/status`, { is_active: isActive })
      .then(r => r.data);
  }
};
