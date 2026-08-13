<template>
  <div class="toolbar-row">
    <div>
      <div class="page-kicker">RECRUITER COMMUNICATIONS</div>
      <h1>Email follow-ups</h1>
      <p
        >Track every application response and its outcome in one email chain.</p
      >
    </div>
    <div class="row q-gutter-sm">
      <q-btn
        flat
        round
        icon="refresh"
        aria-label="Refresh email follow-ups"
        :loading="loading"
        @click="$emit('refresh')"
      />
      <q-btn
        color="primary"
        icon="add"
        label="Add email"
        no-caps
        @click="$emit('create')"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ loading: boolean }>();
defineEmits<{ (event: "refresh"): void; (event: "create"): void }>();
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
