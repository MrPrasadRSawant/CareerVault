<template>
  <div class="funnel-wrap" role="list" aria-label="Application conversion funnel">
    <div v-for="(stage, index) in stages" :key="stage.label" class="funnel-stage" role="listitem">
      <div class="funnel-stage-header">
        <div class="funnel-stage-name">
          <span class="funnel-index">{{ index + 1 }}</span>
          <span>{{ stage.label }}</span>
        </div>
        <div class="funnel-stage-result">
          <strong>{{ stage.value }}</strong>
          <span>{{ stage.percent }}%</span>
        </div>
      </div>
      <div
        class="funnel-track"
        role="progressbar"
        :aria-label="`${stage.label}: ${stage.value} of ${total}`"
        :aria-valuenow="stage.percent"
        aria-valuemin="0"
        aria-valuemax="100"
      >
        <div
          class="funnel-fill"
          :style="{ width: `${stageWidth(stage)}%`, background: stage.color }"
        ></div>
      </div>
      <div v-if="index > 0" class="funnel-stage-note">
        {{ stage.percent }}% of all applications reached this stage
      </div>
    </div>

    <div v-if="total > 0" class="funnel-insight">
      <q-icon name="priority_high" size="16px" />
      <span>
        Biggest drop-off: {{ bottleneck.from }} → {{ bottleneck.to }}
        ({{ bottleneck.loss }} applications)
      </span>
    </div>

    <div v-if="total === 0" class="funnel-empty">
      Add your first application to start measuring conversion through your job search.
    </div>
  </div>
</template>

<script setup lang="ts">
import type { FunnelDatum } from "../composables/useDashboard";
import { computed } from "vue";

defineOptions({ name: "ApplicationFunnel" });

const props = defineProps<{
  stages: FunnelDatum[];
}>();

const total = computed(() => props.stages[0]?.value ?? 0);

function stageWidth(stage: FunnelDatum): number {
  if (total.value === 0 || stage.value === 0) return 0;
  return Math.max(3, stage.percent);
}

const bottleneck = computed(() => {
  let largestLoss = 0;
  let from = props.stages[0]?.label ?? "Applications";
  let to = props.stages[1]?.label ?? "Responses";

  for (let index = 1; index < props.stages.length; index += 1) {
    const previous = props.stages[index - 1]!;
    const current = props.stages[index]!;
    const loss = Math.max(0, previous.value - current.value);
    if (loss > largestLoss) {
      largestLoss = loss;
      from = previous.label;
      to = current.label;
    }
  }

  return { from, to, loss: largestLoss };
});
</script>

<style lang="scss" scoped>
.funnel-wrap {
  display: flex;
  flex-direction: column;
  gap: 17px;
}

.funnel-stage {
  display: flex;
  flex-direction: column;
  gap: 7px;
}

.funnel-stage-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.funnel-stage-name,
.funnel-stage-result {
  display: flex;
  align-items: center;
  gap: 8px;
}

.funnel-stage-name {
  color: #243b53;
  font-size: 13.5px;
  font-weight: 600;
}

.funnel-index {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border: 1px solid #dce6eb;
  border-radius: 50%;
  color: #627d98;
  font-size: 11px;
  font-weight: 700;
}

.funnel-stage-result {
  strong {
    color: #102a43;
    font-size: 16px;
  }

  span {
    min-width: 36px;
    color: #829ab1;
    font-size: 12px;
    text-align: right;
  }
}

.funnel-track {
  height: 11px;
  margin-left: 30px;
  border-radius: 6px;
  background: #edf2f5;
  overflow: hidden;
}

.funnel-fill {
  height: 100%;
  min-width: 3px;
  border-radius: 6px;
  transition: width 0.45s ease;
}

.funnel-stage-note {
  margin-left: 30px;
  color: #829ab1;
  font-size: 11px;
}

.funnel-empty {
  padding: 30px 18px;
  border: 1px dashed #cbd8df;
  border-radius: 10px;
  color: #627d98;
  font-size: 13px;
  line-height: 1.5;
  text-align: center;
}

.funnel-insight {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 2px;
  padding: 10px 12px;
  border-radius: 8px;
  background: #fff8e8;
  color: #8a641c;
  font-size: 12px;

  .q-icon {
    color: #b7791f;
  }
}
</style>
