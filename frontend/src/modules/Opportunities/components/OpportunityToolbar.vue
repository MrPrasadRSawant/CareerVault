<template>
  <div class="opportunity-toolbar">
    <div class="page-header">
      <div>
        <div class="page-title">Opportunities</div>
        <div class="page-subtitle">
          Your opportunity inbox—from scraped leads to roles ready to apply for.
        </div>
      </div>
      <div class="page-actions">
        <q-btn unelevated no-caps color="primary" icon="add" label="New opportunity" @click="$emit('create')" />
        <q-btn flat round dense icon="more_vert" aria-label="More opportunity actions">
          <q-menu anchor="bottom right" self="top right">
            <q-list dense style="min-width: 190px">
              <q-item clickable v-close-popup @click="emit('export')">
                <q-item-section avatar><q-icon name="ios_share" /></q-item-section>
                <q-item-section>Export CSV</q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="emit('template')">
                <q-item-section avatar><q-icon name="description" /></q-item-section>
                <q-item-section>Download CSV template</q-item-section>
              </q-item>
              <q-item clickable v-close-popup :disable="importing" @click="fileInput?.click()">
                <q-item-section avatar>
                  <q-spinner v-if="importing" color="primary" size="18px" />
                  <q-icon v-else name="upload_file" />
                </q-item-section>
                <q-item-section>Import CSV</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
          <q-tooltip>More actions</q-tooltip>
        </q-btn>
        <input ref="fileInput" type="file" accept=".csv,text/csv" hidden @change="onFileSelected" />
      </div>
    </div>
    <div v-if="selectedCount" class="selection-toolbar">
      <span><strong>{{ selectedCount }}</strong> selected</span>
      <q-btn flat no-caps color="negative" icon="delete_outline" label="Delete selected" @click="$emit('bulk-delete')" />
      <q-btn flat no-caps label="Clear selection" @click="$emit('clear-selection')" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

defineProps<{
  importing: boolean;
  selectedCount: number;
}>();

const emit = defineEmits<{
  (event: "create"): void;
  (event: "template"): void;
  (event: "export"): void;
  (event: "bulk-delete"): void;
  (event: "clear-selection"): void;
  (event: "import", file: File): void;
}>();

const fileInput = ref<HTMLInputElement | null>(null);

function onFileSelected(event: Event) {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0];
  if (file) emit("import", file);
  input.value = "";
}
</script>

<style lang="scss" scoped>
.page-header, .selection-toolbar { display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
.page-header { margin-bottom: 16px; }
.page-title { color: #102a43; font-size: 26px; font-weight: 750; letter-spacing: -0.4px; }
.page-subtitle { margin-top: 4px; color: #627d98; font-size: 14px; }
.page-actions { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.selection-toolbar { justify-content: flex-start; margin-bottom: 14px; padding: 8px 12px; border: 1px solid #f4c7c3; border-radius: 9px; background: #fff8f7; color: #8b3a35; font-size: 13px; }
@media (max-width: 700px) {
  .page-actions { width: 100%; }
  .page-actions .q-btn { flex: 1; }
}
</style>
