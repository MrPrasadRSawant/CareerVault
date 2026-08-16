import { api } from "@/api/client";
import type { PasswordPolicy, TokenWithUser, User, UserRole } from "./types";

export type { PasswordPolicy, TokenWithUser, User, UserRole };

export const authApi = {
  passwordPolicy(): Promise<PasswordPolicy> {
    return api.get("/auth/password-policy").then(r => r.data);
  },

  register(
    email: string,
    full_name: string,
    password: string,
    termsVersion: number
  ): Promise<TokenWithUser> {
    return api
      .post("/auth/register", {
        email,
        full_name,
        password,
        terms_accepted: true,
        terms_version: termsVersion
      })
      .then(r => r.data);
  },

  login(email: string, password: string): Promise<TokenWithUser> {
    return api.post("/auth/login", { email, password }).then(r => r.data);
  },

  changePassword(currentPassword: string, newPassword: string): Promise<void> {
    return api
      .post("/auth/change-password", {
        current_password: currentPassword,
        new_password: newPassword
      })
      .then(() => undefined);
  },

  logout(): Promise<void> {
    return api.post("/auth/logout").then(() => undefined);
  },

  me(): Promise<User> {
    return api.get("/auth/me").then(r => r.data);
  }
};
