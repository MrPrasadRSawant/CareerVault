import type { CoverLetter } from "@/api/coverLetters";
import type {
  CoverLetterExportColumnKey,
  CoverLetterFilters,
  CoverLetterTabKey
} from "./types";

export const coverLetterTabs: Array<{
  key: CoverLetterTabKey;
  label: string;
}> = [
  { key: "all", label: "All" },
  { key: "with-content", label: "With content" },
  { key: "empty", label: "Empty" }
];

export const coverLetterExportColumns: Array<{
  key: CoverLetterExportColumnKey;
  label: string;
}> = [
  { key: "name", label: "Name" },
  { key: "file_name", label: "File name" },
  { key: "content_preview", label: "Content preview" },
  { key: "created_at", label: "Created" },
  { key: "updated_at", label: "Updated" }
];

export function defaultCoverLetterFilters(): CoverLetterFilters {
  return { search: "", createdFrom: "", createdTo: "" };
}

export function tabMatches(
  row: CoverLetter,
  tab: CoverLetterTabKey
): boolean {
  if (tab === "all") return true;
  if (tab === "with-content") return !!row.content;
  return !row.content;
}

export function csvCell(value: unknown): string {
  const text =
    value === null || value === undefined
      ? ""
      : typeof value === "string" || typeof value === "number" || typeof value === "boolean"
        ? String(value)
        : "";
  return /[",\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

export function contentPreview(content: string | null, max = 80): string {
  if (!content) return "";
  const single = content.replace(/\s+/g, " ").trim();
  return single.length > max ? single.slice(0, max) + "..." : single;
}

export function exportValue(
  row: CoverLetter,
  key: CoverLetterExportColumnKey
): string {
  switch (key) {
    case "name":
      return row.name;
    case "file_name":
      return row.file_name ?? "";
    case "content_preview":
      return contentPreview(row.content);
    case "created_at":
      return row.created_at;
    case "updated_at":
      return row.updated_at;
  }
}
