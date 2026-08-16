import type { Resume } from "@/api/resumes";
import type {
  ResumeExportColumnKey,
  ResumeFilters,
  ResumeRow,
  ResumeTabKey
} from "./types";

export const resumeTabs: Array<{ key: ResumeTabKey; label: string }> = [
  { key: "all", label: "All" },
  { key: "active", label: "Active" },
  { key: "attached", label: "Attached" },
  { key: "unattached", label: "Unattached" }
];

export const resumeExportColumns: Array<{
  key: ResumeExportColumnKey;
  label: string;
}> = [
  { key: "name", label: "Resume name" },
  { key: "version", label: "Version" },
  { key: "file_type", label: "File type" },
  { key: "file_size", label: "File size" },
  { key: "applications", label: "Linked applications" },
  { key: "is_active", label: "Active" },
  { key: "created_at", label: "Uploaded" }
];

export function defaultResumeFilters(): ResumeFilters {
  return {
    search: "",
    fileType: "",
    attachment: "all",
    uploadedFrom: "",
    uploadedTo: ""
  };
}

export function fileTypeLabel(
  resume: Pick<Resume, "content_type" | "file_name">
): string {
  const contentType = resume.content_type?.toLowerCase() ?? "";
  if (contentType.includes("pdf")) return "PDF";
  if (contentType.includes("word") || contentType.includes("document"))
    return "DOCX";
  const extension = resume.file_name?.split(".").pop()?.toUpperCase();
  return extension && extension.length <= 5 ? extension : "FILE";
}

export function formatFileSize(bytes: number | null): string {
  if (bytes === null || bytes === undefined) return "—";
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function tabMatches(row: ResumeRow, tab: ResumeTabKey): boolean {
  if (tab === "all") return true;
  if (tab === "active") return row.is_active;
  if (tab === "attached") return row.linkedApplications.length > 0;
  return row.linkedApplications.length === 0;
}

export function csvCell(value: unknown): string {
  const text =
    value === null || value === undefined
      ? ""
      : typeof value === "string" ||
          typeof value === "number" ||
          typeof value === "boolean"
        ? String(value)
        : "";
  return /[",\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

export function exportValue(
  row: ResumeRow,
  key: ResumeExportColumnKey
): string {
  switch (key) {
    case "name":
      return row.name;
    case "version":
      return row.version ?? "";
    case "file_type":
      return fileTypeLabel(row);
    case "file_size":
      return formatFileSize(row.file_size);
    case "applications":
      return String(row.linkedApplications.length);
    case "is_active":
      return row.is_active ? "Yes" : "No";
    case "created_at":
      return row.created_at;
  }
}
