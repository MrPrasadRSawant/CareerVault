<template>
  <q-page class="q-pa-md">
    <div class="row items-center justify-between q-mb-md">
      <div>
        <div class="text-h5">Resumes</div>
        <div class="text-grey-7"> Upload and manage your resume versions. </div>
      </div>

      <q-btn
        color="primary"
        icon="upload_file"
        label="Upload Resume"
        @click="fileInput?.click()"
      />
      <input
        ref="fileInput"
        type="file"
        accept=".pdf,.doc,.docx,.txt,.md"
        class="hidden"
        @change="onFileSelected"
      />
    </div>

    <q-card flat bordered>
      <q-table
        :rows="resumes"
        :columns="columns"
        row-key="id"
        :loading="loading"
      >
        <template #body-cell-name="props">
          <q-td :props="props">
            <q-icon name="description" class="q-mr-sm" color="primary" />
            {{ props.row.name }}
            <q-badge
              v-if="props.row.is_active"
              class="q-ml-sm"
              color="green"
              label="active"
            />
          </q-td>
        </template>

        <template #body-cell-file_size="props">
          <q-td :props="props">
            {{ formatSize(props.row.file_size) }}
          </q-td>
        </template>

        <template #body-cell-actions="props">
          <q-td :props="props" class="text-right">
            <q-btn
              flat
              round
              dense
              color="primary"
              icon="star"
              :disable="props.row.is_active"
              @click="onSetActive(props.row)"
            >
              <q-tooltip>Set as active resume</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              dense
              color="negative"
              icon="delete"
              @click="onDelete(props.row.id)"
            >
              <q-tooltip>Delete resume</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useQuasar, type QTableProps } from "quasar";
import { resumeApi } from "@/api/resumes";
import type { Resume } from "@/api/resumes";

const $q = useQuasar();

const columns: QTableProps["columns"] = [
  {
    name: "name",
    label: "Name",
    align: "left",
    field: "name"
  },
  {
    name: "version",
    label: "Version",
    align: "left",
    field: "version"
  },
  {
    name: "file_size",
    label: "Size",
    align: "left",
    field: "file_size"
  },
  {
    name: "created_at",
    label: "Uploaded",
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

const resumes = ref<Resume[]>([]);
const loading = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);

function formatSize(bytes: number | null): string {
  if (bytes === null || bytes === undefined) {
    return "—";
  }
  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`;
  }
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

async function onRequest(): Promise<void> {
  loading.value = true;
  try {
    resumes.value = await resumeApi.list();
  } catch {
    $q.notify({ type: "negative", message: "Could not load resumes" });
  } finally {
    loading.value = false;
  }
}

async function onFileSelected(event: Event): Promise<void> {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0];
  if (file === undefined) {
    return;
  }

  try {
    await resumeApi.upload(file, file.name);
    $q.notify({ type: "positive", message: "Resume uploaded" });
    await onRequest();
  } catch {
    $q.notify({ type: "negative", message: "Could not upload resume" });
  } finally {
    input.value = "";
  }
}

async function onSetActive(resume: Resume): Promise<void> {
  try {
    await resumeApi.update(resume.id, { is_active: true });
    $q.notify({ type: "positive", message: `${resume.name} is now active` });
    await onRequest();
  } catch {
    $q.notify({ type: "negative", message: "Could not update resume" });
  }
}

async function onDelete(id: string): Promise<void> {
  try {
    await resumeApi.remove(id);
    $q.notify({ type: "positive", message: "Resume deleted" });
    await onRequest();
  } catch {
    $q.notify({ type: "negative", message: "Could not delete resume" });
  }
}

onMounted(onRequest);
</script>
