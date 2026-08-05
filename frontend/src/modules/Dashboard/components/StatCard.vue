<template>
  <router-link :to="to" class="stat-card">
    <div
      class="stat-icon"
      :style="{ background: accent + '22', color: accent }"
    >
      <q-icon :name="icon" size="22px" />
    </div>
    <div class="stat-value">{{ value }}</div>
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
  hint: string;
  accent: string;
  to: RouteLocationRaw;
}>();
</script>

<style lang="scss" scoped>
.stat-card {
  display: block;
  background: #fff;
  border: 1px solid #e6edf1;
  border-radius: 14px;
  padding: 20px;
  height: 100%;
  text-decoration: none;
  box-shadow: 0 1px 3px rgba(2, 48, 71, 0.06);
  transition:
    transform 0.15s ease,
    box-shadow 0.15s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(2, 48, 71, 0.1);
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
  color: #023047;
  line-height: 1.1;
}

.stat-label {
  margin-top: 4px;
  font-size: 13.5px;
  font-weight: 600;
  color: #475569;
}

.stat-hint {
  margin-top: 2px;
  font-size: 12px;
  color: #94a3b8;
}
</style>
