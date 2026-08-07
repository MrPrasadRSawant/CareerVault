<template>
  <q-page class="cover-letters-page">
    <CoverLetterToolbar
      @create="showForm = true"
      @export="showExport = true"
      @refresh="load"
    />
    <CoverLetterFilters
      :filters="filters"
      :active-tab="activeTab"
      :counts="tabCounts"
      :result-count="filteredRows.length"
      @update:active-tab="activeTab = $event"
      @clear="clearFilters"
    />
    <CoverLetterTable
      :rows="filteredRows"
      :loading="loading"
      @view="openView"
      @edit="openEdit"
      @delete="deleteLetter"
    />
    <CoverLetterFormDialog
      v-model="showForm"
      :letter="editingLetter"
      :saving="saving"
      @save="onSave"
    />
    <CoverLetterViewDialog
      v-model="showView"
      :letter="viewingLetter"
    />
    <CoverLetterExportDialog
      v-model="showExport"
      :row-count="filteredRows.length"
      @export="exportCsv"
    />
  </q-page>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useQuasar } from "quasar";
import type { CoverLetter } from "@/api/coverLetters";
import CoverLetterToolbar from "./components/CoverLetterToolbar.vue";
import CoverLetterFilters from "./components/CoverLetterFilters.vue";
import CoverLetterTable from "./components/CoverLetterTable.vue";
import CoverLetterFormDialog from "./components/CoverLetterFormDialog.vue";
import CoverLetterViewDialog from "./components/CoverLetterViewDialog.vue";
import CoverLetterExportDialog from "./components/CoverLetterExportDialog.vue";
import { useCoverLetters } from "./composables/useCoverLetters";
import { csvCell, exportValue } from "./utils";
import type { CoverLetterExportColumnKey, CoverLetterRow } from "./types";

const $q = useQuasar();
const {
  filteredRows,
  tabCounts,
  filters,
  activeTab,
  loading,
  saving,
  load,
  clearFilters,
  createLetter,
  updateLetter,
  deleteLetter
} = useCoverLetters();

const showForm = ref(false);
const showView = ref(false);
const showExport = ref(false);
const editingLetter = ref<CoverLetter | null>(null);
const viewingLetter = ref<CoverLetter | null>(null);

function openEdit(row: CoverLetterRow) {
  editingLetter.value = row;
  showForm.value = true;
}

function openView(row: CoverLetterRow) {
  viewingLetter.value = row;
  showView.value = true;
}

async function onSave(payload: { name: string; content: string | null }) {
  if (editingLetter.value) {
    if (await updateLetter(editingLetter.value.id, payload))
      showForm.value = false;
  } else {
    if (await createLetter(payload)) showForm.value = false;
  }
  editingLetter.value = null;
}

function exportCsv(columns: CoverLetterExportColumnKey[]) {
  const header = columns
    .map(column =>
      csvCell(
        column.replace(/_/g, " ").replace(/^./, value => value.toUpperCase())
      )
    )
    .join(",");
  const body = filteredRows.value.map(row =>
    columns.map(column => csvCell(exportValue(row, column))).join(",")
  );
  const blob = new Blob([[header, ...body].join("\n")], {
    type: "text/csv;charset=utf-8;"
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `cover-letters-${new Date().toISOString().slice(0, 10)}.csv`;
  link.click();
  URL.revokeObjectURL(url);
  showExport.value = false;
  $q.notify({
    type: "positive",
    message: `Exported ${filteredRows.value.length} cover letters`
  });
}
</script>

<style lang="scss" scoped>
.cover-letters-page {
  max-width: 1500px;
  margin: 0 auto;
  padding: 24px;
}
@media (max-width: 700px) {
  .cover-letters-page {
    padding: 16px;
  }
}
</style>
