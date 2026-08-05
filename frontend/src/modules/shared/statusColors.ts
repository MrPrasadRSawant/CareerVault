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
  "archived"
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
  archived: "Archived"
};

export const OPPORTUNITY_STATUS_COLORS: Record<OpportunityStatus, string> = {
  draft: "#94A3B8",
  saved: "#8ECAE6",
  applied: "#219EBC",
  interviewing: "#FFB703",
  offered: "#2A9D8F",
  follow_up: "#D99A2B",
  interview_scheduled: "#FFB703",
  interview_completed: "#FB8500",
  offer: "#2A9D8F",
  rejected: "#FB8500",
  not_replied: "#64748B",
  on_hold: "#64748B",
  archived: "#64748B"
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
  applied: "#8ECAE6",
  screening: "#219EBC",
  interview_scheduled: "#FFB703",
  interview_completed: "#FB8500",
  offer: "#2A9D8F",
  rejected: "#FB8500",
  withdrawn: "#64748B"
};
