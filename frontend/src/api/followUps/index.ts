import { api } from "@/api/client";
import type { FollowUp, FollowUpCreate } from "./types";

export type { FollowUp, FollowUpCreate };

export const followUpApi = {
  list(): Promise<FollowUp[]> {
    return api.get("/follow-ups").then(r => r.data);
  },

  get(id: string): Promise<FollowUp> {
    return api.get(`/follow-ups/${id}`).then(r => r.data);
  },

  create(payload: FollowUpCreate): Promise<FollowUp> {
    return api.post("/follow-ups", payload).then(r => r.data);
  },

  update(id: string, payload: Partial<FollowUpCreate>): Promise<FollowUp> {
    return api.patch(`/follow-ups/${id}`, payload).then(r => r.data);
  },

  remove(id: string): Promise<void> {
    return api.delete(`/follow-ups/${id}`);
  }
};
