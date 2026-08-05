import { api } from "@/api/client";
import type { TokenWithUser, User } from "./types";

export type { TokenWithUser, User };

export const authApi = {
  register(
    email: string,
    full_name: string,
    password: string
  ): Promise<TokenWithUser> {
    return api
      .post("/auth/register", { email, full_name, password })
      .then(r => r.data);
  },

  login(email: string, password: string): Promise<TokenWithUser> {
    return api.post("/auth/login", { email, password }).then(r => r.data);
  },

  me(): Promise<User> {
    return api.get("/auth/me").then(r => r.data);
  }
};
