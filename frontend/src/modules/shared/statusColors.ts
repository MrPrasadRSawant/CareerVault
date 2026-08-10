import type { ApplicationStatus } from "@/api/applications";
import type { OpportunityStatus } from "@/api/opportunities";

export const OPPORTUNITY_STATUS_ORDER: OpportunityStatus[] = [
  "draft",
  "saved",
  "applied",
  "interviewing",
  "offered",
  "follow_up",
  "interview_scheduled",
  "interview_completed",
  "offer",
  "rejected",
  "not_replied",
  "on_hold",
  "archived",
  "not_satisfying_expectations"
];

export const OPPORTUNITY_STATUS_LABELS: Record<OpportunityStatus, string> = {
  draft: "Draft",
  saved: "Saved",
  applied: "Applied",
  interviewing: "Interviewing",
  offered: "Offered",
  follow_up: "Follow-up",
  interview_scheduled: "Interview scheduled",
  interview_completed: "Interview completed",
  offer: "Offer",
  rejected: "Rejected",
  not_replied: "Not replied",
  on_hold: "On hold",
  archived: "Archived",
  not_satisfying_expectations: "Not satisfying expectations"
};

export const OPPORTUNITY_STATUS_COLORS: Record<OpportunityStatus, string> = {
  draft: "var(--cv-status-draft)",
  saved: "var(--cv-status-applied-soft)",
  applied: "var(--cv-status-applied)",
  interviewing: "var(--cv-status-interview)",
  offered: "var(--cv-status-offer)",
  follow_up: "var(--cv-amber)",
  interview_scheduled: "var(--cv-status-interview)",
  interview_completed: "var(--cv-status-interview-complete)",
  offer: "var(--cv-status-offer)",
  rejected: "var(--cv-status-interview-complete)",
  not_replied: "var(--cv-status-closed)",
  on_hold: "var(--cv-status-closed)",
  archived: "var(--cv-status-closed)",
  not_satisfying_expectations: "var(--cv-status-warning)"
};

export const APPLICATION_STATUS_ORDER: ApplicationStatus[] = [
  "applied",
  "screening",
  "interview_scheduled",
  "interview_completed",
  "offer",
  "rejected",
  "withdrawn"
];

export const APPLICATION_STATUS_LABELS: Record<ApplicationStatus, string> = {
  applied: "Applied",
  screening: "Screening",
  interview_scheduled: "Interview scheduled",
  interview_completed: "Interview completed",
  offer: "Offer",
  rejected: "Rejected",
  withdrawn: "Withdrawn"
};

export const APPLICATION_STATUS_COLORS: Record<ApplicationStatus, string> = {
  applied: "var(--cv-status-applied-soft)",
  screening: "var(--cv-status-applied)",
  interview_scheduled: "var(--cv-status-interview)",
  interview_completed: "var(--cv-status-interview-complete)",
  offer: "var(--cv-status-offer)",
  rejected: "var(--cv-status-interview-complete)",
  withdrawn: "var(--cv-status-closed)"
};
