export interface FollowUp {
  id: string;
  application_id: string;
  scheduled_at: string;
  subject: string | null;
  message: string | null;
  status: string;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface FollowUpCreate {
  application_id: string;
  scheduled_at: string;
  subject?: string | null;
  message?: string | null;
}
