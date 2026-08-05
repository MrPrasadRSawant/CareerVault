export interface ApiKey {
  id: string;
  name: string;
  key_prefix: string;
  created_on_utc: string;
  last_used_on_utc: string | null;
  expires_on_utc: string | null;
  is_revoked: boolean;
}

export interface ApiKeyCreated extends ApiKey {
  key: string;
}

export interface ApiKeyCreate {
  name: string;
  expires_on_utc?: string | null;
}

export type ApiKeyUpdate = ApiKeyCreate;
