<template>
  <div class="trend-wrap">
    <svg
      viewBox="0 0 100 36"
      preserveAspectRatio="none"
      class="trend-svg"
      role="img"
      aria-label="Applications per week"
    >
      <defs>
        <linearGradient id="trend-fill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#219EBC" stop-opacity="0.35" />
          <stop offset="100%" stop-color="#219EBC" stop-opacity="0.02" />
        </linearGradient>
      </defs>

      <line
        x1="0"
        y1="34"
        x2="100"
        y2="34"
        stroke="#e2e8f0"
        stroke-width="0.4"
      />

      <path :d="areaPath" fill="url(#trend-fill)" />
      <path
        :d="linePath"
        fill="none"
        stroke="#219EBC"
        stroke-width="1.6"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
      <circle
        v-for="(p, i) in coords"
        :key="i"
        :cx="p.x"
        :cy="p.y"
        r="1.5"
        fill="#fff"
        stroke="#219EBC"
        stroke-width="1"
      />
    </svg>

    <div class="trend-labels">
      <span v-for="(p, i) in points" :key="i" class="trend-label">
        {{ p.label }}
      </span>
    </div>

    <div v-if="maxValue === 0" class="trend-empty">
      No applications recorded in the last 8 weeks
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { WeeklyPoint } from "../composables/useDashboard";

defineOptions({ name: "TrendChart" });

const props = defineProps<{
  points: WeeklyPoint[];
}>();

const maxValue = computed(() => Math.max(4, ...props.points.map(p => p.value)));

const coords = computed(() =>
  props.points.map((p, i) => {
    const x =
      props.points.length > 1 ? (i / (props.points.length - 1)) * 100 : 0;
    const y = 34 - (p.value / maxValue.value) * 30;
    return { x, y, value: p.value };
  })
);

const linePath = computed(() =>
  coords.value.map((c, i) => `${i === 0 ? "M" : "L"}${c.x},${c.y}`).join(" ")
);

const areaPath = computed(() => {
  const pts = coords.value;
  if (pts.length === 0) return "";
  const first = pts[0]!;
  const last = pts[pts.length - 1]!;
  return `M${first.x},34 L${linePath.value.slice(1)} L${last.x},34 Z`;
});
</script>

<style lang="scss" scoped>
.trend-wrap {
  position: relative;
}

.trend-svg {
  width: 100%;
  height: 160px;
  overflow: visible;
}

.trend-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 6px;
}

.trend-label {
  font-size: 11px;
  color: #94a3b8;
  white-space: nowrap;
}

.trend-empty {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  color: #94a3b8;
}
</style>
