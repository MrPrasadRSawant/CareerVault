import type { ApplicationStatus } from "@/api/applications";
import type { Resume } from "@/api/resumes";

export type ResumeTabKey = "all" | "active" | "attached" | "unattached";
export type ResumeAttachmentFilter = "all" | "attached" | "unattached";

export interface LinkedApplicationSummary {
  id: string;
  status: ApplicationStatus;
  opportunityTitle: string;
}

export interface ResumeRow extends Resume {
  linkedApplications: LinkedApplicationSummary[];
}

export interface ResumeFilters {
  search: string;
  fileType: string;
  attachment: ResumeAttachmentFilter;
  uploadedFrom: string;
  uploadedTo: string;
}

export type ResumeExportColumnKey = "name" | "version" | "file_type" | "file_size" | "applications" | "is_active" | "created_at";
