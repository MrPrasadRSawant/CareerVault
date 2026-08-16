import { api } from "@/api/client";
import type { TermsOfService } from "./types";

export type { TermsOfService };

export const legalApi = {
  termsOfService(): Promise<TermsOfService> {
    return api.get("/legal/terms-of-service").then(response => response.data);
  }
};
