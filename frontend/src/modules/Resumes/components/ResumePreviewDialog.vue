<template>
  <q-dialog :model-value="modelValue" maximized @update:model-value="$emit('update:modelValue', $event)">
    <q-card class="preview-card">
      <q-card-section class="preview-header row items-center"><div><div class="preview-kicker">RESUME PREVIEW</div><div class="preview-title">{{ resume?.name || "Resume" }}</div><div class="preview-meta">{{ resume?.file_name || "Uploaded file" }} · {{ resume ? fileTypeLabel(resume) : "" }}</div></div><q-space /><q-btn flat round dense icon="download" color="primary" aria-label="Download resume" @click="$emit('download')" /><q-btn flat round dense icon="close" v-close-popup /></q-card-section>
      <q-card-section class="preview-body"><q-inner-loading :showing="loading"><q-spinner color="primary" size="40px" /></q-inner-loading><iframe v-if="previewUrl && isPdf" class="preview-frame" :src="previewUrl" title="Resume preview" /><pre v-else-if="previewText !== null" class="text-preview">{{ previewText }}</pre><div v-else class="unsupported-preview"><q-icon :name="error ? 'error_outline' : 'description'" size="56px" :color="error ? 'negative' : 'primary'" /><div class="text-h6 q-mt-md">{{ error ? "Preview could not be loaded" : "Preview is available after download" }}</div><div class="text-grey-7 q-mt-sm">{{ error ? "The file may have been removed or the session may have expired." : "This file type cannot be rendered directly in the browser." }}</div><q-btn class="q-mt-md" color="primary" icon="download" label="Download resume" @click="$emit('download')" /></div></q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { Resume } from "@/api/resumes";
import { fileTypeLabel } from "../utils";
const props = defineProps<{ modelValue: boolean; resume: Resume | null; previewUrl: string | null; previewText: string | null; loading: boolean; error: boolean }>();
defineEmits<{ (event: "update:modelValue", value: boolean): void; (event: "download"): void }>();
const isPdf = computed(() => props.resume ? fileTypeLabel(props.resume) === "PDF" : false);
</script>

<style lang="scss" scoped>
.preview-card { display: flex; width: 100%; height: 100%; flex-direction: column; background: var(--cv-page); }
.preview-header { flex: 0 0 auto; border-bottom: 1px solid var(--cv-border); background: var(--cv-surface); }
.preview-kicker { color: var(--cv-muted-light); font-size: 10px; font-weight: 800; letter-spacing: .08em; }
.preview-title { margin-top: 3px; color: var(--cv-navy); font-size: 20px; font-weight: 800; }
.preview-meta { margin-top: 3px; color: var(--cv-muted); font-size: 12px; }
.preview-body { position: relative; flex: 1 1 auto; min-height: 0; height: calc(100vh - 82px); padding: 0; }
.preview-frame { width: 100%; height: 100%; border: 0; background: var(--cv-surface); }
.text-preview { height: 100%; margin: 0; overflow: auto; padding: 32px max(5vw, 20px); background: var(--cv-surface); color: var(--cv-text); font-family: ui-monospace, SFMono-Regular, Consolas, monospace; line-height: 1.6; white-space: pre-wrap; }
.unsupported-preview { display: flex; height: 100%; align-items: center; justify-content: center; flex-direction: column; text-align: center; }
</style>
