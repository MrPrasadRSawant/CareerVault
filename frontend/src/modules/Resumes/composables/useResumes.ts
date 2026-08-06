import { computed, onMounted, reactive, ref } from "vue";
import { useQuasar } from "quasar";
import { applicationApi } from "@/api/applications";
import { opportunityApi } from "@/api/opportunities";
import { resumeApi } from "@/api/resumes";
import { defaultResumeFilters, fileTypeLabel, tabMatches } from "../utils";
import type { ResumeFilters, ResumeRow, ResumeTabKey } from "../types";

export function useResumes() {
  const $q = useQuasar();
  const resumes = ref<ResumeRow[]>([]);
  const loading = ref(false);
  const saving = ref(false);
  const activeTab = ref<ResumeTabKey>("all");
  const filters = reactive<ResumeFilters>(defaultResumeFilters());

  const filteredRows = computed(() => resumes.value.filter(row => {
    const search = filters.search.trim().toLowerCase();
    const haystack = [row.name, row.version, row.file_name, fileTypeLabel(row)].filter(Boolean).join(" ").toLowerCase();
    if (search && !haystack.includes(search)) return false;
    if (!tabMatches(row, activeTab.value)) return false;
    if (filters.fileType && fileTypeLabel(row) !== filters.fileType) return false;
    if (filters.attachment === "attached" && row.linkedApplications.length === 0) return false;
    if (filters.attachment === "unattached" && row.linkedApplications.length > 0) return false;
    const createdDate = row.created_at.slice(0, 10);
    if (filters.uploadedFrom && createdDate < filters.uploadedFrom) return false;
    if (filters.uploadedTo && createdDate > filters.uploadedTo) return false;
    return true;
  }));

  const tabCounts = computed<Record<ResumeTabKey, number>>(() => ({
    all: resumes.value.length,
    active: resumes.value.filter(row => tabMatches(row, "active")).length,
    attached: resumes.value.filter(row => tabMatches(row, "attached")).length,
    unattached: resumes.value.filter(row => tabMatches(row, "unattached")).length
  }));

  async function load(): Promise<void> {
    loading.value = true;
    try {
      const [resumeList, applicationList, opportunityList] = await Promise.all([resumeApi.list(), applicationApi.list(), opportunityApi.list()]);
      const opportunityNames = new Map(opportunityList.map(opportunity => [opportunity.id, opportunity.title]));
      const linkedByResume = new Map<string, ResumeRow["linkedApplications"]>();
      for (const application of applicationList) {
        if (!application.resume_id) continue;
        const linked = linkedByResume.get(application.resume_id) ?? [];
        linked.push({ id: application.id, status: application.status, opportunityTitle: opportunityNames.get(application.opportunity_id) ?? "Unknown opportunity" });
        linkedByResume.set(application.resume_id, linked);
      }
      resumes.value = resumeList.map(resume => ({ ...resume, linkedApplications: linkedByResume.get(resume.id) ?? [] }));
    } catch {
      $q.notify({ type: "negative", message: "Could not load resumes" });
    } finally {
      loading.value = false;
    }
  }

  function clearFilters(): void {
    Object.assign(filters, defaultResumeFilters());
    activeTab.value = "all";
  }

  async function uploadResume(file: File, name: string, version: string): Promise<boolean> {
    saving.value = true;
    try {
      const uploaded = await resumeApi.upload(file, name || file.name, version || undefined);
      resumes.value.unshift({ ...uploaded, linkedApplications: [] });
      $q.notify({ type: "positive", message: "Resume uploaded" });
      return true;
    } catch {
      $q.notify({ type: "negative", message: "Could not upload resume" });
      return false;
    } finally {
      saving.value = false;
    }
  }

  async function deleteResume(row: ResumeRow): Promise<void> {
    if (row.linkedApplications.length > 0) {
      $q.notify({ type: "warning", message: "Attached resumes cannot be deleted" });
      return;
    }
    const confirmed = await new Promise<boolean>(resolve => {
      $q.dialog({ title: "Delete resume?", message: `Remove “${row.name}”? This cannot be undone.`, cancel: true, persistent: true }).onOk(() => resolve(true)).onCancel(() => resolve(false));
    });
    if (!confirmed) return;
    try {
      await resumeApi.remove(row.id);
      resumes.value = resumes.value.filter(resume => resume.id !== row.id);
      $q.notify({ type: "positive", message: "Resume deleted" });
    } catch {
      $q.notify({ type: "negative", message: "Could not delete resume" });
    }
  }

  onMounted(load);
  return { resumes, filteredRows, tabCounts, filters, activeTab, loading, saving, load, clearFilters, uploadResume, deleteResume };
}

