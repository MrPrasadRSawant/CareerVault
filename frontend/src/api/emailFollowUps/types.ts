import type { ApplicationStatus } from "@/api/applications";

export type EmailFollowUpOutcome = "pending" | "won" | "lost";

export interface EmailFollowUp {
  id: string;
  application_id: string;
  external_message_id: string | null;
  thread_id: string | null;
  subject: string;
  sender_email: string;
  sender_name: string | null;
  recipient_emails: string[] | null;
  received_at: string;
  body_text: string | null;
  outcome: EmailFollowUpOutcome;
  reason: string | null;
  reason_category: string | null;
  ai_confidence: number | null;
  raw_metadata: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
}

export interface EmailFollowUpGroup {
  application_id: string;
  opportunity_title: string;
  company_name: string | null;
  application_status: ApplicationStatus;
  applied_date: string | null;
  latest_received_at: string;
  latest_outcome: EmailFollowUpOutcome;
  email_count: number;
  emails: EmailFollowUp[];
}

export interface EmailFollowUpPayload {
  application_id: string;
  external_message_id?: string | null;
  thread_id?: string | null;
  subject: string;
  sender_email: string;
  sender_name?: string | null;
  recipient_emails?: string[] | null;
  received_at: string;
  body_text?: string | null;
  outcome?: EmailFollowUpOutcome;
  reason?: string | null;
  reason_category?: string | null;
  ai_confidence?: number | null;
  raw_metadata?: Record<string, unknown> | null;
}
