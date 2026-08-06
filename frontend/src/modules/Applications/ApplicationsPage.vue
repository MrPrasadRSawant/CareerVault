<template>
  <q-page class="applications-page q-pa-md">
    <div class="page-shell">
      <ApplicationToolbar :has-opportunities="opportunities.length > 0" @create="showCreate = true" @export="showExport = true" @refresh="load" />
      <ApplicationFilters :filters="filters" :active-tab="activeTab" :counts="tabCounts" @update:active-tab="activeTab = $event" @clear="clearFilters" />
      <div class="results-meta q-mb-sm">Showing {{ filteredRows.length }} of {{ rows.length }} applications</div>
      <ApplicationTable :rows="filteredRows" :loading="loading" :saving="saving" @view="openView" @delete="deleteApplication" @status-change="onStatusChange" />
    </div>
    <ApplicationFormDialog v-model="showCreate" :opportunities="opportunities" :saving="saving" @save="onCreate" />
    <ApplicationViewDialog v-model="showView" :application="viewedApplication" />
    <ApplicationExportDialog v-model="showExport" :row-count="filteredRows.length" @export="exportCsv" />
  </q-page>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useQuasar } from "quasar";
import type { ApplicationStatus } from "@/api/applications";
import ApplicationToolbar from "./components/ApplicationToolbar.vue";
import ApplicationFilters from "./components/ApplicationFilters.vue";
import ApplicationTable from "./components/ApplicationTable.vue";
import ApplicationFormDialog from "./components/ApplicationFormDialog.vue";
import ApplicationViewDialog from "./components/ApplicationViewDialog.vue";
import ApplicationExportDialog from "./components/ApplicationExportDialog.vue";
import { useApplications } from "./composables/useApplications";
import { applicationExportValue, csvCell } from "./utils";
import type { ApplicationExportColumnKey, ApplicationRow } from "./types";

const $q = useQuasar();
const { opportunities, rows, filteredRows, tabCounts, filters, activeTab, loading, saving, load, clearFilters, updateStatus, createApplication, deleteApplication } = useApplications();
const showCreate = ref(false);
const showView = ref(false);
const showExport = ref(false);
const viewedApplication = ref<ApplicationRow | null>(null);

function openView(row: ApplicationRow) { viewedApplication.value = row; showView.value = true; }
async function onStatusChange(row: ApplicationRow, status: ApplicationStatus) { if (status !== row.status) await updateStatus(row.id, status); }
async function onCreate(payload: { opportunity_id: string; status: ApplicationStatus; applied_date: string | null; notes: string | null }) {
  if (await createApplication(payload)) showCreate.value = false;
}
function exportCsv(columns: ApplicationExportColumnKey[]) {
  const header = columns.map(column => csvCell(column.replace(/_/g, " ").replace(/^./, value => value.toUpperCase()))).join(",");
  const body = filteredRows.value.map(row => columns.map(column => csvCell(applicationExportValue(row, column))).join(","));
  const blob = new Blob([[header, ...body].join("\n")], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a"); link.href = url; link.download = `applications-${new Date().toISOString().slice(0, 10)}.csv`; link.click(); URL.revokeObjectURL(url);
  showExport.value = false;
  $q.notify({ type: "positive", message: `Exported ${filteredRows.value.length} applications` });
}
</script>

<style lang="scss" scoped>
.applications-page { background: var(--cv-surface-soft); }
.page-shell { max-width: 1360px; margin: 0 auto; }
.results-meta { color: var(--cv-muted-light); font-size: 12px; }
</style>
