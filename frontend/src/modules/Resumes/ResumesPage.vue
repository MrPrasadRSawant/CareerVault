<template>
  <q-page class="resumes-page q-pa-md">
    <div class="page-shell">
      <ResumeToolbar @upload="showUpload = true" @export="showExport = true" @refresh="load" />
      <ResumeFilters :filters="filters" :active-tab="activeTab" :counts="tabCounts" @update:active-tab="activeTab = $event" @clear="clearFilters" />
      <div class="results-meta q-mb-sm">Showing {{ filteredRows.length }} of {{ resumes.length }} resumes</div>
      <ResumeTable :rows="filteredRows" :loading="loading" @view="openPreview" @download="downloadResume" @delete="deleteResume" />
    </div>
    <ResumeUploadDialog v-model="showUpload" :saving="saving" @save="onUpload" />
    <ResumePreviewDialog v-model="showPreview" :resume="previewResume" :preview-url="previewUrl" :preview-text="previewText" :loading="previewLoading" :error="previewError" @download="previewResume && downloadResume(previewResume)" />
    <ResumeExportDialog v-model="showExport" :row-count="filteredRows.length" @export="exportCsv" />
  </q-page>
</template>

<script setup lang="ts">
import { onBeforeUnmount, ref, watch } from "vue";
import { useQuasar } from "quasar";
import { resumeApi } from "@/api/resumes";
import ResumeToolbar from "./components/ResumeToolbar.vue";
import ResumeFilters from "./components/ResumeFilters.vue";
import ResumeTable from "./components/ResumeTable.vue";
import ResumeUploadDialog from "./components/ResumeUploadDialog.vue";
import ResumePreviewDialog from "./components/ResumePreviewDialog.vue";
import ResumeExportDialog from "./components/ResumeExportDialog.vue";
import { useResumes } from "./composables/useResumes";
import { csvCell, exportValue, fileTypeLabel } from "./utils";
import type { ResumeExportColumnKey, ResumeRow } from "./types";

const $q = useQuasar();
const { resumes, filteredRows, tabCounts, filters, activeTab, loading, saving, load, clearFilters, uploadResume, deleteResume } = useResumes();
const showUpload = ref(false);
const showPreview = ref(false);
const showExport = ref(false);
const previewResume = ref<ResumeRow | null>(null);
const previewUrl = ref<string | null>(null);
const previewText = ref<string | null>(null);
const previewLoading = ref(false);
const previewError = ref(false);

function clearPreviewUrl() {
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value);
  previewUrl.value = null;
}

async function openPreview(row: ResumeRow) {
  clearPreviewUrl();
  previewText.value = null;
  previewError.value = false;
  previewResume.value = row;
  showPreview.value = true;
  previewLoading.value = true;
  try {
    const blob = await resumeApi.download(row.id);
    if (["TXT", "MD"].includes(fileTypeLabel(row))) previewText.value = await blob.text();
    else {
      const previewBlob = fileTypeLabel(row) === "PDF" && blob.type !== "application/pdf" ? new Blob([blob], { type: "application/pdf" }) : blob;
      previewUrl.value = URL.createObjectURL(previewBlob);
    }
  } catch {
    previewError.value = true;
    $q.notify({ type: "negative", message: "Could not preview resume" });
  } finally {
    previewLoading.value = false;
  }
}

async function downloadResume(row: ResumeRow) {
  try {
    const blob = await resumeApi.download(row.id);
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = row.file_name || `${row.name}.${fileTypeLabel(row).toLowerCase()}`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  } catch {
    $q.notify({ type: "negative", message: "Could not download resume" });
  }
}

async function onUpload(payload: { file: File; name: string; version: string }) {
  if (await uploadResume(payload.file, payload.name, payload.version)) showUpload.value = false;
}

function exportCsv(columns: ResumeExportColumnKey[]) {
  const header = columns.map(column => csvCell(column.replace(/_/g, " ").replace(/^./, value => value.toUpperCase()))).join(",");
  const body = filteredRows.value.map(row => columns.map(column => csvCell(exportValue(row, column))).join(","));
  const blob = new Blob([[header, ...body].join("\n")], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `resumes-${new Date().toISOString().slice(0, 10)}.csv`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
  showExport.value = false;
  $q.notify({ type: "positive", message: `Exported ${filteredRows.value.length} resumes` });
}

watch(showPreview, open => { if (!open) { clearPreviewUrl(); previewText.value = null; previewResume.value = null; previewError.value = false; } });
onBeforeUnmount(clearPreviewUrl);
</script>

<style lang="scss" scoped>
.resumes-page { background: var(--cv-surface-soft); }
.page-shell { max-width: 1360px; margin: 0 auto; }
.results-meta { color: var(--cv-muted-light); font-size: 12px; }
</style>
