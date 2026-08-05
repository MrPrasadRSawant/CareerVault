import { api } from "@/api/client";
import type { Company, CompanyCreate } from "./types";

export type { Company, CompanyCreate };

export const companyApi = {
  list(): Promise<Company[]> {
    return api.get("/companies").then(r => r.data);
  },

  get(id: string): Promise<Company> {
    return api.get(`/companies/${id}`).then(r => r.data);
  },

  create(payload: CompanyCreate): Promise<Company> {
    return api.post("/companies", payload).then(r => r.data);
  },

  update(id: string, payload: Partial<CompanyCreate>): Promise<Company> {
    return api.patch(`/companies/${id}`, payload).then(r => r.data);
  },

  remove(id: string): Promise<void> {
    return api.delete(`/companies/${id}`);
  }
};
