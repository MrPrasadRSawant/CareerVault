<template>
  <div class="trend-wrap">
    <div class="trend-summary" aria-live="polite">
      <div class="trend-primary-metric">
        <span class="trend-metric-value">{{ totalApplications }}</span>
        <span class="trend-metric-label">{{ metricLabel }}</span>
      </div>
      <div class="trend-secondary-metrics">
        <div class="trend-secondary-metric">
          <span class="trend-secondary-label">Weekly average</span>
          <strong>{{ weeklyAverage }}</strong>
        </div>
        <div class="trend-secondary-metric">
          <span class="trend-secondary-label">Peak week</span>
          <strong>{{ peakValue }}</strong>
        </div>
        <div class="trend-secondary-metric trend-change" :class="changeClass">
          <span class="trend-secondary-label">Recent movement</span>
          <strong>{{ changeLabel }}</strong>
        </div>
      </div>
    </div>

    <div class="trend-insight">
      <q-icon :name="insightIcon" size="16px" />
      <span>{{ insight }}</span>
    </div>

    <div class="trend-chart-shell">
      <svg
        viewBox="0 0 640 250"
        preserveAspectRatio="none"
        class="trend-svg"
        role="img"
        :aria-labelledby="`${chartId}-title ${chartId}-description`"
      >
        <title :id="`${chartId}-title`">{{ metricTitle }} per week</title>
        <desc :id="`${chartId}-description`">{{ chartDescription }}</desc>

        <defs>
          <linearGradient :id="`${chartId}-area`" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#1F6F8B" stop-opacity="0.24" />
            <stop offset="100%" stop-color="#1F6F8B" stop-opacity="0.015" />
          </linearGradient>
          <filter
            :id="`${chartId}-shadow`"
            x="-20%"
            y="-20%"
            width="140%"
            height="150%"
          >
            <feDropShadow
              dx="0"
              dy="3"
              stdDeviation="3"
              flood-color="#1F6F8B"
              flood-opacity="0.2"
            />
          </filter>
        </defs>

        <g class="trend-y-axis" aria-hidden="true">
          <line
            v-for="tick in yTicks"
            :key="tick.value"
            :x1="chartPadding.left"
            :y1="tick.y"
            :x2="chartWidth - chartPadding.right"
            :y2="tick.y"
          />
          <text
            v-for="tick in yTicks"
            :key="`label-${tick.value}`"
            x="0"
            :y="tick.y + 4"
          >
            {{ tick.value }}
          </text>
        </g>

        <path :d="areaPath" :fill="`url(#${chartId}-area)`" />
        <path
          :d="linePath"
          class="trend-line"
          :filter="`url(#${chartId}-shadow)`"
          vector-effect="non-scaling-stroke"
        />

        <g v-if="activePoint" class="trend-tooltip-layer" aria-hidden="true">
          <line
            class="trend-crosshair"
            :x1="activePoint.x"
            :y1="chartPadding.top"
            :x2="activePoint.x"
            :y2="chartHeight - chartPadding.bottom"
          />
          <circle
            :cx="activePoint.x"
            :cy="activePoint.y"
            r="7"
            class="trend-point-ring"
          />
          <g :transform="`translate(${tooltipX}, ${tooltipY})`">
            <rect width="118" height="48" rx="8" class="trend-tooltip" />
            <text x="12" y="19" class="trend-tooltip-label">
              {{ activePoint.label }}
            </text>
            <text x="12" y="37" class="trend-tooltip-value">
              {{ activePoint.value }}
              {{ activePoint.value === 1 ? singularLabel : metricLabel }}
            </text>
          </g>
        </g>

        <circle
          v-for="(point, index) in plottedPoints"
          :key="point.label"
          :cx="point.x"
          :cy="point.y"
          r="4"
          class="trend-point"
          tabindex="0"
          :aria-label="`${point.label}: ${point.value} ${metricLabel}`"
          @mouseenter="activeIndex = index"
          @mouseleave="activeIndex = null"
          @focus="activeIndex = index"
          @blur="activeIndex = null"
        >
          <title>{{ point.label }}: {{ point.value }} {{ metricLabel }}</title>
        </circle>
      </svg>

      <div class="trend-x-axis" aria-hidden="true">
        <span v-for="point in points" :key="point.label">{{
          point.label
        }}</span>
      </div>

      <div
        v-if="points.length === 0 || totalApplications === 0"
        class="trend-empty"
      >
        <q-icon name="insights" size="24px" />
        <span>No {{ metricLabel }} recorded in this period</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, useId } from "vue";
import type { WeeklyPoint } from "../composables/useDashboard";

defineOptions({ name: "TrendChart" });

const props = withDefaults(
  defineProps<{
    points: WeeklyPoint[];
    metricLabel?: string;
  }>(),
  { metricLabel: "applications" }
);

const chartId = useId().replace(/:/g, "");
const singularLabel = computed(() =>
  props.metricLabel.endsWith("ies")
    ? `${props.metricLabel.slice(0, -3)}y`
    : props.metricLabel.endsWith("s")
      ? props.metricLabel.slice(0, -1)
      : props.metricLabel
);
const metricTitle = computed(
  () => props.metricLabel.charAt(0).toUpperCase() + props.metricLabel.slice(1)
);
const activeIndex = ref<number | null>(null);

const chartWidth = 640;
const chartHeight = 250;
const chartPadding = { top: 18, right: 14, bottom: 28, left: 34 };

const totalApplications = computed(() =>
  props.points.reduce((total, point) => total + Math.max(0, point.value), 0)
);

const weeklyAverage = computed(() =>
  props.points.length
    ? (totalApplications.value / props.points.length).toFixed(1)
    : "0.0"
);

const peakValue = computed(() =>
  Math.max(0, ...props.points.map(point => point.value))
);

const recentTotal = computed(() =>
  props.points
    .slice(-4)
    .reduce((total, point) => total + Math.max(0, point.value), 0)
);

const previousTotal = computed(() =>
  props.points
    .slice(-8, -4)
    .reduce((total, point) => total + Math.max(0, point.value), 0)
);

const changePercent = computed(() => {
  if (previousTotal.value === 0) return recentTotal.value > 0 ? 100 : 0;
  return Math.round(
    ((recentTotal.value - previousTotal.value) / previousTotal.value) * 100
  );
});

const changeLabel = computed(() => {
  if (previousTotal.value === 0) return recentTotal.value > 0 ? "New" : "Flat";
  if (changePercent.value === 0) return "Flat";
  return `${changePercent.value > 0 ? "+" : ""}${changePercent.value}%`;
});

const changeClass = computed(() =>
  changePercent.value > 0
    ? "trend-change--up"
    : changePercent.value < 0
      ? "trend-change--down"
      : "trend-change--flat"
);

const insightIcon = computed(() =>
  changePercent.value > 0
    ? "trending_up"
    : changePercent.value < 0
      ? "trending_down"
      : "trending_flat"
);

const insight = computed(() => {
  if (totalApplications.value === 0)
    return `Start logging ${props.metricLabel} to see your momentum over time.`;
  if (previousTotal.value === 0 && recentTotal.value > 0)
    return "Recent activity is newly established; keep tracking to build a reliable trend.";
  if (changePercent.value > 0)
    return `${metricTitle.value} activity is up ${changePercent.value}% in the most recent four weeks.`;
  if (changePercent.value < 0)
    return `${metricTitle.value} activity is down ${Math.abs(changePercent.value)}% in the most recent four weeks.`;
  return `${metricTitle.value} activity is stable compared with the previous four weeks.`;
});

const scaleMax = computed(() => {
  const highest = Math.max(0, ...props.points.map(point => point.value));
  return Math.max(4, Math.ceil(highest / 4) * 4);
});

const yTicks = computed(() => {
  const step = scaleMax.value / 4;
  return [0, 1, 2, 3, 4].map(index => ({
    value: Math.round(step * (4 - index)),
    y:
      chartPadding.top +
      index * ((chartHeight - chartPadding.top - chartPadding.bottom) / 4)
  }));
});

const plottedPoints = computed(() => {
  const innerWidth = chartWidth - chartPadding.left - chartPadding.right;
  const innerHeight = chartHeight - chartPadding.top - chartPadding.bottom;
  return props.points.map((point, index) => ({
    ...point,
    value: Math.max(0, point.value),
    x:
      props.points.length > 1
        ? chartPadding.left + (index / (props.points.length - 1)) * innerWidth
        : chartPadding.left + innerWidth / 2,
    y:
      chartPadding.top +
      innerHeight -
      (Math.max(0, point.value) / scaleMax.value) * innerHeight
  }));
});

function buildSmoothPath(points: typeof plottedPoints.value): string {
  if (points.length === 0) return "";
  if (points.length === 1) return `M ${points[0]!.x} ${points[0]!.y}`;

  let path = `M ${points[0]!.x} ${points[0]!.y}`;
  for (let index = 1; index < points.length; index += 1) {
    const previous = points[index - 1]!;
    const current = points[index]!;
    const distance = (current.x - previous.x) * 0.42;
    path += ` C ${previous.x + distance} ${previous.y}, ${current.x - distance} ${current.y}, ${current.x} ${current.y}`;
  }
  return path;
}

const linePath = computed(() => buildSmoothPath(plottedPoints.value));

const areaPath = computed(() => {
  const points = plottedPoints.value;
  if (points.length === 0) return "";
  const first = points[0]!;
  const last = points[points.length - 1]!;
  return `${linePath.value} L ${last.x} ${chartHeight - chartPadding.bottom} L ${first.x} ${chartHeight - chartPadding.bottom} Z`;
});

const activePoint = computed(() =>
  activeIndex.value === null
    ? null
    : (plottedPoints.value[activeIndex.value] ?? null)
);

const tooltipX = computed(() => {
  if (!activePoint.value) return 0;
  return Math.min(
    chartWidth - chartPadding.right - 118,
    Math.max(chartPadding.left, activePoint.value.x - 59)
  );
});

const tooltipY = computed(() =>
  activePoint.value ? Math.max(chartPadding.top, activePoint.value.y - 62) : 0
);

const chartDescription = computed(
  () =>
    `${totalApplications.value} ${props.metricLabel} across ${props.points.length} weeks. Peak week: ${peakValue.value}.`
);
</script>

<style lang="scss" scoped>
.trend-wrap {
  position: relative;
}

.trend-summary {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 14px;
}

.trend-primary-metric {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.trend-metric-value {
  color: #102a43;
  font-size: 30px;
  font-weight: 750;
  letter-spacing: -0.8px;
  line-height: 1;
}

.trend-metric-label,
.trend-secondary-label {
  color: #829ab1;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.45px;
  text-transform: uppercase;
}

.trend-secondary-metrics {
  display: flex;
  gap: 22px;
}

.trend-secondary-metric {
  display: flex;
  flex-direction: column;
  gap: 4px;
  text-align: right;

  strong {
    color: #243b53;
    font-size: 15px;
    font-weight: 700;
  }
}

.trend-change--up strong {
  color: #2f855a;
}

.trend-change--down strong {
  color: #c53030;
}

.trend-change--flat strong {
  color: #627d98;
}

.trend-insight {
  display: flex;
  align-items: center;
  gap: 7px;
  margin-bottom: 8px;
  color: #627d98;
  font-size: 12px;

  .q-icon {
    color: #1f6f8b;
  }
}

.trend-chart-shell {
  position: relative;
  min-height: 250px;
}

.trend-svg {
  display: block;
  width: 100%;
  height: 250px;
  overflow: visible;
}

.trend-y-axis {
  line {
    stroke: #e7eef2;
    stroke-dasharray: 3 5;
    stroke-width: 1;
    vector-effect: non-scaling-stroke;
  }

  text {
    fill: #9aabba;
    font-size: 11px;
    text-anchor: end;
  }
}

.trend-line {
  fill: none;
  stroke: #1f6f8b;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 3;
}

.trend-point {
  fill: #fff;
  stroke: #1f6f8b;
  stroke-width: 2.5;
  cursor: pointer;
  transition: r 0.15s ease;
  vector-effect: non-scaling-stroke;

  &:hover,
  &:focus-visible {
    r: 6;
    outline: none;
  }
}

.trend-point-ring {
  fill: #fff;
  stroke: #d99a2b;
  stroke-width: 2;
  vector-effect: non-scaling-stroke;
}

.trend-crosshair {
  stroke: #b7c9d3;
  stroke-dasharray: 3 4;
  stroke-width: 1;
  vector-effect: non-scaling-stroke;
}

.trend-tooltip {
  fill: #102a43;
  filter: drop-shadow(0 4px 8px rgba(16, 42, 67, 0.18));
}

.trend-tooltip-label {
  fill: #b7c9d3;
  font-size: 10px;
}

.trend-tooltip-value {
  fill: #fff;
  font-size: 13px;
  font-weight: 700;
}

.trend-x-axis {
  display: flex;
  justify-content: space-between;
  padding: 2px 14px 0 34px;
  color: #829ab1;
  font-size: 11px;
  white-space: nowrap;
}

.trend-empty {
  position: absolute;
  inset: 34px 0 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border-radius: 10px;
  background: rgba(245, 248, 250, 0.72);
  color: #829ab1;
  font-size: 13px;
}

@media (max-width: 600px) {
  .trend-summary {
    display: block;
  }

  .trend-secondary-metrics {
    justify-content: space-between;
    margin-top: 14px;
  }

  .trend-secondary-metric {
    text-align: left;
  }

  .trend-secondary-label {
    font-size: 10px;
  }

  .trend-x-axis {
    font-size: 10px;
  }
}
</style>
