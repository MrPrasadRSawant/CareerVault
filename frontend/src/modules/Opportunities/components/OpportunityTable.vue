<template>
  <div class="panel-card">
    <q-table
      v-model:pagination="pagination"
      v-model:selected="selected"
      :rows="rows"
      :columns="columns"
      row-key="id"
      selection="multiple"
      :loading="loading"
      flat
      bordered
      hide-pagination
      no-data-label="No opportunities match your filters"
    >
      <template #loading><q-inner-loading showing color="primary" /></template>

      <template #body-cell-title="props">
        <q-td :props="props">
          <button
            class="role-link"
            type="button"
            @click.stop="viewRow(props.row)"
          >
            <span class="role-title">{{ props.row.title }}</span>
            <span class="role-source"
              >Posted {{ formatOpportunityDate(props.row.posted_on_utc) }}</span
            >
            <q-tooltip
              class="role-tooltip"
              :offset="[0, 8]"
              style="
                padding: 0;
                overflow: visible;
                background: transparent;
                box-shadow: none;
              "
            >
              <div class="analysis-card">
                <div class="analysis-eyebrow">
                  <span
                    ><q-icon name="insights" size="14px" /> Opportunity
                    snapshot</span
                  >
                  <span
                    class="analysis-status"
                    :style="statusStyle(props.row.status)"
                    >{{ statusLabel(props.row.status) }}</span
                  >
                </div>
                <div class="analysis-title">{{ props.row.title }}</div>
                <div class="analysis-company"
                  ><q-icon name="business" size="15px" />
                  {{ props.row.company_name || "Company not specified" }}</div
                >
                <div class="analysis-grid">
                  <div
                    ><span>Location</span
                    ><strong>{{
                      props.row.job_location || "Not specified"
                    }}</strong></div
                  >
                  <div
                    ><span>Experience</span
                    ><strong>{{
                      props.row.experience_level || "Not specified"
                    }}</strong></div
                  >
                  <div
                    ><span>Posted</span
                    ><strong>{{
                      formatOpportunityDate(props.row.posted_on_utc)
                    }}</strong></div
                  >
                  <div
                    ><span>Skills</span
                    ><strong
                      >{{
                        props.row.required_skills?.length || 0
                      }}
                      listed</strong
                    ></div
                  >
                </div>
              </div>
            </q-tooltip>
          </button>
        </q-td>
      </template>

      <template #body-cell-company_name="props">
        <q-td :props="props"
          ><span class="company-name">{{
            props.row.company_name || "—"
          }}</span></q-td
        >
      </template>

      <template #body-cell-status="props">
        <q-td
          :props="props"
          class="status-cell"
          @dblclick="beginStatusEdit(props.row)"
        >
          <q-select
            v-if="editingStatusId === props.row.id"
            :model-value="props.row.status"
            dense
            autofocus
            options-dense
            emit-value
            map-options
            outlined
            class="inline-status"
            :options="statusOptions"
            :loading="updatingStatusIds.includes(props.row.id)"
            @update:model-value="onStatusSelected(props.row, $event)"
            @blur="editingStatusId = null"
          />
          <span
            v-else
            class="status-chip"
            :style="statusStyle(props.row.status)"
          >
            {{ statusLabel(props.row.status) }}
          </span>
          <q-tooltip v-if="editingStatusId !== props.row.id"
            >Double-click to edit status</q-tooltip
          >
        </q-td>
      </template>

      <template #body-cell-posted_on_utc="props">
        <q-td :props="props" class="date-cell">{{
          formatOpportunityDate(props.row.posted_on_utc)
        }}</q-td>
      </template>

      <template #body-cell-job_location="props">
        <q-td :props="props"
          ><span class="location-cell"
            ><q-icon name="place" size="15px" />{{
              props.row.job_location || "Not specified"
            }}</span
          ></q-td
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
            @click.stop="viewRow(props.row)"
            ><q-tooltip>View opportunity</q-tooltip></q-btn
          >
          <q-btn
            flat
            round
            dense
            icon="edit"
            color="primary"
            @click.stop="editRow(props.row)"
            ><q-tooltip>Edit opportunity</q-tooltip></q-btn
          >
          <q-btn flat round dense icon="more_vert" color="primary">
            <q-menu anchor="bottom right" self="top right">
              <q-list dense style="min-width: 190px">
                <q-item clickable v-close-popup @click="viewRow(props.row)"
                  ><q-item-section avatar
                    ><q-icon name="visibility" /></q-item-section
                  ><q-item-section>View details</q-item-section></q-item
                >
                <q-item clickable v-close-popup @click="convertRow(props.row)"
                  ><q-item-section avatar
                    ><q-icon name="assignment_turned_in" /></q-item-section
                  ><q-item-section
                    >Convert to application</q-item-section
                  ></q-item
                >
                <q-item
                  v-if="props.row.post_url"
                  clickable
                  v-close-popup
                  tag="a"
                  :href="props.row.post_url"
                  target="_blank"
                  rel="noopener noreferrer"
                  ><q-item-section avatar
                    ><q-icon name="open_in_new" /></q-item-section
                  ><q-item-section>Open job post</q-item-section></q-item
                >
                <q-item
                  v-if="props.row.company_career_page"
                  clickable
                  v-close-popup
                  tag="a"
                  :href="props.row.company_career_page"
                  target="_blank"
                  rel="noopener noreferrer"
                  ><q-item-section avatar
                    ><q-icon name="business" /></q-item-section
                  ><q-item-section>Company career page</q-item-section></q-item
                >
                <q-item
                  v-if="props.row.company_url"
                  clickable
                  v-close-popup
                  tag="a"
                  :href="props.row.company_url"
                  target="_blank"
                  rel="noopener noreferrer"
                  ><q-item-section avatar
                    ><q-icon name="language" /></q-item-section
                  ><q-item-section>Company website</q-item-section></q-item
                >
                <q-separator />
                <q-item
                  clickable
                  v-close-popup
                  class="text-negative"
                  @click="deleteRow(props.row)"
                  ><q-item-section avatar
                    ><q-icon
                      name="delete_outline"
                      color="negative" /></q-item-section
                  ><q-item-section>Delete</q-item-section></q-item
                >
              </q-list>
            </q-menu>
            <q-tooltip>More actions</q-tooltip>
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
import type { Opportunity, OpportunityStatus } from "@/api/opportunities";
import {
  OPPORTUNITY_STATUS_COLORS,
  OPPORTUNITY_STATUS_LABELS
} from "@/modules/shared/statusColors";
import { formatOpportunityDate } from "../utils";

const props = defineProps<{
  rows: Opportunity[];
  loading: boolean;
  selectedRows: Opportunity[];
  statusOptions: { label: string; value: OpportunityStatus }[];
  updatingStatusIds: string[];
  viewOpportunity?: (opportunity: Opportunity) => void;
}>();

const emit = defineEmits<{
  (event: "update:selectedRows", value: Opportunity[]): void;
  (event: "view", opportunity: Opportunity): void;
  (event: "edit", opportunity: Opportunity): void;
  (event: "convert", opportunity: Opportunity): void;
  (event: "delete", opportunity: Opportunity): void;
  (
    event: "status-change",
    opportunity: Opportunity,
    status: OpportunityStatus
  ): void;
}>();

const selected = computed({
  get: () => props.selectedRows,
  set: value => emit("update:selectedRows", value)
});
const editingStatusId = ref<string | null>(null);
const pagination = ref({ page: 1, rowsPerPage: 10 });
const columns: QTableProps["columns"] = [
  {
    name: "title",
    required: true,
    label: "Role",
    align: "left",
    field: "title",
    sortable: true
  },
  {
    name: "company_name",
    label: "Company",
    align: "left",
    field: "company_name",
    sortable: true
  },
  {
    name: "status",
    label: "Status",
    align: "left",
    field: "status",
    sortable: true
  },
  {
    name: "job_location",
    label: "Location",
    align: "left",
    field: "job_location"
  },
  {
    name: "posted_on_utc",
    label: "Posted",
    align: "left",
    field: "posted_on_utc",
    sortable: true
  },
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

function statusLabel(status: OpportunityStatus) {
  return OPPORTUNITY_STATUS_LABELS[status];
}
function statusStyle(status: OpportunityStatus) {
  return { background: OPPORTUNITY_STATUS_COLORS[status], color: "#fff" };
}
function beginStatusEdit(opportunity: Opportunity) {
  editingStatusId.value = opportunity.id;
}
function viewRow(opportunity: Opportunity) {
  if (props.viewOpportunity) props.viewOpportunity(opportunity);
  else emit("view", opportunity);
}
function editRow(opportunity: Opportunity) {
  emit("edit", opportunity);
}
function convertRow(opportunity: Opportunity) {
  emit("convert", opportunity);
}
function deleteRow(opportunity: Opportunity) {
  emit("delete", opportunity);
}
function onStatusSelected(opportunity: Opportunity, status: OpportunityStatus) {
  editingStatusId.value = null;
  emit("status-change", opportunity, status);
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
.role-link {
  display: flex;
  width: 100%;
  max-width: 360px;
  flex-direction: column;
  align-items: flex-start;
  gap: 3px;
  padding: 0;
  border: 0;
  background: transparent;
  color: inherit;
  cursor: pointer;
  text-align: left;
}
.role-title {
  display: block;
  width: 100%;
  overflow: hidden;
  color: #102a43;
  font-size: 14px;
  font-weight: 700;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.role-link:hover .role-title {
  color: #1f6f8b;
  text-decoration: underline;
}
.role-source,
.date-cell {
  color: #829ab1;
  font-size: 11px;
}
.company-name {
  color: #334e68;
  font-weight: 600;
}
.location-cell {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: #627d98;
  font-size: 13px;
}
.date-cell {
  font-size: 13px;
  white-space: nowrap;
}
.status-cell {
  min-width: 140px;
  cursor: pointer;
}
.inline-status {
  min-width: 145px;
}
.status-chip {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
}
.actions-cell {
  white-space: nowrap;
}
:deep(.role-tooltip) {
  padding: 0;
  background: transparent;
  box-shadow: none;
}
.analysis-card {
  width: 310px;
  padding: 14px;
  border: 0;
  border-radius: 12px;
  background: #fff;
  box-shadow:
    0 18px 40px rgba(16, 42, 67, 0.24),
    0 4px 12px rgba(16, 42, 67, 0.14);
  color: #243b53;
}
.analysis-eyebrow {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  color: #829ab1;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.55px;
  text-transform: uppercase;
}
.analysis-eyebrow > span:first-child {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.analysis-status {
  padding: 3px 7px;
  border-radius: 999px;
  color: #fff;
  font-size: 9px;
  letter-spacing: 0;
  white-space: nowrap;
}
.analysis-title {
  margin-top: 10px;
  color: #102a43;
  font-size: 16px;
  font-weight: 750;
  line-height: 1.3;
}
.analysis-company {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-top: 5px;
  color: #627d98;
  font-size: 12px;
}
.analysis-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  margin-top: 13px;
  padding-top: 11px;
  border-top: 1px solid #edf2f5;
}
.analysis-grid div {
  display: flex;
  min-width: 0;
  flex-direction: column;
  gap: 3px;
}
.analysis-grid span {
  color: #9aaebe;
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 0.45px;
  text-transform: uppercase;
}
.analysis-grid strong {
  overflow: hidden;
  color: #334e68;
  font-size: 11px;
  font-weight: 600;
  text-overflow: ellipsis;
  white-space: nowrap;
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
  .table-footer {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
