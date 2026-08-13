import { computed, ref } from "vue";
import { useQuasar } from "quasar";
import { applicationApi } from "@/api/applications";
import type { ApplicationCreate } from "@/api/applications";
import { opportunityApi } from "@/api/opportunities";
import type {
  Opportunity,
  OpportunityCreate,
  OpportunityStatus
} from "@/api/opportunities";
import { resumeApi } from "@/api/resumes";
import type { Resume } from "@/api/resumes";
import { useNotificationStore } from "@/stores/notifications";
import {
  csvEscape,
  createDefaultFilters,
  normalizeDateTime,
  opportunityExportColumns,
  parseCsv,
  statusLabel
} from "../utils";
import type {
  OpportunityExportColumnKey,
  OpportunityFilters
} from "../types";

export function useOpportunities() {
  const $q = useQuasar();
  const notificationStore = useNotificationStore();
  const opportunities = ref<Opportunity[]>([]);
  const resumes = ref<Resume[]>([]);
  const loading = ref(false);
  const saving = ref(false);
  const savingApplication = ref(false);
  const importing = ref(false);
  const filters = ref<OpportunityFilters>(createDefaultFilters());
  const selectedRows = ref<Opportunity[]>([]);
  const editingOpportunity = ref<Opportunity | null>(null);
  const selectedOpportunity = ref<Opportunity | null>(null);
  const formDialog = ref(false);
  const viewDialog = ref(false);
  const exportDialog = ref(false);
  const applicationDialog = ref(false);
  const convertingOpportunity = ref<Opportunity | null>(null);
  const updatingStatusIds = ref<string[]>([]);
  let resumesLoaded = false;

  const filteredOpportunities = computed(() => {
    const current = filters.value;
    const search = current.search.trim().toLowerCase();
    const company = current.company.trim().toLowerCase();
    const location = current.location.trim().toLowerCase();
    const experience = current.experience.trim().toLowerCase();
    const skills = current.skills.trim().toLowerCase();
    const from = current.postedFrom
      ? new Date(`${current.postedFrom}T00:00:00`).getTime()
      : null;
    const to = current.postedTo
      ? new Date(`${current.postedTo}T23:59:59.999`).getTime()
      : null;

    return opportunities.value.filter(opportunity => {
      if (
        current.statuses.length > 0 &&
        !current.statuses.includes(opportunity.status)
      ) {
        return false;
      }
      const text = [
        opportunity.title,
        opportunity.company_name,
        opportunity.job_location,
        opportunity.description,
        opportunity.experience_level,
        ...(opportunity.required_skills ?? [])
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      if (search && !text.includes(search)) return false;
      if (company && !String(opportunity.company_name ?? "").toLowerCase().includes(company)) return false;
      if (location && !String(opportunity.job_location ?? "").toLowerCase().includes(location)) return false;
      if (experience && !String(opportunity.experience_level ?? "").toLowerCase().includes(experience)) return false;
      if (skills && !(opportunity.required_skills ?? []).join(" ").toLowerCase().includes(skills)) return false;
      if (from !== null && (!opportunity.posted_on_utc || new Date(opportunity.posted_on_utc).getTime() < from)) return false;
      if (to !== null && (!opportunity.posted_on_utc || new Date(opportunity.posted_on_utc).getTime() > to)) return false;
      return true;
    });
  });

  async function load() {
    loading.value = true;
    try {
      opportunities.value = await opportunityApi.list();
    } catch {
      $q.notify({ type: "negative", message: "Could not load opportunities" });
    } finally {
      loading.value = false;
    }
  }

  function clearFilters() {
    filters.value = createDefaultFilters();
  }

  function openCreate() {
    editingOpportunity.value = null;
    formDialog.value = true;
  }

  function openEdit(opportunity: Opportunity) {
    editingOpportunity.value = opportunity;
    viewDialog.value = false;
    formDialog.value = true;
  }

  function openView(opportunity: Opportunity) {
    selectedOpportunity.value = opportunity;
    viewDialog.value = true;
  }

  async function openApplicationConversion(opportunity: Opportunity) {
    convertingOpportunity.value = opportunity;
    applicationDialog.value = true;
    if (resumesLoaded) return;
    try {
      resumes.value = await resumeApi.list();
      resumesLoaded = true;
    } catch {
      $q.notify({
        type: "warning",
        message: "Resumes could not be loaded; you can still create the application"
      });
    }
  }

  async function convertToApplication(payload: ApplicationCreate) {
    savingApplication.value = true;
    try {
      await applicationApi.create(payload);
      applicationDialog.value = false;
      convertingOpportunity.value = null;
      $q.notify({ type: "positive", message: "Application recorded" });
    } catch {
      $q.notify({ type: "negative", message: "Could not create application" });
    } finally {
      savingApplication.value = false;
    }
  }

  async function saveOpportunity(id: string | null, payload: OpportunityCreate) {
    saving.value = true;
    try {
      if (id) {
        const updated = await opportunityApi.update(id, payload);
        replaceOpportunity(updated);
        selectedOpportunity.value = updated;
      } else {
        await opportunityApi.create(payload);
      }
      formDialog.value = false;
      $q.notify({
        type: "positive",
        message: id ? "Opportunity updated" : "Opportunity created"
      });
      if (!id) await load();
      if (!id) await notificationStore.refreshUnseenCount();
    } catch {
      $q.notify({ type: "negative", message: "Could not save opportunity" });
    } finally {
      saving.value = false;
    }
  }

  async function updateStatus(opportunity: Opportunity, status: OpportunityStatus) {
    if (opportunity.status === status) return;
    updatingStatusIds.value = [...updatingStatusIds.value, opportunity.id];
    try {
      const updated = await opportunityApi.update(opportunity.id, { status });
      replaceOpportunity(updated);
      $q.notify({ type: "positive", message: "Status updated" });
    } catch {
      $q.notify({ type: "negative", message: "Could not update status" });
    } finally {
      updatingStatusIds.value = updatingStatusIds.value.filter(id => id !== opportunity.id);
    }
  }

  function replaceOpportunity(updated: Opportunity) {
    const index = opportunities.value.findIndex(item => item.id === updated.id);
    if (index >= 0) opportunities.value[index] = updated;
    selectedRows.value = selectedRows.value.map(item =>
      item.id === updated.id ? updated : item
    );
  }

  function confirmDelete(opportunity: Opportunity) {
    $q.dialog({
      title: "Delete opportunity?",
      message: `This will remove "${opportunity.title}" from your inbox.`,
      cancel: true,
      persistent: true,
      ok: { label: "Delete", color: "negative", unelevated: true }
    }).onOk(async () => {
      try {
        await opportunityApi.remove(opportunity.id);
        selectedRows.value = selectedRows.value.filter(row => row.id !== opportunity.id);
        opportunities.value = opportunities.value.filter(row => row.id !== opportunity.id);
        $q.notify({ type: "positive", message: "Opportunity deleted" });
      } catch {
        $q.notify({ type: "negative", message: "Could not delete opportunity" });
      }
    });
  }

  function confirmBulkDelete() {
    const ids = selectedRows.value.map(row => row.id);
    if (!ids.length) return;
    $q.dialog({
      title: "Delete selected opportunities?",
      message: `This will remove ${ids.length} selected opportunities from your inbox.`,
      cancel: true,
      persistent: true,
      ok: { label: "Delete selected", color: "negative", unelevated: true }
    }).onOk(async () => {
      try {
        await opportunityApi.bulkRemove(ids);
        const selected = new Set(ids);
        opportunities.value = opportunities.value.filter(row => !selected.has(row.id));
        selectedRows.value = [];
        $q.notify({ type: "positive", message: `${ids.length} opportunities deleted` });
      } catch {
        $q.notify({ type: "negative", message: "Could not delete selected opportunities" });
      }
    });
  }

  function downloadTemplate() {
    const headers = [
      "role",
      "company_name",
      "post_url",
      "company_career_page",
      "company_url",
      "posted_on_utc",
      "job_description",
      "skills_asked",
      "expected_work_experience",
      "job_location"
    ];
    downloadCsv(headers.join(",") + "\n", "careervault-opportunities-template.csv");
  }

  async function importCsv(file: File) {
    importing.value = true;
    try {
      const rows = parseCsv(await file.text());
      if (rows.length < 2) throw new Error("CSV has no rows");
      const headers = rows[0]!.map(header => header.trim().toLowerCase());
      const value = (row: string[], name: string) => row[headers.indexOf(name)]?.trim() || null;
      let imported = 0;
      for (const row of rows.slice(1)) {
        const title = value(row, "role");
        if (!title) continue;
        await opportunityApi.create({
          title,
          company_name: value(row, "company_name"),
          post_url: value(row, "post_url"),
          company_career_page: value(row, "company_career_page"),
          company_url: value(row, "company_url"),
          posted_on_utc: normalizeDateTime(value(row, "posted_on_utc") ?? ""),
          description: value(row, "job_description"),
          required_skills: (value(row, "skills_asked") ?? "").split(/[;,]/).map(skill => skill.trim()).filter(Boolean),
          experience_level: value(row, "expected_work_experience"),
          job_location: value(row, "job_location"),
          status: "draft"
        });
        imported += 1;
      }
      $q.notify({ type: "positive", message: `${imported} opportunities imported as drafts` });
      await load();
      await notificationStore.refreshUnseenCount();
    } catch {
      $q.notify({ type: "negative", message: "Could not import CSV. Download the template to check the column names." });
    } finally {
      importing.value = false;
    }
  }

  function openExport() {
    exportDialog.value = true;
  }

  function exportFiltered(columns: OpportunityExportColumnKey[]) {
    const selected = opportunityExportColumns.filter(column => columns.includes(column.key));
    if (!selected.length) {
      $q.notify({ type: "warning", message: "Choose at least one column to export" });
      return;
    }
    const lines = [
      selected.map(column => csvEscape(column.label)).join(","),
      ...filteredOpportunities.value.map(opportunity =>
        selected.map(column => csvEscape(column.value(opportunity))).join(",")
      )
    ];
    downloadCsv(`\uFEFF${lines.join("\r\n")}\r\n`, `careervault-opportunities-${new Date().toISOString().slice(0, 10)}.csv`);
    exportDialog.value = false;
    $q.notify({ type: "positive", message: `${filteredOpportunities.value.length} opportunities exported` });
  }

  function downloadCsv(content: string, filename: string) {
    const url = URL.createObjectURL(new Blob([content], { type: "text/csv;charset=utf-8" }));
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = filename;
    anchor.click();
    URL.revokeObjectURL(url);
  }

  return {
    opportunities,
    resumes,
    loading,
    saving,
    savingApplication,
    importing,
    filters,
    selectedRows,
    editingOpportunity,
    selectedOpportunity,
    formDialog,
    viewDialog,
    exportDialog,
    applicationDialog,
    convertingOpportunity,
    updatingStatusIds,
    filteredOpportunities,
    load,
    clearFilters,
    openCreate,
    openEdit,
    openView,
    openApplicationConversion,
    convertToApplication,
    saveOpportunity,
    updateStatus,
    confirmDelete,
    confirmBulkDelete,
    downloadTemplate,
    importCsv,
    openExport,
    exportFiltered,
    statusLabel
  };
}
