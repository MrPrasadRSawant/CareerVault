import { api } from "@/api/client";
import type { Resume, ResumeCreate, ResumeUpdate } from "./types";

export type { Resume, ResumeCreate, ResumeUpdate };

export const resumeApi = {
  list(): Promise<Resume[]> {
    return api.get("/resumes").then(r => r.data);
  },

  get(id: string): Promise<Resume> {
    return api.get(`/resumes/${id}`).then(r => r.data);
  },

  create(payload: ResumeCreate): Promise<Resume> {
    return api.post("/resumes", payload).then(r => r.data);
  },

  upload(file: File, name?: string): Promise<Resume> {
    const formData = new FormData();
    formData.append("file", file);
    if (name !== undefined) {
      formData.append("name", name);
    }
    return api.post("/resumes/upload", formData).then(r => r.data);
  },

  update(id: string, payload: ResumeUpdate): Promise<Resume> {
    return api.patch(`/resumes/${id}`, payload).then(r => r.data);
  },

  remove(id: string): Promise<void> {
    return api.delete(`/resumes/${id}`);
  }
};
