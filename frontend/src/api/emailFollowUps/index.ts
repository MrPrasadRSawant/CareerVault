import { api } from "@/api/client";
import type {
  EmailFollowUp,
  EmailFollowUpGroup,
  EmailFollowUpPayload
} from "./types";

export type {
  EmailFollowUp,
  EmailFollowUpGroup,
  EmailFollowUpOutcome,
  EmailFollowUpPayload
} from "./types";

export const emailFollowUpApi = {
  list(): Promise<EmailFollowUpGroup[]> {
    return api.get("/email-follow-ups").then(response => response.data);
  },

  get(id: string): Promise<EmailFollowUp> {
    return api.get(`/email-follow-ups/${id}`).then(response => response.data);
  },

  create(payload: EmailFollowUpPayload): Promise<EmailFollowUp> {
    return api
      .post("/email-follow-ups", payload)
      .then(response => response.data);
  },

  update(
    id: string,
    payload: Partial<EmailFollowUpPayload>
  ): Promise<EmailFollowUp> {
    return api
      .patch(`/email-follow-ups/${id}`, payload)
      .then(response => response.data);
  },

  remove(id: string): Promise<void> {
    return api.delete(`/email-follow-ups/${id}`);
  }
};
