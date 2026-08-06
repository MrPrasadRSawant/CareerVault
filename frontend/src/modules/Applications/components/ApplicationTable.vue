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
      no-data-label="No applications match these filters"
    >
      <template #body-cell-opportunity="props">
        <q-td :props="props">
          <button
            class="title-button ellipsis"
            type="button"
            @click="$emit('view', props.row)"
            >{{ props.row.opportunity?.title ?? "Unknown opportunity" }}</button
          >
          <q-tooltip
            class="application-tooltip"
            :offset="[0, 8]"
            style="
              padding: 0;
              overflow: visible;
              background: transparent;
              box-shadow: none;
            "
          >
            <div class="analysis-card">
              <div class="analysis-kicker"
                ><q-icon name="insights" /> APPLICATION SNAPSHOT
                <q-badge
                  class="status-badge"
                  :style="statusStyle(props.row.status)"
                  >{{ statusLabel(props.row.status) }}</q-badge
                ></div
              >
              <div class="analysis-title">{{
                props.row.opportunity?.title ?? "Unknown opportunity"
              }}</div>
              <div class="analysis-company"
                ><q-icon name="business" />
                {{
                  props.row.opportunity?.company_name ?? "Company not specified"
                }}</div
              >
              <q-separator class="q-my-sm" />
              <div class="analysis-grid">
                <div
                  ><span>APPLIED</span
                  ><strong>{{
                    props.row.applied_date || "Not yet"
                  }}</strong></div
                >
                <div
                  ><span>LOCATION</span
                  ><strong>{{
                    props.row.opportunity?.job_location || "Not specified"
                  }}</strong></div
                >
                <div
                  ><span>RESUME</span
                  ><strong>{{
                    props.row.resume?.name || "Missing"
                  }}</strong></div
                >
                <div
                  ><span>COVER LETTER</span
                  ><strong>{{
                    props.row.cover_letter_id ? "Attached" : "Missing"
                  }}</strong></div
                >
              </div>
              <div v-if="props.row.notes" class="analysis-notes">{{
                props.row.notes
              }}</div>
            </div>
          </q-tooltip>
        </q-td>
      </template>
      <template #body-cell-company="props"
        ><q-td :props="props"
          ><span class="ellipsis cell-text">{{
            props.row.opportunity?.company_name || "—"
          }}</span></q-td
        ></template
      >
      <template #body-cell-status="props">
        <q-td :props="props">
          <q-select
            v-if="editingStatusId === props.row.id"
            :model-value="props.row.status"
            :options="statusOptions"
            dense
            outlined
            emit-value
            map-options
            options-dense
            :loading="saving"
            class="status-select"
            autofocus
            @update:model-value="onStatusSelected(props.row, $event)"
            @blur="stopEditing"
            @keyup.esc="stopEditing"
          />
          <span
            v-else
            class="status-display status-chip"
            tabindex="0"
            :style="statusStyle(props.row.status)"
            @dblclick="startEditing(props.row)"
          >
            {{ statusLabel(props.row.status) }}
            <q-tooltip>Double-click to edit status</q-tooltip>
          </span>
        </q-td>
      </template>
      <template #body-cell-resume="props">
        <q-td :props="props">
          <div v-if="props.row.resume" class="resume-cell">
            <button
              class="resume-link ellipsis"
              type="button"
              @click="$emit('preview-resume', props.row.resume)"
              ><q-icon name="description" class="q-mr-xs" />{{
                props.row.resume.name
              }}</button
            >
            <q-tooltip>Preview attached resume</q-tooltip>
          </div>
          <span v-else class="missing-resume">Not attached</span>
        </q-td>
      </template>
      <template #body-cell-applied_date="props"
        ><q-td :props="props">{{
          props.row.applied_date || "—"
        }}</q-td></template
      >
      <template #body-cell-notes="props">
        <q-td :props="props"
          ><span class="ellipsis cell-text">{{ props.row.notes || "—" }}</span
          ><q-tooltip v-if="props.row.notes">{{
            props.row.notes
          }}</q-tooltip></q-td
        >
      </template>
      <template #body-cell-actions="props">
        <q-td :props="props" class="actions-cell">
          <q-btn
            flat
            round
            dense
            icon="visibility"
            color="primary"
            @click="$emit('view', props.row)"
          />
          <q-btn
            flat
            round
            dense
            icon="more_vert"
            color="primary"
            aria-label="More actions"
          >
            <q-menu anchor="bottom right" self="top right">
              <q-list dense style="min-width: 190px">
                <q-item
                  v-close-popup
                  clickable
                  @click="$emit('view', props.row)"
                  ><q-item-section avatar
                    ><q-icon name="visibility" /></q-item-section
                  ><q-item-section>View details</q-item-section></q-item
                >
                <q-item
                  v-if="props.row.opportunity?.post_url"
                  v-close-popup
                  clickable
                  tag="a"
                  :href="props.row.opportunity.post_url"
                  target="_blank"
                  ><q-item-section avatar
                    ><q-icon name="open_in_new" /></q-item-section
                  ><q-item-section>Open job post</q-item-section></q-item
                >
                <q-item
                  v-if="props.row.opportunity?.company_url"
                  v-close-popup
                  clickable
                  tag="a"
                  :href="props.row.opportunity.company_url"
                  target="_blank"
                  ><q-item-section avatar
                    ><q-icon name="language" /></q-item-section
                  ><q-item-section>Company website</q-item-section></q-item
                >
                <q-item
                  v-if="props.row.opportunity?.company_career_page"
                  v-close-popup
                  clickable
                  tag="a"
                  :href="props.row.opportunity.company_career_page"
                  target="_blank"
                  ><q-item-section avatar
                    ><q-icon name="work_outline" /></q-item-section
                  ><q-item-section>Career page</q-item-section></q-item
                >
                <q-separator />
                <q-item
                  v-if="props.row.resume"
                  v-close-popup
                  clickable
                  @click="$emit('preview-resume', props.row.resume)"
                  ><q-item-section avatar
                    ><q-icon name="picture_as_pdf" /></q-item-section
                  ><q-item-section
                    >Preview attached resume</q-item-section
                  ></q-item
                >
                <q-item
                  v-close-popup
                  clickable
                  @click="$emit('bind-resume', props.row)"
                  ><q-item-section avatar><q-icon name="link" /></q-item-section
                  ><q-item-section>{{
                    props.row.resume ? "Change bound resume" : "Bind resume"
                  }}</q-item-section></q-item
                >
                <q-separator />
                <q-item
                  v-close-popup
                  clickable
                  class="text-negative"
                  @click="$emit('delete', props.row)"
                  ><q-item-section avatar
                    ><q-icon name="delete" color="negative" /></q-item-section
                  ><q-item-section>Delete application</q-item-section></q-item
                >
              </q-list>
            </q-menu>
          </q-btn>
        </q-td>
      </template>
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
import type { ApplicationStatus } from "@/api/applications";
import {
  APPLICATION_STATUS_COLORS,
  APPLICATION_STATUS_LABELS
} from "@/modules/shared/statusColors";
import { applicationStatusOptions } from "../utils";
import type { ApplicationRow } from "../types";

const props = defineProps<{
  rows: ApplicationRow[];
  loading: boolean;
  saving: boolean;
}>();
const emit = defineEmits<{
  (event: "view", row: ApplicationRow): void;
  (event: "delete", row: ApplicationRow): void;
  (event: "bind-resume", row: ApplicationRow): void;
  (
    event: "preview-resume",
    resume: NonNullable<ApplicationRow["resume"]>
  ): void;
  (
    event: "status-change",
    row: ApplicationRow,
    status: ApplicationStatus
  ): void;
}>();
const statusOptions = applicationStatusOptions;
const pagination = ref({ page: 1, rowsPerPage: 10 });
const editingStatusId = ref<string | null>(null);
const columns: QTableProps["columns"] = [
  {
    name: "opportunity",
    label: "Opportunity",
    align: "left",
    field: row => row.opportunity?.title ?? ""
  },
  {
    name: "company",
    label: "Company",
    align: "left",
    field: row => row.opportunity?.company_name ?? ""
  },
  { name: "status", label: "Status", align: "left", field: "status" },
  {
    name: "resume",
    label: "Resume",
    align: "left",
    field: row => row.resume?.name ?? ""
  },
  {
    name: "applied_date",
    label: "Applied on",
    align: "left",
    field: "applied_date"
  },
  { name: "notes", label: "Notes", align: "left", field: "notes" },
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

function statusLabel(status: ApplicationStatus) {
  return APPLICATION_STATUS_LABELS[status];
}
function statusStyle(status: ApplicationStatus) {
  return {
    background: APPLICATION_STATUS_COLORS[status],
    color: "var(--cv-white)"
  };
}
function startEditing(row: ApplicationRow) {
  editingStatusId.value = row.id;
}
function stopEditing() {
  editingStatusId.value = null;
}
function onStatusSelected(row: ApplicationRow, status: ApplicationStatus) {
  if (status !== row.status) emit("status-change", row, status);
  stopEditing();
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
.title-button {
  display: block;
  max-width: 270px;
  border: 0;
  padding: 0;
  background: transparent;
  color: var(--cv-primary-dark);
  font-size: 14px;
  font-weight: 750;
  text-align: left;
  cursor: pointer;
}
.title-button:hover {
  text-decoration: underline;
}
.cell-text {
  display: block;
  max-width: 210px;
  color: var(--cv-muted);
}
.status-display {
  display: inline-flex;
  align-items: center;
  cursor: pointer;
  outline: none;
}
.status-display:focus-visible {
  border-radius: 5px;
  box-shadow: 0 0 0 2px var(--cv-focus-ring);
}
.status-chip {
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
}
.status-select {
  min-width: 170px;
}
.resume-cell {
  max-width: 190px;
}
.resume-link {
  display: block;
  max-width: 190px;
  overflow: hidden;
  border: 0;
  padding: 0;
  background: transparent;
  color: var(--cv-primary-dark);
  font-size: 12px;
  text-align: left;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: pointer;
}
.resume-link:hover {
  text-decoration: underline;
}
.missing-resume {
  color: var(--cv-muted-light);
  font-size: 12px;
}
.actions-cell {
  white-space: nowrap;
}
.analysis-card {
  width: 320px;
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
.status-badge {
  margin-left: auto;
  font-size: 10px;
}
.analysis-title {
  margin-top: 10px;
  color: var(--cv-navy);
  font-size: 16px;
  font-weight: 800;
  line-height: 1.25;
}
.analysis-company {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-top: 8px;
  color: var(--cv-muted);
  font-size: 12px;
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
.analysis-notes {
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
    width: 270px;
  }
  .table-footer {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
