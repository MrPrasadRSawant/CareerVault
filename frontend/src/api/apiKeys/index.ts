import { api } from "../client";
import type {
  ApiKey,
  ApiKeyCreate,
  ApiKeyCreated,
  ApiKeyUpdate
} from "./types";

export const apiKeyApi = {
  list: () =>
    api.get<ApiKey[]>("/settings/api-keys").then(response => response.data),
  create: (payload: ApiKeyCreate) =>
    api
      .post<ApiKeyCreated>("/settings/api-keys", payload)
      .then(response => response.data),
  update: (id: string, payload: ApiKeyUpdate) =>
    api
      .patch<ApiKey>(`/settings/api-keys/${id}`, payload)
      .then(response => response.data),
  revoke: (id: string) => api.delete(`/settings/api-keys/${id}`)
};

export * from "./types";
