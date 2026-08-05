<template>
  <div class="bars-wrap" role="list" aria-label="Application statuses">
    <div v-for="(item, i) in data" :key="i" class="bar-row" role="listitem">
      <div class="bar-header">
        <span class="bar-label">{{ item.label }}</span>
        <span class="bar-value">{{ item.value }}</span>
      </div>
      <div
        class="bar-track"
        role="progressbar"
        :aria-label="`${item.label}: ${item.value}`"
        :aria-valuenow="item.percent"
        aria-valuemin="0"
        aria-valuemax="100"
      >
        <div
          class="bar-fill"
          :style="{ width: `${Math.min(100, Math.max(0, item.percent))}%`, background: item.color }"
        ></div>
      </div>
    </div>
    <div v-if="data.every(d => d.value === 0)" class="bars-empty">
      No applications yet
    </div>
  </div>
</template>

<script setup lang="ts">
import type { StatusDatum } from "../composables/useDashboard";

defineOptions({ name: "StatusBars" });

defineProps<{
  data: StatusDatum[];
}>();
</script>

<style lang="scss" scoped>
.bars-wrap {
  display: flex;
  flex-direction: column;
  gap: 18px;
  min-height: 220px;
  justify-content: center;
}

.bar-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.bar-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}

.bar-label {
  font-size: 13.5px;
  font-weight: 500;
  color: #475569;
}

.bar-value {
  font-size: 13.5px;
  font-weight: 700;
  color: #023047;
}

.bar-track {
  height: 9px;
  border-radius: 5px;
  background: #eef2f6;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  min-width: 2px;
  border-radius: 5px;
  transition: width 0.5s ease;
}

.bars-empty {
  font-size: 13px;
  color: #94a3b8;
  padding: 24px 0;
  text-align: center;
}
</style>
