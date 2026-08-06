<template>
  <div class="filters-card">
    <q-tabs
      :model-value="activeTab"
      dense
      align="left"
      active-color="primary"
      indicator-color="primary"
      class="application-tabs"
      @update:model-value="
        $emit('update:activeTab', $event as ApplicationTabKey)
      "
    >
      <q-tab
        v-for="tab in tabs"
        :key="tab.key"
        :name="tab.key"
        :aria-label="`${tab.label}: ${counts[tab.key]}`"
      >
        <span class="application-tab-label">
          <span>{{ tab.label }}</span>
          <span
            class="tab-count"
            :class="{ 'tab-count--empty': counts[tab.key] === 0 }"
            >{{ counts[tab.key] }}</span
          >
        </span>
      </q-tab>
    </q-tabs>
    <div class="filter-row">
      <q-input
        v-model="filters.search"
        outlined
        dense
        clearable
        debounce="250"
        class="search-input"
        placeholder="Search opportunity, company or notes"
        ><template #prepend><q-icon name="search" /></template
      ></q-input>
      <q-select
        v-model="filters.statuses"
        outlined
        dense
        multiple
        use-chips
        emit-value
        map-options
        options-dense
        class="status-filter"
        :options="statusOptions"
        label="All statuses"
      />
      <q-btn
        flat
        no-caps
        icon="tune"
        label="Advanced filters"
        :color="advancedOpen ? 'primary' : undefined"
        @click="advancedOpen = !advancedOpen"
      />
      <q-btn
        flat
        no-caps
        icon="restart_alt"
        label="Clear"
        @click="$emit('clear')"
      />
      <div class="workspace-count"
        >{{ resultCount }}
        {{ resultCount === 1 ? "application" : "applications" }}</div
      >
    </div>
    <q-slide-transition>
      <div v-show="advancedOpen" class="advanced-grid">
        <q-input v-model="filters.company" outlined dense label="Company" />
        <q-input v-model="filters.location" outlined dense label="Location" />
        <ProfessionalDateRangeField
          class="range-filter"
          :from="filters.appliedFrom"
          :to="filters.appliedTo"
          label="Applied date range"
          @update:from="filters.appliedFrom = $event"
          @update:to="filters.appliedTo = $event"
        />
        <q-select
          v-model="filters.hasResume"
          outlined
          dense
          emit-value
          map-options
          label="Resume"
          :options="presenceOptions"
        />
        <q-select
          v-model="filters.hasCoverLetter"
          outlined
          dense
          emit-value
          map-options
          label="Cover letter"
          :options="presenceOptions"
        />
        <q-input
          v-model="filters.notes"
          outlined
          dense
          class="notes-filter"
          label="Notes contain"
        />
      </div>
    </q-slide-transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import ProfessionalDateRangeField from "@/components/ProfessionalDateRangeField.vue";
import type { ApplicationFilters, ApplicationTabKey } from "../types";
import { applicationStatusOptions, applicationTabs } from "../utils";

defineProps<{
  filters: ApplicationFilters;
  activeTab: ApplicationTabKey;
  counts: Record<ApplicationTabKey, number>;
  resultCount: number;
}>();
defineEmits<{
  (event: "update:activeTab", value: ApplicationTabKey): void;
  (event: "clear"): void;
}>();
const tabs = applicationTabs;
const statusOptions = applicationStatusOptions;
const presenceOptions = [
  { label: "Any", value: "any" },
  { label: "Attached", value: "yes" },
  { label: "Missing", value: "no" }
];
const advancedOpen = ref(false);
</script>

<style lang="scss" scoped>
.filters-card {
  margin-bottom: 14px;
}
.application-tabs {
  border-bottom: 1px solid var(--cv-border-light);
}
.application-tab-label {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  font-size: 13px;
  font-weight: 700;
  line-height: 1;
}
.tab-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  border-radius: 999px;
  background: var(--cv-primary-soft);
  color: var(--cv-primary-dark);
  font-size: 11px;
  font-weight: 800;
}
.tab-count--empty {
  background: var(--cv-empty-soft);
  color: var(--cv-muted-light);
}
.application-tabs :deep(.q-tab--active) .tab-count {
  background: var(--cv-primary-dark);
  color: var(--cv-white);
}
.filter-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
  flex-wrap: wrap;
}
.search-input {
  flex: 1 1 340px;
  max-width: 520px;
}
.status-filter {
  width: 220px;
}
.workspace-count {
  margin-left: auto;
  color: #829ab1;
  font-size: 13px;
}
.advanced-grid {
  display: grid;
  grid-template-columns: repeat(6, minmax(120px, 1fr));
  gap: 10px;
  margin-top: 10px;
  padding: 12px;
  border: 1px solid #dce6eb;
  border-radius: 10px;
  background: #fff;
}
.notes-filter {
  grid-column: span 2;
}
.range-filter {
  grid-column: span 2;
}
@media (max-width: 900px) {
  .advanced-grid {
    grid-template-columns: repeat(3, minmax(120px, 1fr));
  }
}
@media (max-width: 600px) {
  .advanced-grid {
    grid-template-columns: repeat(2, minmax(120px, 1fr));
  }
  .workspace-count {
    width: 100%;
    margin-left: 0;
  }
  .status-filter {
    flex: 1 1 200px;
  }
  .notes-filter {
    grid-column: span 2;
  }
  .range-filter {
    grid-column: span 2;
  }
}
</style>
