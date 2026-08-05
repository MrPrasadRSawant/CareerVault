<template>
  <q-page class="opportunities-page">
    <div class="page-header">
      <div>
        <div class="page-title">Opportunities</div>
        <div class="page-subtitle">
          Track job opportunities you've saved from anywhere.
        </div>
      </div>

      <q-btn
        unelevated
        no-caps
        color="primary"
        icon="add"
        label="New Opportunity"
        @click="showCreateDialog = true"
      />
    </div>

    <div class="panel-card">
      <q-table
        :rows="opportunities"
        :columns="columns"
        row-key="id"
        :loading="loading"
        :filter="filter"
        :rows-per-page-options="[10, 25, 50]"
        @request="onRequest"
      >
        <template #top-right>
          <q-input
            v-model="filter"
            dense
            debounce="300"
            placeholder="Search"
            clearable
            outlined
            rounded
          >
            <template #append>
              <q-icon name="search" />
            </template>
          </q-input>
        </template>

        <template #body-cell-status="props">
          <q-td :props="props">
            <span
              class="status-chip"
              :style="{ background: statusColor(props.row.status) }"
            >
              {{ statusLabel(props.row.status) }}
            </span>
          </q-td>
        </template>

        <template #body-cell-salary_range="props">
          <q-td :props="props">
            {{ props.row.salary_range || "—" }}
          </q-td>
        </template>

        <template #body-cell-created_at="props">
          <q-td :props="props">
            {{ formatDate(props.row.created_at) }}
          </q-td>
        </template>

        <template #body-cell-actions="props">
          <q-td :props="props" class="text-right">
            <q-btn
              flat
              round
              dense
              color="negative"
              icon="delete"
              :disable="loading"
              @click="onDelete(props.row.id)"
            >
              <q-tooltip>Delete opportunity</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>
    </div>

    <q-dialog v-model="showCreateDialog">
      <q-card class="dialog-card">
        <q-card-section class="row items-center">
          <div class="text-h6">New Opportunity</div>
          <q-space />
          <q-btn flat round dense icon="close" v-close-popup />
        </q-card-section>

        <q-card-section>
          <q-form @submit="onCreate" class="q-gutter-sm">
            <q-input
              v-model="form.title"
              label="Job title *"
              filled
              :rules="[isRequired]"
            />
            <q-input
              v-model="form.salary_range"
              label="Salary range"
              filled
              placeholder="e.g. 100k-130k"
            />
            <q-input
              v-model="form.application_link"
              label="Application link"
              filled
              type="url"
            />
            <q-select
              v-model="form.status"
              label="Status"
              filled
              :options="statusOptions"
              emit-value
              map-options
            />
            <q-input
              v-model="form.required_skills"
              label="Required skills (comma separated)"
              filled
            />
            <q-input
              v-model="form.description"
              label="Job description"
              filled
              type="textarea"
              autogrow
            />

            <div class="row justify-end q-gutter-sm q-mt-sm">
              <q-btn label="Cancel" flat color="primary" v-close-popup />
              <q-btn
                label="Save"
                type="submit"
                color="primary"
                :loading="creating"
              />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { useQuasar, type QTableProps } from "quasar";
import { opportunityApi } from "@/api/opportunities";
import type { Opportunity, OpportunityStatus } from "@/api/opportunities";
import {
  OPPORTUNITY_STATUS_COLORS,
  OPPORTUNITY_STATUS_LABELS
} from "@/modules/shared/statusColors";

interface OpportunityRow {
  id: string;
  title: string;
  status: OpportunityStatus;
  salary_range: string | null;
  created_at: string;
}

const $q = useQuasar();

const columns: QTableProps["columns"] = [
  {
    name: "title",
    required: true,
    label: "Title",
    align: "left",
    field: "title",
    sortable: true
  },
  {
    name: "status",
    label: "Status",
    align: "left",
    field: "status"
  },
  {
    name: "salary_range",
    label: "Salary",
    align: "left",
    field: "salary_range"
  },
  {
    name: "created_at",
    label: "Created",
    align: "left",
    field: "created_at"
  },
  {
    name: "actions",
    label: "",
    align: "right",
    field: "actions"
  }
];

const opportunities = ref<OpportunityRow[]>([]);
const loading = ref(false);
const creating = ref(false);
const filter = ref("");
const showCreateDialog = ref(false);

const statusOptions = [
  { label: "Saved", value: "saved" },
  { label: "Applied", value: "applied" },
  { label: "Interviewing", value: "interviewing" },
  { label: "Offered", value: "offered" },
  { label: "Rejected", value: "rejected" },
  { label: "Archived", value: "archived" }
];

const form = reactive({
  title: "",
  salary_range: "",
  application_link: "",
  status: "saved" as OpportunityStatus,
  required_skills: "",
  description: ""
});

function isRequired(value: string | null) {
  return (value ?? "").trim().length > 0 || "This field is required";
}

function statusColor(status: OpportunityStatus): string {
  return OPPORTUNITY_STATUS_COLORS[status];
}

function statusLabel(status: OpportunityStatus): string {
  return OPPORTUNITY_STATUS_LABELS[status];
}

function formatDate(value: string): string {
  return new Date(value).toLocaleDateString();
}

async function onRequest(): Promise<void> {
  loading.value = true;
  try {
    const rows = await opportunityApi.list();
    opportunities.value = rows.map(row => ({
      id: row.id,
      title: row.title,
      status: row.status,
      salary_range: row.salary_range,
      created_at: row.created_at
    }));
  } catch {
    $q.notify({ type: "negative", message: "Could not load opportunities" });
  } finally {
    loading.value = false;
  }
}

async function onCreate(): Promise<void> {
  creating.value = true;
  try {
    const skills = form.required_skills
      .split(",")
      .map(s => s.trim())
      .filter(Boolean);

    await opportunityApi.create({
      title: form.title,
      salary_range: form.salary_range || null,
      application_link: form.application_link || null,
      status: form.status,
      required_skills: skills.length > 0 ? skills : null,
      description: form.description || null
    });

    $q.notify({ type: "positive", message: "Opportunity saved" });
    showCreateDialog.value = false;
    Object.assign(form, {
      title: "",
      salary_range: "",
      application_link: "",
      status: "saved",
      required_skills: "",
      description: ""
    });
    await onRequest();
  } catch {
    $q.notify({ type: "negative", message: "Could not create opportunity" });
  } finally {
    creating.value = false;
  }
}

async function onDelete(id: string): Promise<void> {
  try {
    await opportunityApi.remove(id);
    $q.notify({ type: "positive", message: "Opportunity deleted" });
    await onRequest();
  } catch {
    $q.notify({ type: "negative", message: "Could not delete opportunity" });
  }
}

onMounted(onRequest);
</script>

<style lang="scss" scoped>
.opportunities-page {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #023047;
  letter-spacing: -0.3px;
}

.page-subtitle {
  margin-top: 4px;
  font-size: 14px;
  color: #64748b;
}

.panel-card {
  background: #fff;
  border: 1px solid #e6edf1;
  border-radius: 14px;
  padding: 8px;
  box-shadow: 0 1px 3px rgba(2, 48, 71, 0.06);
}

.status-chip {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  color: #fff;
}

.dialog-card {
  width: 100%;
  max-width: 520px;
}
</style>
