export interface CoverLetter {
  id: string;
  name: string;
  content: string | null;
  file_name: string | null;
  file_size: number | null;
  created_at: string;
  updated_at: string;
}

export interface CoverLetterCreate {
  name: string;
  content?: string | null;
}
