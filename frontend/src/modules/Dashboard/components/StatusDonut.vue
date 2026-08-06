<template>
  <div class="donut-wrap">
    <div v-if="total > 0" class="donut-chart">
      <svg
        viewBox="0 0 42 42"
        class="donut-svg"
        role="img"
        :aria-labelledby="`${chartId}-title ${chartId}-description`"
      >
        <title :id="`${chartId}-title`">Status distribution</title>
        <desc :id="`${chartId}-description`">
          {{ total }} total opportunities grouped by status.
        </desc>
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
          TOTAL
        </text>
      </svg>
    </div>

    <div v-if="total > 0" class="summary-table-wrap">
      <table class="summary-table">
        <caption class="sr-only">Opportunity counts grouped by status</caption>
        <thead>
          <tr>
            <th scope="col">Status</th>
            <th scope="col" class="numeric-column">Count</th>
            <th scope="col" class="numeric-column">Share</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in legendItems" :key="item.label">
            <td>
              <span class="status-name">
                <span class="legend-dot" :style="{ background: item.color }"></span>
                {{ item.label }}
              </span>
            </td>
            <td class="summary-value numeric-column">{{ item.value }}</td>
            <td class="summary-percent numeric-column">{{ item.percent }}%</td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <th scope="row">Total</th>
            <td class="summary-value numeric-column">{{ total }}</td>
            <td class="summary-percent numeric-column">100%</td>
          </tr>
        </tfoot>
      </table>
    </div>
    <div v-else class="donut-empty">No data yet</div>
  </div>
</template>

<script setup lang="ts">
import { computed, useId } from "vue";
import type { StatusDatum } from "../composables/useDashboard";

defineOptions({ name: "StatusDonut" });

const props = defineProps<{
  data: StatusDatum[];
  total: number;
}>();

const chartId = useId().replace(/:/g, "");

const legendItems = computed(() => props.data.filter(item => item.value > 0));

const segments = computed(() => {
  let cumulative = 0;
  return props.data
    .filter(d => d.value > 0)
    .map(d => {
      const length = props.total > 0 ? (d.value / props.total) * 100 : 0;
      const seg = { ...d, length, offset: cumulative };
      cumulative += length;
      return seg;
    });
});
</script>

<style lang="scss" scoped>
.donut-wrap {
  display: grid;
  grid-template-columns: minmax(160px, 210px) minmax(0, 1fr);
  align-items: center;
  gap: 28px;
  min-height: 210px;
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
  transition:
    stroke-dasharray 0.4s ease,
    stroke-dashoffset 0.4s ease;
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

.summary-table-wrap {
  width: 100%;
  overflow-x: auto;
}

.summary-table {
  width: 100%;
  border-collapse: collapse;
  color: #475569;
  font-size: 13px;
}

.summary-table caption.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.summary-table th,
.summary-table td {
  padding: 9px 12px;
  border-bottom: 1px solid #edf2f5;
  text-align: left;
}

.summary-table thead th {
  color: #829ab1;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.summary-table tfoot th,
.summary-table tfoot td {
  border-bottom: 0;
  color: #102a43;
  font-weight: 700;
}

.status-name {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 3px;
}

.summary-value {
  font-weight: 700;
  color: #023047;
}

.summary-percent {
  color: #94a3b8;
}

.summary-table .numeric-column {
  width: 82px;
  text-align: right;
}

.donut-empty {
  grid-column: 1 / -1;
  font-size: 13px;
  color: #94a3b8;
  padding: 20px 0;
  text-align: center;
}

@media (max-width: 700px) {
  .donut-wrap {
    display: flex;
    flex-direction: column;
    gap: 18px;
  }

  .summary-table th,
  .summary-table td {
    padding: 8px;
  }
}
</style>
