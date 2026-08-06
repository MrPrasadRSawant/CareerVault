import type { Opportunity, OpportunityStatus } from "@/api/opportunities";

export interface OpportunityFilters {
  search: string;
  statuses: OpportunityStatus[];
  company: string;
  location: string;
  experience: string;
  skills: string;
  postedFrom: string;
  postedTo: string;
}

export type OpportunityExportColumnKey =
  | "title"
  | "company_name"
  | "status"
  | "job_location"
  | "post_url"
  | "company_career_page"
  | "company_url"
  | "posted_on_utc"
  | "experience_level"
  | "required_skills"
  | "description"
  | "created_on_utc"
  | "updated_on_utc";

export interface OpportunityExportColumn {
  key: OpportunityExportColumnKey;
  label: string;
  value: (opportunity: Opportunity) => string;
}
