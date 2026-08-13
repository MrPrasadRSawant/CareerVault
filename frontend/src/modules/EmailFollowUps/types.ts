import type { EmailFollowUpOutcome } from "@/api/emailFollowUps";

export interface ApplicationChoice {
  applicationId: string;
  label: string;
}

export interface EmailFollowUpFilters {
  search: string;
  outcome: EmailFollowUpOutcome | "all";
}
