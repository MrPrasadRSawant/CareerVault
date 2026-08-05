import { api } from "@/api/client";
import type { Interview, InterviewCreate } from "./types";

export type { Interview, InterviewCreate };

export const interviewApi = {
  list(): Promise<Interview[]> {
    return api.get("/interviews").then(r => r.data);
  },

  get(id: string): Promise<Interview> {
    return api.get(`/interviews/${id}`).then(r => r.data);
  },

  create(payload: InterviewCreate): Promise<Interview> {
    return api.post("/interviews", payload).then(r => r.data);
  },

  update(id: string, payload: Partial<InterviewCreate>): Promise<Interview> {
    return api.patch(`/interviews/${id}`, payload).then(r => r.data);
  },

  remove(id: string): Promise<void> {
    return api.delete(`/interviews/${id}`);
  }
};
