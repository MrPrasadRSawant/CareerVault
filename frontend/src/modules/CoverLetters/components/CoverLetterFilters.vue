<template>
  <div class="filters-card">
    <q-tabs
      :model-value="activeTab"
      dense
      align="left"
      active-color="primary"
      indicator-color="primary"
      class="cover-letter-tabs"
      @update:model-value="
        $emit('update:activeTab', $event as CoverLetterTabKey)
      "
    >
      <q-tab
        v-for="tab in tabs"
        :key="tab.key"
        :name="tab.key"
        :aria-label="`${tab.label}: ${counts[tab.key]}`"
      >
        <span class="tab-label">
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
        placeholder="Search letter name or content"
        ><template #prepend><q-icon name="search" /></template
      ></q-input>
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
        {{ resultCount === 1 ? "letter" : "letters" }}</div
      >
    </div>
    <q-slide-transition>
      <div v-show="advancedOpen" class="advanced-grid">
        <ProfessionalDateRangeField
          class="range-filter"
          :from="filters.createdFrom"
          :to="filters.createdTo"
          label="Created date range"
          @update:from="filters.createdFrom = $event"
          @update:to="filters.createdTo = $event"
        />
      </div>
    </q-slide-transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import ProfessionalDateRangeField from "@/components/ProfessionalDateRangeField.vue";
import type { CoverLetterFilters, CoverLetterTabKey } from "../types";
import { coverLetterTabs } from "../utils";

defineProps<{
  filters: CoverLetterFilters;
  activeTab: CoverLetterTabKey;
  counts: Record<CoverLetterTabKey, number>;
  resultCount: number;
}>();
defineEmits<{
  (event: "update:activeTab", value: CoverLetterTabKey): void;
  (event: "clear"): void;
}>();
const tabs = coverLetterTabs;
const advancedOpen = ref(false);
</script>

<style lang="scss" scoped>
.filters-card {
  margin-bottom: 14px;
}
.cover-letter-tabs {
  border-bottom: 1px solid var(--cv-border-light);
}
.tab-label {
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
.cover-letter-tabs :deep(.q-tab--active) .tab-count {
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
  .range-filter {
    grid-column: span 2;
  }
}
</style>
