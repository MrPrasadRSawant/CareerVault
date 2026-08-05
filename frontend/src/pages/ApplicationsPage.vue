<template>
  <q-page class="q-pa-md">
    <div class="row items-center justify-between q-mb-md">
      <div>
        <div class="text-h5">Applications</div>
        <div class="text-grey-7">Track the progress of every application.</div>
      </div>

      <q-btn
        color="primary"
        icon="add"
        label="New Application"
        :disable="opportunities.length === 0"
        @click="showCreateDialog = true"
      />
    </div>

    <q-card flat bordered>
      <q-table
        :rows="applications"
        :columns="columns"
        row-key="id"
        :loading="loading"
      >
        <template #body-cell-status="props">
          <q-td :props="props">
            <q-select
              v-model="props.row.status"
              :options="statusOptions"
              dense
              borderless
              emit-value
              map-options
              :color="statusColor(props.row.status)"
              @update:model-value="onStatusChange(props.row)"
            />
          </q-td>
        </template>

        <template #body-cell-applied_date="props">
          <q-td :props="props">
            {{ props.row.applied_date || "—" }}
          </q-td>
        </template>

        <template #body-cell-opportunity_title="props">
          <q-td :props="props">
            {{ opportunityTitle(props.row.opportunity_id) }}
          </q-td>
        </template>
      </q-table>
    </q-card>

    <q-dialog v-model="showCreateDialog">
      <q-card class="dialog-card">
        <q-card-section class="row items-center">
          <div class="text-h6">New Application</div>
          <q-space />
          <q-btn flat round dense icon="close" v-close-popup />
        </q-card-section>

        <q-card-section>
          <q-form @submit="onCreate" class="q-gutter-sm">
            <q-select
              v-model="form.opportunity_id"
              label="Opportunity *"
              filled
              :options="opportunityOptions"
              emit-value
              map-options
              :rules="[isRequired]"
            />
            <q-input
              v-model="form.applied_date"
              label="Applied date"
              filled
              type="date"
            />
            <q-input
              v-model="form.notes"
              label="Notes"
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
import { computed, onMounted, reactive, ref } from "vue";
import { useQuasar, type QTableProps } from "quasar";
import { applicationApi } from "@/api/applications";
import { opportunityApi } from "@/api/opportunities";
import type { Application, ApplicationStatus } from "@/api/applications";
import type { Opportunity } from "@/api/opportunities";

interface ApplicationRow extends Application {
  status: ApplicationStatus;
}

const $q = useQuasar();

const columns: QTableProps["columns"] = [
  {
    name: "opportunity_title",
    label: "Opportunity",
    align: "left",
    field: "opportunity_id"
  },
  {
    name: "status",
    label: "Status",
    align: "left",
    field: "status"
  },
  {
    name: "applied_date",
    label: "Applied on",
    align: "left",
    field: "applied_date"
  },
  {
    name: "notes",
    label: "Notes",
    align: "left",
    field: "notes"
  }
];

const applications = ref<ApplicationRow[]>([]);
const opportunities = ref<Opportunity[]>([]);
const loading = ref(false);
const creating = ref(false);
const showCreateDialog = ref(false);

const statusOptions = [
  { label: "Applied", value: "applied" },
  { label: "Screening", value: "screening" },
  { label: "Interview scheduled", value: "interview_scheduled" },
  { label: "Interview completed", value: "interview_completed" },
  { label: "Offer", value: "offer" },
  { label: "Rejected", value: "rejected" },
  { label: "Withdrawn", value: "withdrawn" }
];

const opportunityOptions = computed(() =>
  opportunities.value.map(o => ({ label: o.title, value: o.id }))
);

const form = reactive({
  opportunity_id: null as string | null,
  applied_date: "",
  notes: ""
});

function isRequired(value: string | null) {
  return value !== null || "This field is required";
}

function statusColor(status: ApplicationStatus): string {
  switch (status) {
    case "interview_scheduled":
    case "interview_completed":
      return "teal";
    case "offer":
      return "green";
    case "rejected":
      return "red";
    case "withdrawn":
      return "grey";
    default:
      return "blue";
  }
}

function opportunityTitle(opportunityId: string): string {
  return (
    opportunities.value.find(o => o.id === opportunityId)?.title ?? "Unknown"
  );
}

async function onRequest(): Promise<void> {
  loading.value = true;
  try {
    const [apps, opps] = await Promise.all([
      applicationApi.list(),
      opportunityApi.list()
    ]);
    applications.value = apps.map(app => ({ ...app, status: app.status }));
    opportunities.value = opps;
  } catch {
    $q.notify({ type: "negative", message: "Could not load applications" });
  } finally {
    loading.value = false;
  }
}

async function onCreate(): Promise<void> {
  creating.value = true;
  try {
    await applicationApi.create({
      opportunity_id: form.opportunity_id as string,
      applied_date: form.applied_date || null,
      notes: form.notes || null
    });
    $q.notify({ type: "positive", message: "Application recorded" });
    showCreateDialog.value = false;
    Object.assign(form, { opportunity_id: null, applied_date: "", notes: "" });
    await onRequest();
  } catch {
    $q.notify({ type: "negative", message: "Could not create application" });
  } finally {
    creating.value = false;
  }
}

async function onStatusChange(row: ApplicationRow): Promise<void> {
  try {
    await applicationApi.updateStatus(row.id, row.status);
    $q.notify({ type: "positive", message: `Status updated to ${row.status}` });
  } catch {
    $q.notify({ type: "negative", message: "Could not update status" });
    await onRequest();
  }
}

onMounted(onRequest);
</script>

<style lang="scss" scoped>
.dialog-card {
  width: 100%;
  max-width: 520px;
}
</style>
