<template>
  <q-card flat bordered class="filter-card">
    <div class="filter-content">
      <q-tabs
        :model-value="activeTab"
        dense
        no-caps
        inline-label
        active-color="primary"
        indicator-color="primary"
        align="left"
        class="notification-tabs"
        @update:model-value="$emit('update:activeTab', $event)"
      >
        <q-tab name="all" label="All">
          <q-badge color="blue-grey-2" text-color="blue-grey-9" class="q-ml-sm">
            {{ totalCount }}
          </q-badge>
        </q-tab>
        <q-tab name="unseen" label="Unseen">
          <q-badge color="negative" class="q-ml-sm">{{ unseenCount }}</q-badge>
        </q-tab>
        <q-tab name="seen" label="Seen">
          <q-badge color="blue-grey-2" text-color="blue-grey-9" class="q-ml-sm">
            {{ seenCount }}
          </q-badge>
        </q-tab>
      </q-tabs>
      <q-input
        :model-value="search"
        dense
        outlined
        clearable
        debounce="150"
        placeholder="Search notifications"
        class="search-input"
        @update:model-value="$emit('update:search', String($event ?? ''))"
      >
        <template #prepend><q-icon name="search" /></template>
      </q-input>
    </div>
  </q-card>
</template>

<script setup lang="ts">
import type { NotificationTab } from "../types";

defineProps<{
  activeTab: NotificationTab;
  search: string;
  totalCount: number;
  unseenCount: number;
  seenCount: number;
}>();
defineEmits<{
  (event: "update:activeTab", value: NotificationTab): void;
  (event: "update:search", value: string): void;
}>();
</script>

<style lang="scss" scoped>
.filter-card {
  margin-bottom: 16px;
  border-color: var(--cv-border);
  border-radius: 12px;
}
.filter-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 6px 12px 6px 4px;
}
.search-input {
  width: 280px;
}
@media (max-width: 700px) {
  .filter-content {
    align-items: stretch;
    flex-direction: column;
    padding: 8px 12px 12px;
  }
  .notification-tabs {
    margin: 0 -8px;
  }
  .search-input {
    width: 100%;
  }
}
</style>
