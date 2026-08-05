export type OpportunityStatus =
  | "saved"
  | "applied"
  | "interviewing"
  | "offered"
  | "rejected"
  | "archived";

export interface Opportunity {
  id: string;
  company_id: string | null;
  title: string;
  description: string | null;
  application_link: string | null;
  salary_range: string | null;
  required_skills: string[] | null;
  experience_level: string | null;
  status: OpportunityStatus;
  source: string | null;
  posted_date: string | null;
  deadline: string | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface OpportunityCreate {
  title: string;
  company_id?: number | null;
  description?: string | null;
  application_link?: string | null;
  salary_range?: string | null;
  required_skills?: string[] | null;
  experience_level?: string | null;
  status?: OpportunityStatus;
  source?: string | null;
  posted_date?: string | null;
  deadline?: string | null;
  notes?: string | null;
}
