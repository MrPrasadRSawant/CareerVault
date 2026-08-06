<template>
  <q-page class="applications-page">
    <ApplicationToolbar
      :has-opportunities="opportunities.length > 0"
      @create="showCreate = true"
      @export="showExport = true"
      @refresh="load"
    />
    <ApplicationFilters
      :filters="filters"
      :active-tab="activeTab"
      :counts="tabCounts"
      :result-count="filteredRows.length"
      @update:active-tab="activeTab = $event"
      @clear="clearFilters"
    />
    <ApplicationTable
      :rows="filteredRows"
      :loading="loading"
      :saving="saving"
      @view="openView"
      @delete="deleteApplication"
      @bind-resume="openBinding"
      @preview-resume="openResumePreview"
      @status-change="onStatusChange"
    />
    <ApplicationFormDialog
      v-model="showCreate"
      :opportunities="opportunities"
      :resumes="resumes"
      :saving="saving"
      @save="onCreate"
    />
    <ApplicationViewDialog
      v-model="showView"
      :application="viewedApplication"
    />
    <ApplicationExportDialog
      v-model="showExport"
      :row-count="filteredRows.length"
      @export="exportCsv"
    />
    <ApplicationResumeBindingDialog
      v-model="showBinding"
      :application="bindingApplication"
      :resumes="resumes"
      :saving="saving"
      @save="onBindResume"
    />
    <ResumePreviewDialog
      v-model="showResumePreview"
      :resume="previewResume"
      :preview-url="previewUrl"
      :preview-text="previewText"
      :loading="previewLoading"
      :error="previewError"
      @download="previewResume && downloadResume(previewResume)"
    />
  </q-page>
</template>

<script setup lang="ts">
import { onBeforeUnmount, ref, watch } from "vue";
import { useQuasar } from "quasar";
import type { ApplicationStatus } from "@/api/applications";
import { resumeApi } from "@/api/resumes";
import type { Resume } from "@/api/resumes";
import ApplicationToolbar from "./components/ApplicationToolbar.vue";
import ApplicationFilters from "./components/ApplicationFilters.vue";
import ApplicationTable from "./components/ApplicationTable.vue";
import ApplicationFormDialog from "./components/ApplicationFormDialog.vue";
import ApplicationViewDialog from "./components/ApplicationViewDialog.vue";
import ApplicationExportDialog from "./components/ApplicationExportDialog.vue";
import ApplicationResumeBindingDialog from "./components/ApplicationResumeBindingDialog.vue";
import ResumePreviewDialog from "@/modules/Resumes/components/ResumePreviewDialog.vue";
import { useApplications } from "./composables/useApplications";
import { applicationExportValue, csvCell } from "./utils";
import { fileTypeLabel } from "@/modules/Resumes/utils";
import type { ApplicationExportColumnKey, ApplicationRow } from "./types";

const $q = useQuasar();
const {
  opportunities,
  resumes,
  filteredRows,
  tabCounts,
  filters,
  activeTab,
  loading,
  saving,
  load,
  clearFilters,
  updateStatus,
  createApplication,
  bindResume,
  deleteApplication
} = useApplications();
const showCreate = ref(false);
const showView = ref(false);
const showExport = ref(false);
const showBinding = ref(false);
const showResumePreview = ref(false);
const viewedApplication = ref<ApplicationRow | null>(null);
const bindingApplication = ref<ApplicationRow | null>(null);
const previewResume = ref<Resume | null>(null);
const previewUrl = ref<string | null>(null);
const previewText = ref<string | null>(null);
const previewLoading = ref(false);
const previewError = ref(false);

function openView(row: ApplicationRow) {
  viewedApplication.value = row;
  showView.value = true;
}
function openBinding(row: ApplicationRow) {
  bindingApplication.value = row;
  showBinding.value = true;
}
async function onBindResume(resumeId: string | null) {
  if (!bindingApplication.value) return;
  if (await bindResume(bindingApplication.value.id, resumeId))
    showBinding.value = false;
}
async function onStatusChange(row: ApplicationRow, status: ApplicationStatus) {
  if (status !== row.status) await updateStatus(row.id, status);
}
async function onCreate(payload: {
  opportunity_id: string;
  resume_id: string | null;
  status: ApplicationStatus;
  applied_date: string | null;
  notes: string | null;
}) {
  if (await createApplication(payload)) showCreate.value = false;
}

function clearPreviewUrl() {
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value);
  previewUrl.value = null;
}

async function openResumePreview(resume: Resume) {
  clearPreviewUrl();
  previewText.value = null;
  previewError.value = false;
  previewResume.value = resume;
  showResumePreview.value = true;
  previewLoading.value = true;
  try {
    const blob = await resumeApi.download(resume.id);
    if (["TXT", "MD"].includes(fileTypeLabel(resume)))
      previewText.value = await blob.text();
    else {
      const previewBlob =
        fileTypeLabel(resume) === "PDF" && blob.type !== "application/pdf"
          ? new Blob([blob], { type: "application/pdf" })
          : blob;
      previewUrl.value = URL.createObjectURL(previewBlob);
    }
  } catch {
    previewError.value = true;
    $q.notify({
      type: "negative",
      message: "Could not preview attached resume"
    });
  } finally {
    previewLoading.value = false;
  }
}

async function downloadResume(resume: Resume) {
  try {
    const blob = await resumeApi.download(resume.id);
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download =
      resume.file_name ||
      `${resume.name}.${fileTypeLabel(resume).toLowerCase()}`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  } catch {
    $q.notify({
      type: "negative",
      message: "Could not download attached resume"
    });
  }
}

function exportCsv(columns: ApplicationExportColumnKey[]) {
  const header = columns
    .map(column =>
      csvCell(
        column.replace(/_/g, " ").replace(/^./, value => value.toUpperCase())
      )
    )
    .join(",");
  const body = filteredRows.value.map(row =>
    columns
      .map(column => csvCell(applicationExportValue(row, column)))
      .join(",")
  );
  const blob = new Blob([[header, ...body].join("\n")], {
    type: "text/csv;charset=utf-8;"
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `applications-${new Date().toISOString().slice(0, 10)}.csv`;
  link.click();
  URL.revokeObjectURL(url);
  showExport.value = false;
  $q.notify({
    type: "positive",
    message: `Exported ${filteredRows.value.length} applications`
  });
}

watch(showResumePreview, open => {
  if (!open) {
    clearPreviewUrl();
    previewText.value = null;
    previewResume.value = null;
    previewError.value = false;
  }
});
onBeforeUnmount(clearPreviewUrl);
</script>

<style lang="scss" scoped>
.applications-page {
  max-width: 1500px;
  margin: 0 auto;
  padding: 24px;
}
@media (max-width: 700px) {
  .applications-page {
    padding: 16px;
  }
}
</style>
