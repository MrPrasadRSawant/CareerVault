<template>
  <q-card flat bordered class="filter-card">
    <q-card-section class="filter-row">
      <q-input
        :model-value="filters.search"
        dense
        outlined
        clearable
        debounce="150"
        placeholder="Search job, company, sender, subject, or reason"
        class="search-input"
        @update:model-value="filters.search = String($event ?? '')"
      >
        <template #prepend><q-icon name="search" /></template>
      </q-input>
      <q-select
        :model-value="filters.outcome"
        dense
        outlined
        emit-value
        map-options
        label="Outcome"
        :options="outcomeOptions"
        class="outcome-select"
        @update:model-value="filters.outcome = $event"
      />
      <q-btn
        v-if="filters.search || filters.outcome !== 'all'"
        flat
        no-caps
        color="primary"
        icon="filter_alt_off"
        label="Clear"
        @click="$emit('clear')"
      />
      <q-space />
      <span class="result-count">{{ resultCount }} applications</span>
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
import type { EmailFollowUpFilters } from "../types";
import { emailOutcomeOptions } from "../utils";

defineProps<{
  filters: EmailFollowUpFilters;
  resultCount: number;
}>();
defineEmits<{ (event: "clear"): void }>();

const outcomeOptions = [
  { label: "All outcomes", value: "all" },
  ...emailOutcomeOptions.map(({ label, value }) => ({ label, value }))
];
</script>

<style lang="scss" scoped>
.filter-card {
  margin-bottom: 16px;
  border-color: var(--cv-border);
  border-radius: 12px;
}
.filter-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
}
.search-input {
  width: min(460px, 100%);
}
.outcome-select {
  width: 180px;
}
.result-count {
  color: var(--cv-muted-light);
  font-size: 12px;
  white-space: nowrap;
}
@media (max-width: 700px) {
  .filter-row {
    align-items: stretch;
    flex-direction: column;
  }
  .search-input,
  .outcome-select {
    width: 100%;
  }
}
</style>
