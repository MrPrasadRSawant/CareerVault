<template>
  <q-page class="q-pa-md">
    <div class="row items-center justify-between q-mb-md">
      <div>
        <div class="text-h5">Companies</div>
        <div class="text-grey-7"
          >Keep track of employers in your job search.</div
        >
      </div>

      <q-btn
        color="primary"
        icon="add"
        label="New Company"
        @click="openCreate"
      />
    </div>

    <q-card flat bordered>
      <q-table
        :rows="companies"
        :columns="columns"
        row-key="id"
        :loading="loading"
        no-data-label="No companies yet — add your first one."
      >
        <template #body-cell-name="props">
          <q-td :props="props">
            <q-icon name="business" class="q-mr-sm" color="primary" />
            {{ props.row.name }}
          </q-td>
        </template>

        <template #body-cell-website="props">
          <q-td :props="props">
            <a
              v-if="props.row.website"
              :href="websiteHref(props.row.website)"
              target="_blank"
              rel="noopener"
              class="website-link"
            >
              {{ props.row.website }}
            </a>
            <span v-else>—</span>
          </q-td>
        </template>

        <template #body-cell-created_at="props">
          <q-td :props="props">{{ formatDate(props.row.created_at) }}</q-td>
        </template>

        <template #body-cell-actions="props">
          <q-td :props="props" class="text-right">
            <q-btn
              flat
              round
              dense
              color="primary"
              icon="edit"
              @click="openEdit(props.row)"
            >
              <q-tooltip>Edit company</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              dense
              color="negative"
              icon="delete"
              @click="onDelete(props.row)"
            >
              <q-tooltip>Delete company</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>
    </q-card>

    <q-dialog v-model="showDialog">
      <q-card class="dialog-card">
        <q-card-section class="row items-center">
          <div class="text-h6">{{
            editing ? "Edit Company" : "New Company"
          }}</div>
          <q-space />
          <q-btn flat round dense icon="close" v-close-popup />
        </q-card-section>

        <q-card-section>
          <q-form @submit="onSave" class="q-gutter-sm">
            <q-input
              v-model="form.name"
              label="Name *"
              filled
              :rules="[isRequired]"
            />
            <q-input
              v-model="form.website"
              label="Website"
              filled
              placeholder="https://example.com"
            />
            <div class="row q-col-gutter-sm">
              <q-input
                class="col-6"
                v-model="form.industry"
                label="Industry"
                filled
              />
              <q-input
                class="col-6"
                v-model="form.location"
                label="Location"
                filled
              />
            </div>
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
                :loading="saving"
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
import { companyApi } from "@/api/companies";
import type { Company } from "@/api/companies";

interface CompanyForm {
  name: string;
  website: string;
  industry: string;
  location: string;
  notes: string;
}

const emptyForm = (): CompanyForm => ({
  name: "",
  website: "",
  industry: "",
  location: "",
  notes: ""
});

const $q = useQuasar();

const columns: QTableProps["columns"] = [
  { name: "name", label: "Name", align: "left", field: "name", sortable: true },
  {
    name: "industry",
    label: "Industry",
    align: "left",
    field: "industry"
  },
  { name: "location", label: "Location", align: "left", field: "location" },
  { name: "website", label: "Website", align: "left", field: "website" },
  {
    name: "created_at",
    label: "Added",
    align: "left",
    field: "created_at"
  },
  { name: "actions", label: "", align: "right", field: "actions" }
];

const companies = ref<Company[]>([]);
const loading = ref(false);
const saving = ref(false);
const showDialog = ref(false);
const editing = ref<string | null>(null);
const form = reactive<CompanyForm>(emptyForm());

function isRequired(value: string | null) {
  return (value ?? "").trim().length > 0 || "This field is required";
}

function websiteHref(website: string): string {
  return /^https?:\/\//i.test(website) ? website : `https://${website}`;
}

function formatDate(value: string): string {
  return new Date(value).toLocaleDateString();
}

function resetForm() {
  Object.assign(form, emptyForm());
}

function openCreate() {
  editing.value = null;
  resetForm();
  showDialog.value = true;
}

function openEdit(company: Company) {
  editing.value = company.id;
  Object.assign(form, {
    name: company.name,
    website: company.website ?? "",
    industry: company.industry ?? "",
    location: company.location ?? "",
    notes: company.notes ?? ""
  });
  showDialog.value = true;
}

async function onRequest(): Promise<void> {
  loading.value = true;
  try {
    companies.value = await companyApi.list();
  } catch {
    $q.notify({ type: "negative", message: "Could not load companies" });
  } finally {
    loading.value = false;
  }
}

async function onSave(): Promise<void> {
  saving.value = true;
  try {
    const payload = {
      name: form.name,
      website: form.website.trim() || null,
      industry: form.industry.trim() || null,
      location: form.location.trim() || null,
      notes: form.notes.trim() || null
    };
    if (editing.value !== null) {
      await companyApi.update(editing.value, payload);
      $q.notify({ type: "positive", message: "Company updated" });
    } else {
      await companyApi.create(payload);
      $q.notify({ type: "positive", message: "Company added" });
    }
    showDialog.value = false;
    await onRequest();
  } catch {
    $q.notify({ type: "negative", message: "Could not save company" });
  } finally {
    saving.value = false;
  }
}

async function onDelete(company: Company): Promise<void> {
  $q.dialog({
    title: "Delete company",
    message: `Delete "${company.name}"? This cannot be undone.`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await companyApi.remove(company.id);
      $q.notify({ type: "positive", message: "Company deleted" });
      await onRequest();
    } catch {
      $q.notify({ type: "negative", message: "Could not delete company" });
    }
  });
}

onMounted(onRequest);
</script>

<style lang="scss" scoped>
.dialog-card {
  width: 100%;
  max-width: 520px;
}

.website-link {
  color: #219ebc;
  text-decoration: none;

  &:hover {
    text-decoration: underline;
  }
}
</style>
