import type { Application, ApplicationStatus } from "@/api/applications";
import type { Opportunity } from "@/api/opportunities";
import type { Resume } from "@/api/resumes";

export type ApplicationTabKey =
  | "all"
  | "active"
  | "applied"
  | "interviews"
  | "offer"
  | "closed";
export type FilterPresence = "any" | "yes" | "no";

export interface ApplicationRow extends Application {
  opportunity: Opportunity | null;
  resume: Resume | null;
}

export interface ApplicationFilters {
  search: string;
  statuses: ApplicationStatus[];
  company: string;
  location: string;
  notes: string;
  appliedFrom: string;
  appliedTo: string;
  hasResume: FilterPresence;
  hasCoverLetter: FilterPresence;
}

export type ApplicationExportColumnKey =
  | "opportunity"
  | "company"
  | "status"
  | "applied_date"
  | "location"
  | "notes"
  | "resume"
  | "cover_letter"
  | "created_at";
