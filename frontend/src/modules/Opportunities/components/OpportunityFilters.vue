<template>
  <div class="filters-card">
    <div class="filter-row">
      <q-input
        :model-value="modelValue.search"
        dense
        outlined
        clearable
        debounce="250"
        class="search-input"
        placeholder="Search role, company, skills or description"
        @update:model-value="update('search', String($event ?? ''))"
      >
        <template #prepend><q-icon name="search" /></template>
      </q-input>
      <q-select
        :model-value="modelValue.statuses"
        dense
        outlined
        multiple
        use-chips
        emit-value
        map-options
        options-dense
        class="status-filter"
        label="All statuses"
        :options="statusOptions"
        @update:model-value="updateStatuses"
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
      <div class="workspace-count">
        {{ resultCount }}
        {{ resultCount === 1 ? "opportunity" : "opportunities" }}
      </div>
    </div>
    <q-slide-transition>
      <div v-show="advancedOpen" class="advanced-grid">
        <q-input
          :model-value="modelValue.company"
          dense
          outlined
          label="Company"
          @update:model-value="update('company', String($event ?? ''))"
        />
        <q-input
          :model-value="modelValue.location"
          dense
          outlined
          label="Location"
          @update:model-value="update('location', String($event ?? ''))"
        />
        <q-input
          :model-value="modelValue.experience"
          dense
          outlined
          label="Experience"
          @update:model-value="update('experience', String($event ?? ''))"
        />
        <q-input
          :model-value="modelValue.skills"
          dense
          outlined
          label="Required skill"
          @update:model-value="update('skills', String($event ?? ''))"
        />
        <ProfessionalDateRangeField
          class="range-filter"
          :from="modelValue.postedFrom"
          :to="modelValue.postedTo"
          label="Posted date range"
          @update:from="update('postedFrom', $event)"
          @update:to="update('postedTo', $event)"
        />
      </div>
    </q-slide-transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import ProfessionalDateRangeField from "@/components/ProfessionalDateRangeField.vue";
import type { OpportunityStatus } from "@/api/opportunities";
import type { OpportunityFilters } from "../types";

const props = defineProps<{
  modelValue: OpportunityFilters;
  statusOptions: { label: string; value: string }[];
  resultCount: number;
}>();

const emit = defineEmits<{
  (event: "update:modelValue", value: OpportunityFilters): void;
  (event: "clear"): void;
}>();

const advancedOpen = ref(false);

function update<K extends keyof OpportunityFilters>(
  key: K,
  value: OpportunityFilters[K]
) {
  emit("update:modelValue", { ...props.modelValue, [key]: value });
}

function updateStatuses(value: unknown) {
  update(
    "statuses",
    Array.isArray(value) ? (value as OpportunityStatus[]) : []
  );
}
</script>

<style lang="scss" scoped>
.filters-card {
  margin-bottom: 14px;
}
.filter-row {
  display: flex;
  align-items: center;
  gap: 10px;
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
}
</style>
