<template>
  <q-page class="q-pa-md">
    <div class="row items-center justify-between q-mb-md">
      <div>
        <div class="text-h5">Cover Letters</div>
        <div class="text-grey-7"
          >Draft and keep your tailored letters handy.</div
        >
      </div>

      <q-btn
        color="primary"
        icon="add"
        label="New Letter"
        @click="openCreate"
      />
    </div>

    <q-card flat bordered>
      <q-table
        :rows="letters"
        :columns="columns"
        row-key="id"
        :loading="loading"
        no-data-label="No cover letters yet — create your first one."
      >
        <template #body-cell-name="props">
          <q-td :props="props">
            <q-icon name="article" class="q-mr-sm" color="primary" />
            {{ props.row.name }}
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
              icon="visibility"
              :disable="!props.row.content"
              @click="openView(props.row)"
            >
              <q-tooltip>View letter</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              dense
              color="primary"
              icon="edit"
              @click="openEdit(props.row)"
            >
              <q-tooltip>Edit letter</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              dense
              color="negative"
              icon="delete"
              @click="onDelete(props.row)"
            >
              <q-tooltip>Delete letter</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>
    </q-card>

    <q-dialog v-model="showDialog">
      <q-card class="dialog-card">
        <q-card-section class="row items-center">
          <div class="text-h6">
            {{ editing ? "Edit Letter" : "New Letter" }}
          </div>
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
              v-model="form.content"
              label="Content"
              filled
              type="textarea"
              autogrow
              class="letter-input"
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

    <q-dialog v-model="showViewDialog">
      <q-card class="dialog-card view-card">
        <q-card-section class="row items-center">
          <div class="text-h6">{{ viewing?.name }}</div>
          <q-space />
          <q-btn flat round dense icon="close" v-close-popup />
        </q-card-section>

        <q-card-section class="view-content">
          <p v-if="viewing?.content" class="letter-content">
            {{ viewing.content }}
          </p>
          <p v-else class="text-grey-6">This letter has no content yet.</p>
        </q-card-section>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { useQuasar, type QTableProps } from "quasar";
import { coverLetterApi } from "@/api/coverLetters";
import type { CoverLetter } from "@/api/coverLetters";

interface LetterForm {
  name: string;
  content: string;
}

const emptyForm = (): LetterForm => ({ name: "", content: "" });

const $q = useQuasar();

const columns: QTableProps["columns"] = [
  { name: "name", label: "Name", align: "left", field: "name", sortable: true },
  {
    name: "created_at",
    label: "Created",
    align: "left",
    field: "created_at"
  },
  { name: "actions", label: "", align: "right", field: "actions" }
];

const letters = ref<CoverLetter[]>([]);
const loading = ref(false);
const saving = ref(false);
const showDialog = ref(false);
const showViewDialog = ref(false);
const editing = ref<string | null>(null);
const viewing = ref<CoverLetter | null>(null);
const form = reactive<LetterForm>(emptyForm());

function isRequired(value: string | null) {
  return (value ?? "").trim().length > 0 || "This field is required";
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

function openEdit(letter: CoverLetter) {
  editing.value = letter.id;
  Object.assign(form, { name: letter.name, content: letter.content ?? "" });
  showDialog.value = true;
}

function openView(letter: CoverLetter) {
  viewing.value = letter;
  showViewDialog.value = true;
}

async function onRequest(): Promise<void> {
  loading.value = true;
  try {
    letters.value = await coverLetterApi.list();
  } catch {
    $q.notify({ type: "negative", message: "Could not load cover letters" });
  } finally {
    loading.value = false;
  }
}

async function onSave(): Promise<void> {
  saving.value = true;
  try {
    const payload = {
      name: form.name,
      content: form.content.trim() || null
    };
    if (editing.value !== null) {
      await coverLetterApi.update(editing.value, payload);
      $q.notify({ type: "positive", message: "Letter updated" });
    } else {
      await coverLetterApi.create(payload);
      $q.notify({ type: "positive", message: "Letter created" });
    }
    showDialog.value = false;
    await onRequest();
  } catch {
    $q.notify({ type: "negative", message: "Could not save letter" });
  } finally {
    saving.value = false;
  }
}

async function onDelete(letter: CoverLetter): Promise<void> {
  $q.dialog({
    title: "Delete letter",
    message: `Delete "${letter.name}"? This cannot be undone.`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await coverLetterApi.remove(letter.id);
      $q.notify({ type: "positive", message: "Letter deleted" });
      await onRequest();
    } catch {
      $q.notify({ type: "negative", message: "Could not delete letter" });
    }
  });
}

onMounted(onRequest);
</script>

<style lang="scss" scoped>
.dialog-card {
  width: 100%;
  max-width: 560px;
}

.letter-input :deep(.q-field__native) {
  min-height: 160px;
  font-family: inherit;
  line-height: 1.6;
}

.letter-content {
  white-space: pre-wrap;
  line-height: 1.7;
  margin: 0;
  color: #334e5a;
}
</style>
