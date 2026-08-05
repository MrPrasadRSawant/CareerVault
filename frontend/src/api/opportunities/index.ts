import { api } from "@/api/client";
import type {
  Opportunity,
  OpportunityCreate,
  OpportunityStatus
} from "./types";

export type { Opportunity, OpportunityCreate, OpportunityStatus };

export const opportunityApi = {
  list(status?: OpportunityStatus): Promise<Opportunity[]> {
    return api
      .get("/opportunities", {
        params: status ? { status, limit: 500 } : { limit: 500 }
      })
      .then(r => r.data);
  },

  get(id: string): Promise<Opportunity> {
    return api.get(`/opportunities/${id}`).then(r => r.data);
  },

  create(payload: OpportunityCreate): Promise<Opportunity> {
    return api.post("/opportunities", payload).then(r => r.data);
  },

  update(
    id: string,
    payload: Partial<OpportunityCreate>
  ): Promise<Opportunity> {
    return api.patch(`/opportunities/${id}`, payload).then(r => r.data);
  },

  remove(id: string): Promise<void> {
    return api.delete(`/opportunities/${id}`);
  }
};
