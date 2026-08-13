<template>
  <div class="toolbar-row">
    <div>
      <div class="page-kicker">YOUR ACTIVITY</div>
      <h1>Notifications</h1>
      <p
        >New opportunities and recruiter responses appear here automatically.</p
      >
    </div>
    <div class="row q-gutter-sm">
      <q-btn
        flat
        round
        icon="refresh"
        aria-label="Refresh notifications"
        :loading="loading"
        @click="$emit('refresh')"
      />
      <q-btn
        outline
        no-caps
        color="primary"
        icon="done_all"
        label="Mark all as seen"
        :disable="unseenCount === 0"
        :loading="markingAll"
        @click="$emit('mark-all-seen')"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ loading: boolean; markingAll: boolean; unseenCount: number }>();
defineEmits<{
  (event: "refresh"): void;
  (event: "mark-all-seen"): void;
}>();
</script>

<style lang="scss" scoped>
.toolbar-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 18px;
}
.page-kicker {
  color: var(--cv-primary);
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.1em;
}
h1 {
  margin: 4px 0 2px;
  color: var(--cv-navy);
  font-size: 28px;
  font-weight: 800;
  line-height: 1.2;
}
p {
  margin: 0;
  color: var(--cv-muted);
}
@media (max-width: 650px) {
  .toolbar-row {
    align-items: stretch;
    flex-direction: column;
  }
}
</style>
