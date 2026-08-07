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
      no-data-label="No cover letters match these filters"
    >
      <template #body-cell-name="props">
        <q-td :props="props">
          <button
            class="letter-title ellipsis"
            type="button"
            @click="$emit('view', props.row)"
          >
            <q-icon name="article" class="q-mr-sm" color="primary" />{{
              props.row.name
            }}
          </button>
          <q-tooltip
            class="letter-tooltip"
            :offset="[0, 8]"
            style="
              padding: 0;
              overflow: visible;
              background: transparent;
              box-shadow: none;
            "
          >
            <div class="analysis-card">
              <div class="analysis-kicker">
                <q-icon name="insights" /> COVER LETTER SNAPSHOT
              </div>
              <div class="analysis-title">{{ props.row.name }}</div>
              <div class="analysis-file">
                <q-icon name="insert_drive_file" />
                {{ props.row.file_name || "Text letter" }}
              </div>
              <q-separator class="q-my-sm" />
              <div class="analysis-grid">
                <div>
                  <span>HAS CONTENT</span>
                  <strong>{{ props.row.content ? "Yes" : "No" }}</strong>
                </div>
                <div>
                  <span>CREATED</span>
                  <strong>{{
                    new Date(props.row.created_at).toLocaleDateString()
                  }}</strong>
                </div>
              </div>
              <div v-if="props.row.content" class="analysis-preview">
                {{ contentPreview(props.row.content) }}
              </div>
            </div>
          </q-tooltip>
        </q-td>
      </template>
      <template #body-cell-file_name="props">
        <q-td :props="props">
          <span class="cell-text">{{
            props.row.file_name || "—"
          }}</span>
        </q-td>
      </template>
      <template #body-cell-content_preview="props">
        <q-td :props="props">
          <span class="ellipsis cell-text">{{
            contentPreview(props.row.content) || "—"
          }}</span>
        </q-td>
      </template>
      <template #body-cell-created_at="props">
        <q-td :props="props">{{
          formatDate(props.row.created_at)
        }}</q-td>
      </template>
      <template #body-cell-actions="props">
        <q-td :props="props" class="actions-cell">
          <q-btn
            flat
            round
            dense
            icon="visibility"
            color="primary"
            :disable="!props.row.content"
            @click="$emit('view', props.row)"
          >
            <q-tooltip>View letter</q-tooltip>
          </q-btn>
          <q-btn
            flat
            round
            dense
            icon="more_vert"
            color="primary"
            aria-label="More cover letter actions"
          >
            <q-menu anchor="bottom right" self="top right">
              <q-list dense style="min-width: 190px">
                <q-item
                  v-close-popup
                  clickable
                  :disable="!props.row.content"
                  @click="$emit('view', props.row)"
                >
                  <q-item-section avatar
                    ><q-icon name="visibility"
                  /></q-item-section>
                  <q-item-section>View letter</q-item-section>
                </q-item>
                <q-item
                  v-close-popup
                  clickable
                  @click="$emit('edit', props.row)"
                >
                  <q-item-section avatar
                    ><q-icon name="edit"
                  /></q-item-section>
                  <q-item-section>Edit letter</q-item-section>
                </q-item>
                <q-separator />
                <q-item
                  v-close-popup
                  clickable
                  class="text-negative"
                  @click="$emit('delete', props.row)"
                >
                  <q-item-section avatar
                    ><q-icon name="delete" color="negative"
                  /></q-item-section>
                  <q-item-section>Delete letter</q-item-section>
                </q-item>
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
import type { CoverLetterRow } from "../types";
import { contentPreview } from "../utils";

const props = defineProps<{
  rows: CoverLetterRow[];
  loading: boolean;
}>();
defineEmits<{
  (event: "view", row: CoverLetterRow): void;
  (event: "edit", row: CoverLetterRow): void;
  (event: "delete", row: CoverLetterRow): void;
}>();

const pagination = ref({ page: 1, rowsPerPage: 10 });
const columns: QTableProps["columns"] = [
  {
    name: "name",
    label: "Name",
    align: "left",
    field: "name",
    sortable: true
  },
  {
    name: "file_name",
    label: "File",
    align: "left",
    field: "file_name"
  },
  {
    name: "content_preview",
    label: "Content",
    align: "left",
    field: row => contentPreview(row.content)
  },
  {
    name: "created_at",
    label: "Created",
    align: "left",
    field: "created_at"
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

function formatDate(value: string) {
  return value ? new Date(value).toLocaleDateString() : "—";
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
.letter-title {
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
.letter-title:hover {
  text-decoration: underline;
}
.cell-text {
  color: var(--cv-text-strong);
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
.analysis-preview {
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
