import type { ApplicationStatus } from "@/api/applications";
import type {
  ApplicationExportColumnKey,
  ApplicationFilters,
  ApplicationRow,
  ApplicationTabKey
} from "./types";
import {
  APPLICATION_STATUS_LABELS,
  APPLICATION_STATUS_ORDER
} from "@/modules/shared/statusColors";

export const applicationStatusOptions = APPLICATION_STATUS_ORDER.map(value => ({
  label: APPLICATION_STATUS_LABELS[value],
  value
}));

export const applicationTabs: Array<{ key: ApplicationTabKey; label: string }> =
  [
    { key: "all", label: "All" },
    { key: "active", label: "Active" },
    { key: "applied", label: "Applied" },
    { key: "interviews", label: "Interviews" },
    { key: "offer", label: "Offers" },
    { key: "closed", label: "Closed" }
  ];

export const applicationExportColumns: Array<{
  key: ApplicationExportColumnKey;
  label: string;
}> = [
  { key: "opportunity", label: "Opportunity" },
  { key: "company", label: "Company" },
  { key: "status", label: "Status" },
  { key: "applied_date", label: "Applied date" },
  { key: "location", label: "Location" },
  { key: "notes", label: "Notes" },
  { key: "resume", label: "Resume attached" },
  { key: "cover_letter", label: "Cover letter attached" },
  { key: "created_at", label: "Created" }
];

export function defaultApplicationFilters(): ApplicationFilters {
  return {
    search: "",
    statuses: [],
    company: "",
    location: "",
    notes: "",
    appliedFrom: "",
    appliedTo: "",
    hasResume: "any",
    hasCoverLetter: "any"
  };
}

export function tabMatches(
  status: ApplicationStatus,
  tab: ApplicationTabKey
): boolean {
  if (tab === "all") return true;
  if (tab === "active")
    return [
      "applied",
      "screening",
      "interview_scheduled",
      "interview_completed",
      "offer"
    ].includes(status);
  if (tab === "applied") return status === "applied";
  if (tab === "interviews")
    return ["interview_scheduled", "interview_completed"].includes(status);
  if (tab === "offer") return status === "offer";
  return ["rejected", "withdrawn"].includes(status);
}

export function applicationStatusLabel(status: ApplicationStatus): string {
  return APPLICATION_STATUS_LABELS[status] ?? status;
}

export function csvCell(value: unknown): string {
  const text =
    value === null || value === undefined
      ? ""
      : typeof value === "string"
        ? value
        : typeof value === "number" || typeof value === "boolean"
          ? String(value)
          : "";
  return /[",\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

export function applicationExportValue(
  row: ApplicationRow,
  key: ApplicationExportColumnKey
): string {
  switch (key) {
    case "opportunity":
      return row.opportunity?.title ?? "Unknown opportunity";
    case "company":
      return row.opportunity?.company_name ?? "";
    case "status":
      return applicationStatusLabel(row.status);
    case "applied_date":
      return row.applied_date ?? "";
    case "location":
      return row.opportunity?.job_location ?? "";
    case "notes":
      return row.notes ?? "";
    case "resume":
      return row.resume_id ? "Yes" : "No";
    case "cover_letter":
      return row.cover_letter_id ? "Yes" : "No";
    case "created_at":
      return row.created_at;
  }
}
