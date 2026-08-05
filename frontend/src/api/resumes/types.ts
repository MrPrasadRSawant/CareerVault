export interface Resume {
  id: string;
  name: string;
  version: string | null;
  file_name: string | null;
  content_type: string | null;
  file_size: number | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ResumeCreate {
  name: string;
  content?: string | null;
}

export interface ResumeUpdate {
  name?: string;
  is_active?: boolean;
  version?: string | null;
}
