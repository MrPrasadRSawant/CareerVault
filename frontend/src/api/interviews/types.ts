export interface Interview {
  id: string;
  application_id: string;
  scheduled_at: string;
  type: string;
  location_or_link: string | null;
  status: string;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface InterviewCreate {
  application_id: string;
  scheduled_at: string;
  type?: string;
  location_or_link?: string | null;
  notes?: string | null;
}
