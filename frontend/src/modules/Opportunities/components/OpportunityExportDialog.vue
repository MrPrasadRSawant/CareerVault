<template>
  <q-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <q-card class="export-dialog">
      <q-card-section class="dialog-header">
        <div
          ><div class="dialog-title">Export opportunities</div
          ><div class="dialog-subtitle"
            >Choose columns for the {{ rowCount }} opportunities matching your
            current filters.</div
          ></div
        >
        <q-btn flat round dense icon="close" v-close-popup />
      </q-card-section>
      <q-card-section>
        <div class="column-grid">
          <q-checkbox
            v-for="column in columns"
            :key="column.key"
            v-model="selectedColumns"
            :val="column.key"
            :label="column.label"
          />
        </div>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat no-caps label="Cancel" v-close-popup />
        <q-btn
          unelevated
          no-caps
          color="primary"
          icon="download"
          label="Export CSV"
          :disable="selectedColumns.length === 0"
          @click="exportCsv"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { opportunityExportColumns } from "../utils";
import type { OpportunityExportColumnKey } from "../types";

const props = defineProps<{ modelValue: boolean; rowCount: number }>();
const emit = defineEmits<{
  (event: "update:modelValue", value: boolean): void;
  (event: "export", columns: OpportunityExportColumnKey[]): void;
}>();
const columns = opportunityExportColumns;
const selectedColumns = ref<OpportunityExportColumnKey[]>([
  "title",
  "company_name",
  "status",
  "job_location",
  "posted_on_utc"
]);
watch(
  () => props.modelValue,
  open => {
    if (open)
      selectedColumns.value = [
        "title",
        "company_name",
        "status",
        "job_location",
        "posted_on_utc"
      ];
  }
);
function exportCsv() {
  emit("export", selectedColumns.value);
}
</script>

<style lang="scss" scoped>
.export-dialog {
  width: min(620px, 94vw);
  max-width: 620px;
}
.dialog-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  border-bottom: 1px solid #edf2f5;
}
.dialog-title {
  color: #102a43;
  font-size: 20px;
  font-weight: 750;
}
.dialog-subtitle {
  margin-top: 4px;
  color: #829ab1;
  font-size: 12px;
}
.column-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px 16px;
}
@media (max-width: 500px) {
  .column-grid {
    grid-template-columns: 1fr;
  }
}
</style>
