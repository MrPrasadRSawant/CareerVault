import { api } from "@/api/client";
import type {
  Application,
  ApplicationCreate,
  ApplicationStatus,
  StatusHistoryEntry
} from "./types";

export type {
  Application,
  ApplicationCreate,
  ApplicationStatus,
  StatusHistoryEntry
};

export const applicationApi = {
  list(): Promise<Application[]> {
    return api.get("/applications").then(r => r.data);
  },

  get(id: string): Promise<Application> {
    return api.get(`/applications/${id}`).then(r => r.data);
  },

  create(payload: ApplicationCreate): Promise<Application> {
    return api.post("/applications", payload).then(r => r.data);
  },

  update(
    id: string,
    payload: Partial<ApplicationCreate>
  ): Promise<Application> {
    return api.patch(`/applications/${id}`, payload).then(r => r.data);
  },

  updateStatus(
    id: string,
    status: ApplicationStatus,
    note?: string
  ): Promise<Application> {
    return api
      .post(`/applications/${id}/status`, { status, note })
      .then(r => r.data);
  },

  statusHistory(id: string): Promise<StatusHistoryEntry[]> {
    return api.get(`/applications/${id}/status-history`).then(r => r.data);
  },

  remove(id: string): Promise<void> {
    return api.delete(`/applications/${id}`);
  }
};
