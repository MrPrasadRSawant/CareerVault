<template>
  <q-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <q-card v-if="letter" class="view-card">
      <q-card-section class="row items-start">
        <div>
          <div class="view-kicker">COVER LETTER</div>
          <div class="view-title">{{ letter.name }}</div>
        </div>
        <q-space />
        <q-btn flat round dense icon="close" v-close-popup />
      </q-card-section>
      <q-card-section class="view-body">
        <div class="detail-grid">
          <div>
            <span>File</span>
            <strong>{{ letter.file_name || "Text letter" }}</strong>
          </div>
          <div>
            <span>Created</span>
            <strong>{{ formatDate(letter.created_at) }}</strong>
          </div>
        </div>
        <div v-if="letter.content" class="content-block">
          <div class="detail-label">Content</div>
          <div class="letter-content rendered-content" v-html="letter.content" />
        </div>
        <p v-else class="text-grey-6">This letter has no content yet.</p>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import type { CoverLetter } from "@/api/coverLetters";

defineProps<{
  modelValue: boolean;
  letter: CoverLetter | null;
}>();
defineEmits<{
  (event: "update:modelValue", value: boolean): void;
}>();

function formatDate(value: string) {
  return value ? new Date(value).toLocaleDateString() : "—";
}
</script>

<style lang="scss" scoped>
.view-card {
  width: min(600px, 94vw);
  border-radius: 14px;
}
.view-kicker {
  color: var(--cv-muted-light);
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.08em;
}
.view-title {
  margin-top: 6px;
  color: var(--cv-navy);
  font-size: 22px;
  font-weight: 800;
}
.view-body {
  padding-top: 0;
}
.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  border-top: 1px solid var(--cv-border-light);
  border-bottom: 1px solid var(--cv-border-light);
  padding: 16px 0;
}
.detail-grid span,
.detail-label {
  display: block;
  color: var(--cv-muted-light);
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
}
.detail-grid strong {
  display: block;
  margin-top: 3px;
  color: var(--cv-text-strong);
  font-size: 13px;
}
.content-block {
  margin-top: 16px;
}
.letter-content {
  margin-top: 8px;
  line-height: 1.7;
  color: #334e5a;
}
.rendered-content :deep(h1) {
  font-size: 20px;
  font-weight: 800;
  margin: 16px 0 8px;
  color: var(--cv-navy);
}
.rendered-content :deep(h2) {
  font-size: 16px;
  font-weight: 800;
  margin: 14px 0 6px;
  color: var(--cv-navy);
}
.rendered-content :deep(ul),
.rendered-content :deep(ol) {
  padding-left: 24px;
  margin: 8px 0;
}
.rendered-content :deep(li) {
  margin: 2px 0;
}
.rendered-content :deep(blockquote) {
  border-left: 3px solid var(--cv-primary);
  margin: 12px 0;
  padding: 8px 16px;
  background: #f8fafc;
  border-radius: 0 8px 8px 0;
  color: var(--cv-muted);
  font-style: italic;
}
.rendered-content :deep(hr) {
  border: none;
  border-top: 1px solid #dce6eb;
  margin: 16px 0;
}
.rendered-content :deep(a) {
  color: var(--cv-primary-dark);
  text-decoration: underline;
}
</style>
