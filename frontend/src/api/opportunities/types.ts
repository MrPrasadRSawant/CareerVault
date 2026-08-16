export type OpportunityStatus =
  | "draft"
  | "saved"
  | "applied"
  | "interviewing"
  | "offered"
  | "follow_up"
  | "interview_scheduled"
  | "interview_completed"
  | "offer"
  | "rejected"
  | "not_replied"
  | "on_hold"
  | "archived"
  | "not_satisfying_expectations";

export interface Opportunity {
  id: string;
  company_name: string | null;
  post_url: string | null;
  company_career_page: string | null;
  company_url: string | null;
  posted_on_utc: string | null;
  job_location: string | null;
  title: string;
  description: string | null;
  required_skills: string[] | null;
  experience_level: string | null;
  status: OpportunityStatus;
  is_deleted: boolean;
  created_by: string;
  created_on_utc: string;
  updated_by: string;
  updated_on_utc: string;
}

export interface OpportunityCreate {
  title: string;
  company_name?: string | null;
  post_url?: string | null;
  company_career_page?: string | null;
  company_url?: string | null;
  posted_on_utc?: string | null;
  job_location?: string | null;
  description?: string | null;
  required_skills?: string[] | null;
  experience_level?: string | null;
  status?: OpportunityStatus;
}
