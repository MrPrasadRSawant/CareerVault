<template>
  <div class="resume-toolbar">
    <div class="page-header">
      <div
        ><div class="page-title">Resumes</div
        ><div class="page-subtitle"
          >Keep tailored resume versions ready for every application and
          interview.</div
        ></div
      >
      <div class="page-actions"
        ><q-btn
          unelevated
          no-caps
          color="primary"
          icon="upload_file"
          label="Upload resume"
          @click="$emit('upload')"
        /><q-btn
          flat
          round
          dense
          icon="more_vert"
          aria-label="More resume actions"
          ><q-menu anchor="bottom right" self="top right"
            ><q-list dense style="min-width: 190px"
              ><q-item v-close-popup clickable @click="$emit('export')"
                ><q-item-section avatar
                  ><q-icon name="file_download" /></q-item-section
                ><q-item-section>Export CSV</q-item-section></q-item
              ><q-item v-close-popup clickable @click="$emit('refresh')"
                ><q-item-section avatar
                  ><q-icon name="refresh" /></q-item-section
                ><q-item-section>Refresh data</q-item-section></q-item
              ></q-list
            ></q-menu
          ><q-tooltip>More actions</q-tooltip></q-btn
        ></div
      >
    </div>
  </div>
</template>

<script setup lang="ts">
defineEmits<{
  (event: "upload"): void;
  (event: "export"): void;
  (event: "refresh"): void;
}>();
</script>

<style lang="scss" scoped>
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
.page-title {
  color: #102a43;
  font-size: 26px;
  font-weight: 750;
  letter-spacing: -0.4px;
}
.page-subtitle {
  margin-top: 4px;
  color: #627d98;
  font-size: 14px;
}
.page-actions {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}
@media (max-width: 700px) {
  .page-actions {
    width: 100%;
  }
  .page-actions .q-btn {
    flex: 1;
  }
}
</style>
