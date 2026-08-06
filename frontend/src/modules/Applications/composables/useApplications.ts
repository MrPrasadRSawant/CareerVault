import { computed, onMounted, reactive, ref } from "vue";
import { useQuasar } from "quasar";
import { applicationApi, type Application, type ApplicationStatus } from "@/api/applications";
import { opportunityApi } from "@/api/opportunities";
import type { Opportunity } from "@/api/opportunities";
import { APPLICATION_STATUS_LABELS } from "@/modules/shared/statusColors";
import { defaultApplicationFilters, tabMatches } from "../utils";
import type { ApplicationFilters, ApplicationRow, ApplicationTabKey } from "../types";

export function useApplications() {
  const $q = useQuasar();
  const applications = ref<Application[]>([]);
  const opportunities = ref<Opportunity[]>([]);
  const loading = ref(false);
  const saving = ref(false);
  const activeTab = ref<ApplicationTabKey>("all");
  const filters = reactive<ApplicationFilters>(defaultApplicationFilters());

  const rows = computed<ApplicationRow[]>(() => applications.value.map(application => ({
    ...application,
    opportunity: opportunities.value.find(item => item.id === application.opportunity_id) ?? null
  })));

  const filteredRows = computed(() => rows.value.filter(row => {
    const opportunity = row.opportunity;
    const haystack = [
      opportunity?.title,
      opportunity?.company_name,
      opportunity?.job_location,
      row.notes,
      APPLICATION_STATUS_LABELS[row.status]
    ].filter(Boolean).join(" ").toLowerCase();
    const search = filters.search.trim().toLowerCase();
    if (search && !haystack.includes(search)) return false;
    if (!tabMatches(row.status, activeTab.value)) return false;
    if (filters.statuses.length && !filters.statuses.includes(row.status)) return false;
    if (filters.company && !(opportunity?.company_name ?? "").toLowerCase().includes(filters.company.toLowerCase())) return false;
    if (filters.location && !(opportunity?.job_location ?? "").toLowerCase().includes(filters.location.toLowerCase())) return false;
    if (filters.notes && !(row.notes ?? "").toLowerCase().includes(filters.notes.toLowerCase())) return false;
    if (filters.appliedFrom && (!row.applied_date || row.applied_date < filters.appliedFrom)) return false;
    if (filters.appliedTo && (!row.applied_date || row.applied_date > filters.appliedTo)) return false;
    if (filters.hasResume === "yes" && !row.resume_id) return false;
    if (filters.hasResume === "no" && row.resume_id) return false;
    if (filters.hasCoverLetter === "yes" && !row.cover_letter_id) return false;
    if (filters.hasCoverLetter === "no" && row.cover_letter_id) return false;
    return true;
  }));

  const tabCounts = computed<Record<ApplicationTabKey, number>>(() => ({
    all: rows.value.length,
    active: rows.value.filter(row => tabMatches(row.status, "active")).length,
    applied: rows.value.filter(row => tabMatches(row.status, "applied")).length,
    interviews: rows.value.filter(row => tabMatches(row.status, "interviews")).length,
    offer: rows.value.filter(row => tabMatches(row.status, "offer")).length,
    closed: rows.value.filter(row => tabMatches(row.status, "closed")).length
  }));

  async function load(): Promise<void> {
    loading.value = true;
    try {
      const [appList, opportunityList] = await Promise.all([applicationApi.list(), opportunityApi.list()]);
      applications.value = appList;
      opportunities.value = opportunityList;
    } catch {
      $q.notify({ type: "negative", message: "Could not load applications" });
    } finally {
      loading.value = false;
    }
  }

  function clearFilters(): void {
    Object.assign(filters, defaultApplicationFilters());
    activeTab.value = "all";
  }

  function replaceApplication(updated: Application): void {
    const index = applications.value.findIndex(application => application.id === updated.id);
    if (index !== -1) applications.value[index] = updated;
  }

  async function updateStatus(id: string, status: ApplicationStatus): Promise<void> {
    const previous = applications.value.find(application => application.id === id)?.status;
    saving.value = true;
    try {
      const updated = await applicationApi.updateStatus(id, status);
      replaceApplication(updated);
      $q.notify({ type: "positive", message: `Status updated to ${APPLICATION_STATUS_LABELS[status]}` });
    } catch {
      $q.notify({ type: "negative", message: "Could not update application status" });
      if (previous) replaceApplication({ ...(applications.value.find(application => application.id === id) as Application), status: previous });
    } finally {
      saving.value = false;
    }
  }

  async function createApplication(payload: Parameters<typeof applicationApi.create>[0]): Promise<boolean> {
    saving.value = true;
    try {
      const created = await applicationApi.create(payload);
      applications.value.unshift(created);
      $q.notify({ type: "positive", message: "Application recorded" });
      return true;
    } catch {
      $q.notify({ type: "negative", message: "Could not create application" });
      return false;
    } finally {
      saving.value = false;
    }
  }

  async function deleteApplication(row: ApplicationRow): Promise<void> {
    const confirmed = await new Promise<boolean>(resolve => {
      $q.dialog({ title: "Delete application?", message: `Remove the application for “${row.opportunity?.title ?? "this opportunity"}”?`, cancel: true, persistent: true }).onOk(() => resolve(true)).onCancel(() => resolve(false));
    });
    if (!confirmed) return;
    try {
      await applicationApi.remove(row.id);
      applications.value = applications.value.filter(application => application.id !== row.id);
      $q.notify({ type: "positive", message: "Application deleted" });
    } catch {
      $q.notify({ type: "negative", message: "Could not delete application" });
    }
  }

  onMounted(load);

  return { applications, opportunities, rows, filteredRows, tabCounts, filters, activeTab, loading, saving, load, clearFilters, updateStatus, createApplication, deleteApplication };
}
