import { api } from "@/api/client";
import type { CoverLetter, CoverLetterCreate } from "./types";

export type { CoverLetter, CoverLetterCreate };

export const coverLetterApi = {
  list(): Promise<CoverLetter[]> {
    return api.get("/cover-letters").then(r => r.data);
  },

  get(id: string): Promise<CoverLetter> {
    return api.get(`/cover-letters/${id}`).then(r => r.data);
  },

  create(payload: CoverLetterCreate): Promise<CoverLetter> {
    return api.post("/cover-letters", payload).then(r => r.data);
  },

  update(
    id: string,
    payload: Partial<CoverLetterCreate>
  ): Promise<CoverLetter> {
    return api.patch(`/cover-letters/${id}`, payload).then(r => r.data);
  },

  remove(id: string): Promise<void> {
    return api.delete(`/cover-letters/${id}`);
  }
};
