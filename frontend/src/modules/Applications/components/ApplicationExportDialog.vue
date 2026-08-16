<template>
  <q-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <q-card class="export-card">
      <q-card-section class="row items-start"
        ><div
          ><div class="text-h6">Export applications</div
          ><div class="text-caption text-grey-7"
            >Choose columns for {{ rowCount }} filtered records.</div
          ></div
        ><q-space /><q-btn flat round dense icon="close" v-close-popup
      /></q-card-section>
      <q-card-section
        ><div class="column-grid"
          ><q-checkbox
            v-for="column in columns"
            :key="column.key"
            v-model="selected"
            :val="column.key"
            :label="column.label" /></div
      ></q-card-section>
      <q-card-actions align="right"
        ><q-btn flat label="Cancel" v-close-popup /><q-btn
          unelevated
          color="primary"
          icon="file_download"
          label="Export CSV"
          :disable="selected.length === 0"
          @click="$emit('export', selected)"
      /></q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import { applicationExportColumns } from "../utils";
import type { ApplicationExportColumnKey } from "../types";
const props = defineProps<{ modelValue: boolean; rowCount: number }>();
defineEmits<{
  (event: "update:modelValue", value: boolean): void;
  (event: "export", columns: ApplicationExportColumnKey[]): void;
}>();
const columns = applicationExportColumns;
const selected = ref<ApplicationExportColumnKey[]>([
  "opportunity",
  "company",
  "status",
  "applied_date"
]);
watch(
  () => props.modelValue,
  open => {
    if (open)
      selected.value = ["opportunity", "company", "status", "applied_date"];
  }
);
</script>

<style lang="scss" scoped>
.export-card {
  width: min(620px, 94vw);
}
.column-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px 16px;
}
@media (max-width: 500px) {
  .column-grid {
    grid-template-columns: 1fr;
  }
}
</style>
