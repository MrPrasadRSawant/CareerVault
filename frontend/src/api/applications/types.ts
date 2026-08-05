export type ApplicationStatus =
  | "applied"
  | "screening"
  | "interview_scheduled"
  | "interview_completed"
  | "offer"
  | "rejected"
  | "withdrawn";

export interface Application {
  id: string;
  opportunity_id: string;
  resume_id: string | null;
  cover_letter_id: string | null;
  status: ApplicationStatus;
  applied_date: string | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface ApplicationCreate {
  opportunity_id: string;
  resume_id?: number | null;
  cover_letter_id?: number | null;
  status?: ApplicationStatus;
  applied_date?: string | null;
  notes?: string | null;
}

export interface StatusHistoryEntry {
  id: string;
  application_id: string;
  status: ApplicationStatus;
  note: string | null;
  changed_at: string;
}
