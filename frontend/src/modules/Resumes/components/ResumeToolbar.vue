<template>
  <div class="resume-toolbar row items-center justify-between q-mb-md">
    <div><div class="page-title">Resumes</div><div class="page-subtitle">Keep tailored resume versions ready for every application and interview.</div></div>
    <div class="row items-center q-gutter-sm"><q-btn color="primary" icon="upload_file" label="Upload resume" @click="$emit('upload')" /><q-btn flat round dense icon="more_vert" aria-label="More resume actions"><q-menu anchor="bottom right" self="top right"><q-list dense style="min-width: 190px"><q-item v-close-popup clickable @click="$emit('export')"><q-item-section avatar><q-icon name="file_download" /></q-item-section><q-item-section>Export CSV</q-item-section></q-item><q-item v-close-popup clickable @click="$emit('refresh')"><q-item-section avatar><q-icon name="refresh" /></q-item-section><q-item-section>Refresh data</q-item-section></q-item></q-list></q-menu></q-btn></div>
  </div>
</template>

<script setup lang="ts">
defineEmits<{ (event: "upload"): void; (event: "export"): void; (event: "refresh"): void }>();
</script>

<style lang="scss" scoped>
.page-title { color: var(--cv-navy); font-size: 28px; font-weight: 800; }
.page-subtitle { margin-top: 3px; color: var(--cv-muted); font-size: 14px; }
@media (max-width: 600px) { .resume-toolbar { align-items: flex-start; gap: 14px; flex-direction: column; } }
</style>

