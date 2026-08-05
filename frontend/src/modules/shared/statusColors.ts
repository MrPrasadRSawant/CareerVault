import type { ApplicationStatus } from "@/api/applications";
import type { OpportunityStatus } from "@/api/opportunities";

export const OPPORTUNITY_STATUS_ORDER: OpportunityStatus[] = [
  "saved",
  "applied",
  "interviewing",
  "offered",
  "rejected",
  "archived"
];

export const OPPORTUNITY_STATUS_LABELS: Record<OpportunityStatus, string> = {
  saved: "Saved",
  applied: "Applied",
  interviewing: "Interviewing",
  offered: "Offered",
  rejected: "Rejected",
  archived: "Archived"
};

export const OPPORTUNITY_STATUS_COLORS: Record<OpportunityStatus, string> = {
  saved: "#8ECAE6",
  applied: "#219EBC",
  interviewing: "#FFB703",
  offered: "#2A9D8F",
  rejected: "#FB8500",
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
