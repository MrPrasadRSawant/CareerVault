<template>
  <div class="filters-wrap q-mb-md">
    <q-tabs :model-value="activeTab" dense align="left" active-color="primary" indicator-color="primary" class="resume-tabs" @update:model-value="$emit('update:activeTab', $event as ResumeTabKey)">
      <q-tab v-for="tab in tabs" :key="tab.key" :name="tab.key" :aria-label="`${tab.label}: ${counts[tab.key]}`"><span class="tab-label"><span>{{ tab.label }}</span><span class="tab-count" :class="{ 'tab-count--empty': counts[tab.key] === 0 }">{{ counts[tab.key] }}</span></span></q-tab>
    </q-tabs>
    <div class="filter-row row items-center q-col-gutter-sm q-mt-sm">
      <div class="col-12 col-md-4"><q-input v-model="filters.search" outlined dense clearable placeholder="Search resume name, version or file"><template #prepend><q-icon name="search" /></template></q-input></div>
      <div class="col-12 col-md-3"><q-select v-model="filters.attachment" outlined dense emit-value map-options label="Application link" :options="attachmentOptions" /></div>
      <div class="col-auto"><q-btn flat no-caps icon="tune" label="Advanced filters" @click="advancedOpen = !advancedOpen" /></div>
      <div class="col-auto"><q-btn flat no-caps icon="restart_alt" label="Clear" @click="$emit('clear')" /></div>
    </div>
    <q-slide-transition><div v-show="advancedOpen" class="advanced-panel q-mt-sm"><div class="row q-col-gutter-sm"><div class="col-12 col-md-4"><q-select v-model="filters.fileType" outlined dense clearable label="File type" :options="fileTypeOptions" /></div><div class="col-12 col-md-4"><q-input v-model="filters.uploadedFrom" outlined dense type="date" label="Uploaded from" /></div><div class="col-12 col-md-4"><q-input v-model="filters.uploadedTo" outlined dense type="date" label="Uploaded to" /></div></div></div></q-slide-transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import type { ResumeFilters, ResumeTabKey } from "../types";
import { resumeTabs } from "../utils";

defineProps<{ filters: ResumeFilters; activeTab: ResumeTabKey; counts: Record<ResumeTabKey, number> }>();
defineEmits<{ (event: "update:activeTab", value: ResumeTabKey): void; (event: "clear"): void }>();
const tabs = resumeTabs;
const attachmentOptions = [{ label: "All links", value: "all" }, { label: "Attached to applications", value: "attached" }, { label: "Not attached", value: "unattached" }];
const fileTypeOptions = ["PDF", "DOC", "DOCX", "TXT", "MD"];
const advancedOpen = ref(false);
</script>

<style lang="scss" scoped>
.resume-tabs { border-bottom: 1px solid var(--cv-border-light); }
.tab-label { display: inline-flex; align-items: center; gap: 7px; font-size: 13px; font-weight: 700; line-height: 1; }
.tab-count { display: inline-flex; align-items: center; justify-content: center; min-width: 20px; height: 20px; padding: 0 6px; border-radius: 999px; background: var(--cv-primary-soft); color: var(--cv-primary-dark); font-size: 11px; font-weight: 800; }
.tab-count--empty { background: var(--cv-empty-soft); color: var(--cv-muted-light); }
.resume-tabs :deep(.q-tab--active) .tab-count { background: var(--cv-primary-dark); color: var(--cv-white); }
.advanced-panel { padding: 14px; border-radius: 10px; background: var(--cv-page); }
</style>
