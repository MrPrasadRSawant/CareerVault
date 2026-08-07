import type { CoverLetter } from "@/api/coverLetters";

export type CoverLetterTabKey = "all" | "with-content" | "empty";

export interface CoverLetterRow extends CoverLetter {}

export interface CoverLetterFilters {
  search: string;
  createdFrom: string;
  createdTo: string;
}

export type CoverLetterExportColumnKey =
  | "name"
  | "file_name"
  | "content_preview"
  | "created_at"
  | "updated_at";
