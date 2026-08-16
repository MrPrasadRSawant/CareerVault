<template>
  <router-link :to="to" class="stat-card">
    <div
      class="stat-icon"
      :style="{ background: accent + '22', color: accent }"
    >
      <q-icon :name="icon" size="22px" />
    </div>
    <div class="stat-value">
      {{ value
      }}<span v-if="valueSuffix" class="stat-value-suffix">{{
        valueSuffix
      }}</span>
    </div>
    <div class="stat-label">{{ label }}</div>
    <div class="stat-hint">{{ hint }}</div>
  </router-link>
</template>

<script setup lang="ts">
import type { RouteLocationRaw } from "vue-router";

defineOptions({ name: "StatCard" });

defineProps<{
  icon: string;
  label: string;
  value: number;
  valueSuffix?: string;
  hint: string;
  accent: string;
  to: RouteLocationRaw;
}>();
</script>

<style lang="scss" scoped>
.stat-card {
  display: block;
  background: #fff;
  border: 1px solid #dfe4ea;
  border-radius: 12px;
  padding: 18px;
  height: 100%;
  text-decoration: none;
  box-shadow: 0 1px 2px rgba(30, 42, 56, 0.04);
  transition:
    transform 0.15s ease,
    box-shadow 0.15s ease;

  &:hover {
    transform: translateY(-1px);
    border-color: #c8d5e8;
    box-shadow: 0 7px 18px rgba(30, 50, 80, 0.09);
  }
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 46px;
  height: 46px;
  border-radius: 12px;
  margin-bottom: 14px;
}

.stat-value {
  font-size: 30px;
  font-weight: 700;
  color: #172033;
  line-height: 1.1;
}

.stat-value-suffix {
  margin-left: 2px;
  font-size: 18px;
  font-weight: 600;
}

.stat-label {
  margin-top: 4px;
  font-size: 13.5px;
  font-weight: 600;
  color: #4f5b6c;
}

.stat-hint {
  margin-top: 2px;
  font-size: 12px;
  color: #8a95a5;
}
</style>
