<template>
  <div class="panel-card">
    <q-table
      v-model:pagination="pagination"
      :rows="rows"
      :columns="columns"
      row-key="id"
      :loading="loading"
      flat
      bordered
      hide-pagination
      no-data-label="No resumes match these filters"
    >
      <template #body-cell-name="props">
        <q-td :props="props"
          ><button
            class="resume-title ellipsis"
            type="button"
            @click="$emit('view', props.row)"
            ><q-icon name="description" class="q-mr-sm" color="primary" />{{
              props.row.name
            }}</button
          ><div class="file-name ellipsis">{{
            props.row.file_name || "Uploaded resume"
          }}</div
          ><q-tooltip
            class="resume-tooltip"
            :offset="[0, 8]"
            style="
              padding: 0;
              overflow: visible;
              background: transparent;
              box-shadow: none;
            "
            ><div class="analysis-card"
              ><div class="analysis-kicker"
                ><q-icon name="insights" /> RESUME SNAPSHOT
                <q-badge v-if="props.row.is_active" class="active-badge"
                  >ACTIVE</q-badge
                ></div
              ><div class="analysis-title">{{ props.row.name }}</div
              ><div class="analysis-file"
                ><q-icon name="insert_drive_file" />
                {{ props.row.file_name || "Resume file" }}</div
              ><q-separator class="q-my-sm" /><div class="analysis-grid"
                ><div
                  ><span>TYPE</span
                  ><strong>{{ fileTypeLabel(props.row) }}</strong></div
                ><div
                  ><span>SIZE</span
                  ><strong>{{
                    formatFileSize(props.row.file_size)
                  }}</strong></div
                ><div
                  ><span>LINKED APPLICATIONS</span
                  ><strong>{{
                    props.row.linkedApplications.length
                  }}</strong></div
                ><div
                  ><span>VERSION</span
                  ><strong>{{
                    props.row.version || "Not specified"
                  }}</strong></div
                ></div
              ><div
                v-if="props.row.linkedApplications.length"
                class="analysis-links"
                >Used by: {{ linkedTitles(props.row)
                }}<span v-if="props.row.linkedApplications.length > 2">
                  +{{ props.row.linkedApplications.length - 2 }} more</span
                ></div
              ></div
            ></q-tooltip
          ></q-td
        >
      </template>
      <template #body-cell-version="props"
        ><q-td :props="props"
          ><span class="cell-text">{{ props.row.version || "—" }}</span></q-td
        ></template
      >
      <template #body-cell-file_type="props"
        ><q-td :props="props"
          ><q-badge
            outline
            color="primary"
            :label="fileTypeLabel(props.row)" /></q-td
      ></template>
      <template #body-cell-file_size="props"
        ><q-td :props="props">{{
          formatFileSize(props.row.file_size)
        }}</q-td></template
      >
      <template #body-cell-applications="props"
        ><q-td :props="props"
          ><q-badge
            rounded
            :color="props.row.linkedApplications.length ? 'primary' : 'grey-5'"
            :label="String(props.row.linkedApplications.length)"
          /><span class="q-ml-sm application-link-label">{{
            props.row.linkedApplications.length ? "Linked" : "Available"
          }}</span></q-td
        ></template
      >
      <template #body-cell-created_at="props"
        ><q-td :props="props">{{
          formatDate(props.row.created_at)
        }}</q-td></template
      >
      <template #body-cell-actions="props"
        ><q-td :props="props" class="actions-cell"
          ><q-btn
            flat
            round
            dense
            icon="visibility"
            color="primary"
            @click="$emit('view', props.row)"
            ><q-tooltip>Preview resume</q-tooltip></q-btn
          ><q-btn
            flat
            round
            dense
            icon="more_vert"
            color="primary"
            aria-label="More resume actions"
            ><q-menu anchor="bottom right" self="top right"
              ><q-list dense style="min-width: 190px"
                ><q-item
                  v-close-popup
                  clickable
                  @click="$emit('view', props.row)"
                  ><q-item-section avatar
                    ><q-icon name="visibility" /></q-item-section
                  ><q-item-section>Preview resume</q-item-section></q-item
                ><q-item
                  v-close-popup
                  clickable
                  @click="$emit('download', props.row)"
                  ><q-item-section avatar
                    ><q-icon name="download" /></q-item-section
                  ><q-item-section>Download file</q-item-section></q-item
                ><q-separator /><q-item
                  v-close-popup
                  clickable
                  :disable="props.row.linkedApplications.length > 0"
                  @click="$emit('delete', props.row)"
                  ><q-item-section avatar
                    ><q-icon
                      name="delete"
                      :color="
                        props.row.linkedApplications.length
                          ? 'grey-5'
                          : 'negative'
                      " /></q-item-section
                  ><q-item-section>{{
                    props.row.linkedApplications.length
                      ? "Attached — cannot delete"
                      : "Delete resume"
                  }}</q-item-section></q-item
                ></q-list
              ></q-menu
            ></q-btn
          ></q-td
        ></template
      >
    </q-table>

    <div v-if="!loading && rows.length > 0" class="table-footer">
      <span
        >Showing {{ firstVisibleRow }}–{{ lastVisibleRow }} of
        {{ rows.length }}</span
      >
      <q-pagination
        v-model="pagination.page"
        :max="pageCount"
        :max-pages="6"
        boundary-numbers
        direction-links
        color="primary"
        active-color="primary"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import type { QTableProps } from "quasar";
import type { ResumeRow } from "../types";
import { fileTypeLabel, formatFileSize } from "../utils";

const props = defineProps<{ rows: ResumeRow[]; loading: boolean }>();
defineEmits<{
  (event: "view", row: ResumeRow): void;
  (event: "download", row: ResumeRow): void;
  (event: "delete", row: ResumeRow): void;
}>();
const pagination = ref({ page: 1, rowsPerPage: 10 });
const columns: QTableProps["columns"] = [
  { name: "name", label: "Resume", align: "left", field: "name" },
  { name: "version", label: "Version", align: "left", field: "version" },
  {
    name: "file_type",
    label: "Type",
    align: "left",
    field: row => fileTypeLabel(row)
  },
  { name: "file_size", label: "Size", align: "left", field: "file_size" },
  {
    name: "applications",
    label: "Applications",
    align: "left",
    field: row => row.linkedApplications.length
  },
  { name: "created_at", label: "Uploaded", align: "left", field: "created_at" },
  { name: "actions", label: "", align: "right", field: "id" }
];
const pageCount = computed(() =>
  Math.max(1, Math.ceil(props.rows.length / pagination.value.rowsPerPage))
);
const firstVisibleRow = computed(
  () => (pagination.value.page - 1) * pagination.value.rowsPerPage + 1
);
const lastVisibleRow = computed(() =>
  Math.min(
    pagination.value.page * pagination.value.rowsPerPage,
    props.rows.length
  )
);

watch(
  () => props.rows,
  () => {
    pagination.value.page = 1;
  },
  { deep: false }
);
watch(pageCount, value => {
  if (pagination.value.page > value) pagination.value.page = value;
});

function formatDate(value: string) {
  return value ? new Date(value).toLocaleDateString() : "—";
}
function linkedTitles(row: ResumeRow) {
  return row.linkedApplications
    .slice(0, 2)
    .map(application => application.opportunityTitle)
    .join(", ");
}
</script>

<style lang="scss" scoped>
.panel-card {
  overflow: hidden;
  background: #fff;
  border: 1px solid #dce6eb;
  border-radius: 14px;
  box-shadow: 0 2px 8px rgba(16, 42, 67, 0.06);
}
.resume-title {
  display: block;
  max-width: 300px;
  border: 0;
  padding: 0;
  background: transparent;
  color: var(--cv-primary-dark);
  font-size: 14px;
  font-weight: 750;
  text-align: left;
  cursor: pointer;
}
.resume-title:hover {
  text-decoration: underline;
}
.file-name {
  max-width: 280px;
  margin: 3px 0 0 28px;
  color: var(--cv-muted-light);
  font-size: 11px;
}
.cell-text {
  color: var(--cv-text-strong);
}
.application-link-label {
  color: var(--cv-muted);
  font-size: 12px;
}
.actions-cell {
  white-space: nowrap;
}
.analysis-card {
  width: 330px;
  padding: 14px;
  border-radius: 12px;
  background: var(--cv-surface);
  color: var(--cv-navy);
  box-shadow: var(--cv-shadow-tooltip);
}
.analysis-kicker {
  display: flex;
  align-items: center;
  gap: 5px;
  color: var(--cv-muted-light);
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.06em;
}
.active-badge {
  margin-left: auto;
  background: var(--cv-status-offer);
  color: var(--cv-white);
  font-size: 9px;
}
.analysis-title {
  margin-top: 10px;
  color: var(--cv-navy);
  font-size: 16px;
  font-weight: 800;
  line-height: 1.25;
}
.analysis-file {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-top: 8px;
  overflow: hidden;
  color: var(--cv-muted);
  font-size: 12px;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.analysis-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
.analysis-grid span {
  display: block;
  color: var(--cv-muted-light);
  font-size: 9px;
  font-weight: 800;
}
.analysis-grid strong {
  display: block;
  margin-top: 2px;
  overflow: hidden;
  color: var(--cv-text-strong);
  font-size: 11px;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.analysis-links {
  margin-top: 10px;
  border-top: 1px solid var(--cv-border-light);
  padding-top: 9px;
  color: var(--cv-muted);
  font-size: 11px;
  line-height: 1.35;
}
.table-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 16px;
  border-top: 1px solid #edf2f5;
  color: #829ab1;
  font-size: 12px;
}
@media (max-width: 700px) {
  .analysis-card {
    width: 280px;
  }
  .table-footer {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
