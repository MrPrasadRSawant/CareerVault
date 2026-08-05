export interface Company {
  id: string;
  name: string;
  website: string | null;
  location: string | null;
  industry: string | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface CompanyCreate {
  name: string;
  website?: string | null;
  location?: string | null;
  industry?: string | null;
  notes?: string | null;
}
