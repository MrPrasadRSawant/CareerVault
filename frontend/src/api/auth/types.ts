export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  created_at: string;
}

export interface TokenWithUser {
  access_token: string;
  token_type: string;
  user: User;
}
