import type { UserRole } from "@/api/auth";

export interface AdminUser {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface AdminUserPage {
  items: AdminUser[];
  total: number;
  limit: number;
  offset: number;
}

export interface AdminOverview {
  total_users: number;
  active_users: number;
  blocked_users: number;
  registrations_today: number;
  new_users_last_7_days: number;
  new_users_last_30_days: number;
  role_counts: AdminRoleCount[];
  registrations_by_day: AdminRegistrationPeriod[];
  registrations_by_month: AdminRegistrationPeriod[];
  registrations_by_year: AdminRegistrationPeriod[];
  recent_users: AdminUser[];
}

export interface AdminRoleCount {
  role: UserRole;
  count: number;
}

export interface AdminRegistrationPeriod {
  period: string;
  role_counts: AdminRoleCount[];
}

export interface AdminUserQuery {
  search?: string;
  is_active?: boolean;
  role?: UserRole;
  limit?: number;
  offset?: number;
}

export type AuthEventType = "login" | "registration";
export type AuthOutcome = "success" | "failure";
export type AuthFailureReason =
  | "invalid_credentials"
  | "account_blocked"
  | "temporarily_locked"
  | "role_not_allowed";
export type AuthSessionStatus = "active" | "ended" | "expired";

export interface AdminSecurityOverview {
  successful_logins_last_24_hours: number;
  failed_logins_last_24_hours: number;
  active_sessions: number;
  retention_days: number;
}

export interface AdminLoginEvent {
  id: string;
  user_id: string | null;
  user_name: string | null;
  user_email: string | null;
  role: UserRole | null;
  account_known: boolean;
  unknown_account_reference: string | null;
  event_type: AuthEventType;
  outcome: AuthOutcome;
  failure_reason: AuthFailureReason | null;
  occurred_at: string;
  ip_address: string | null;
  user_agent: string | null;
  http_status: number;
}

export interface AdminLoginEventPage {
  items: AdminLoginEvent[];
  total: number;
  limit: number;
  offset: number;
}

export interface AdminLoginEventQuery {
  search?: string;
  outcome?: AuthOutcome;
  role?: UserRole;
  limit?: number;
  offset?: number;
}

export interface AdminAuthSession {
  user_id: string;
  user_name: string;
  user_email: string;
  role: UserRole;
  auth_method: AuthEventType;
  started_at: string;
  last_seen_at: string;
  ended_at: string | null;
  expires_at: string;
  status: AuthSessionStatus;
  duration_seconds: number;
  duration_basis: "ongoing" | "exact" | "estimated_last_activity";
  end_reason: "logout" | "account_blocked" | null;
  ip_address: string | null;
  user_agent: string | null;
}

export interface AdminAuthSessionPage {
  items: AdminAuthSession[];
  total: number;
  limit: number;
  offset: number;
}

export interface AdminAuthSessionQuery {
  search?: string;
  role?: UserRole;
  limit?: number;
  offset?: number;
}

export interface RegistrationSettings {
  daily_registration_limit: number;
  registrations_used_today: number;
  registrations_remaining_today: number;
  counter_date_utc: string;
  updated_at: string;
}

export interface LoginSecuritySettings {
  failed_login_attempt_limit: number;
  lockout_duration_minutes: number;
  updated_at: string;
}

export interface PasswordPolicySettings {
  minimum_length: number;
  maximum_length: number;
  updated_at: string;
}

export interface AdminExceptionOverview {
  exceptions_last_24_hours: number;
  exceptions_last_7_days: number;
  unique_fingerprints_last_24_hours: number;
  retention_days: number;
}

export interface AdminExceptionLog {
  id: string;
  request_id: string;
  user_id: string | null;
  user_name: string | null;
  user_email: string | null;
  occurred_at: string;
  method: string;
  route_template: string;
  query_parameter_names: string[];
  status_code: number;
  exception_type: string;
  message: string;
  fingerprint: string;
  ip_address: string | null;
  user_agent: string | null;
  app_environment: string;
  is_handled: boolean;
}

export interface AdminExceptionLogDetail extends AdminExceptionLog {
  traceback: string;
}

export interface AdminExceptionLogPage {
  items: AdminExceptionLog[];
  total: number;
  limit: number;
  offset: number;
}

export interface AdminExceptionLogQuery {
  search?: string;
  status_code?: number;
  limit?: number;
  offset?: number;
}
