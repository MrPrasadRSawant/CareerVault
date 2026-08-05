<template>
  <div class="donut-wrap">
    <div class="donut-chart">
      <svg
        viewBox="0 0 42 42"
        class="donut-svg"
        role="img"
        aria-label="Status distribution"
      >
        <circle
          cx="21"
          cy="21"
          r="15.9155"
          fill="none"
          stroke="#e8eef3"
          stroke-width="4.5"
        />
        <circle
          v-for="(seg, i) in segments"
          :key="i"
          cx="21"
          cy="21"
          r="15.9155"
          fill="none"
          :stroke="seg.color"
          stroke-width="4.5"
          :stroke-dasharray="`${seg.length} ${100 - seg.length}`"
          :stroke-dashoffset="-seg.offset"
          transform="rotate(-90 21 21)"
          class="donut-segment"
        />
        <text x="21" y="19.5" text-anchor="middle" class="donut-total">
          {{ total }}
        </text>
        <text x="21" y="24.5" text-anchor="middle" class="donut-label">
          total
        </text>
      </svg>
    </div>

    <div v-if="total > 0" class="donut-legend">
      <div v-for="(item, i) in data" :key="i" class="legend-row">
        <span class="legend-dot" :style="{ background: item.color }"></span>
        <span class="legend-label">{{ item.label }}</span>
        <span class="legend-value">{{ item.value }}</span>
        <span class="legend-percent">{{ item.percent }}%</span>
      </div>
    </div>
    <div v-else class="donut-empty">No data yet</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { StatusDatum } from "../composables/useDashboard";

defineOptions({ name: "StatusDonut" });

const props = defineProps<{
  data: StatusDatum[];
  total: number;
}>();

const segments = computed(() => {
  let cumulative = 0;
  return props.data
    .filter(d => d.value > 0)
    .map(d => {
      const seg = { ...d, length: d.percent, offset: cumulative };
      cumulative += d.percent;
      return seg;
    });
});
</script>

<style lang="scss" scoped>
.donut-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
}

.donut-chart {
  width: 100%;
  max-width: 190px;
}

.donut-svg {
  width: 100%;
  height: auto;
}

.donut-segment {
  transition: stroke-dasharray 0.4s ease;
}

.donut-total {
  font-size: 9px;
  font-weight: 700;
  fill: #023047;
}

.donut-label {
  font-size: 3.2px;
  fill: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.donut-legend {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px 20px;
  width: 100%;
}

.legend-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 3px;
}

.legend-label {
  color: #475569;
}

.legend-value {
  font-weight: 700;
  color: #023047;
}

.legend-percent {
  color: #94a3b8;
  min-width: 34px;
  text-align: right;
}

.donut-empty {
  font-size: 13px;
  color: #94a3b8;
  padding: 20px 0;
}
</style>
