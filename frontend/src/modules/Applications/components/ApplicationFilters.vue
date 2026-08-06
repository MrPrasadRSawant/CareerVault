<template>
  <div class="filters-wrap q-mb-md">
    <q-tabs :model-value="activeTab" dense align="left" active-color="primary" indicator-color="primary" class="application-tabs" @update:model-value="$emit('update:activeTab', $event as ApplicationTabKey)">
      <q-tab v-for="tab in tabs" :key="tab.key" :name="tab.key" :aria-label="`${tab.label}: ${counts[tab.key]}`">
        <span class="application-tab-label">
          <span>{{ tab.label }}</span>
          <span class="tab-count" :class="{ 'tab-count--empty': counts[tab.key] === 0 }">{{ counts[tab.key] }}</span>
        </span>
      </q-tab>
    </q-tabs>
    <div class="filter-row row items-center q-col-gutter-sm q-mt-sm">
      <div class="col-12 col-md-4"><q-input v-model="filters.search" outlined dense clearable placeholder="Search opportunity, company or notes"><template #prepend><q-icon name="search" /></template></q-input></div>
      <div class="col-12 col-md-3"><q-select v-model="filters.statuses" outlined dense multiple emit-value map-options :options="statusOptions" label="Statuses" /></div>
      <div class="col-auto"><q-btn flat no-caps icon="tune" label="Advanced filters" @click="advancedOpen = !advancedOpen" /></div>
      <div class="col-auto"><q-btn flat no-caps icon="restart_alt" label="Clear" @click="$emit('clear')" /></div>
    </div>
    <q-slide-transition>
      <div v-show="advancedOpen" class="advanced-panel q-mt-sm">
        <div class="row q-col-gutter-sm">
          <div class="col-12 col-md-3"><q-input v-model="filters.company" outlined dense label="Company" /></div>
          <div class="col-12 col-md-3"><q-input v-model="filters.location" outlined dense label="Location" /></div>
          <div class="col-12 col-md-3"><q-input v-model="filters.appliedFrom" outlined dense type="date" label="Applied from" /></div>
          <div class="col-12 col-md-3"><q-input v-model="filters.appliedTo" outlined dense type="date" label="Applied to" /></div>
          <div class="col-12 col-md-3"><q-select v-model="filters.hasResume" outlined dense emit-value map-options label="Resume" :options="presenceOptions" /></div>
          <div class="col-12 col-md-3"><q-select v-model="filters.hasCoverLetter" outlined dense emit-value map-options label="Cover letter" :options="presenceOptions" /></div>
          <div class="col-12 col-md-6"><q-input v-model="filters.notes" outlined dense label="Notes contain" /></div>
        </div>
      </div>
    </q-slide-transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import type { ApplicationFilters, ApplicationTabKey } from "../types";
import { applicationStatusOptions, applicationTabs } from "../utils";

defineProps<{ filters: ApplicationFilters; activeTab: ApplicationTabKey; counts: Record<ApplicationTabKey, number> }>();
defineEmits<{ (event: "update:activeTab", value: ApplicationTabKey): void; (event: "clear"): void }>();
const tabs = applicationTabs;
const statusOptions = applicationStatusOptions;
const presenceOptions = [{ label: "Any", value: "any" }, { label: "Attached", value: "yes" }, { label: "Missing", value: "no" }];
const advancedOpen = ref(false);
</script>

<style lang="scss" scoped>
.application-tabs { border-bottom: 1px solid var(--cv-border-light); }
.application-tab-label { display: inline-flex; align-items: center; gap: 7px; font-size: 13px; font-weight: 700; line-height: 1; }
.tab-count { display: inline-flex; align-items: center; justify-content: center; min-width: 20px; height: 20px; padding: 0 6px; border-radius: 999px; background: var(--cv-primary-soft); color: var(--cv-primary-dark); font-size: 11px; font-weight: 800; }
.tab-count--empty { background: var(--cv-empty-soft); color: var(--cv-muted-light); }
.application-tabs :deep(.q-tab--active) .tab-count { background: var(--cv-primary-dark); color: var(--cv-white); }
.advanced-panel { padding: 14px; border-radius: 10px; background: var(--cv-page); }
</style>
