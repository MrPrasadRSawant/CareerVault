<template>
  <div class="admin-stat-card">
    <div class="stat-heading">
      <span
        class="stat-icon"
        :style="{ color: accent, background: `${accent}16` }"
      >
        <q-icon :name="icon" size="21px" />
      </span>
      <span v-if="badge" class="stat-badge">{{ badge }}</span>
    </div>
    <div class="stat-value">{{ value }}</div>
    <div class="stat-label">{{ label }}</div>
    <div class="stat-hint">{{ hint }}</div>
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: "AdminStatCard" });

defineProps<{
  icon: string;
  value: number;
  label: string;
  hint: string;
  accent: string;
  badge?: string;
}>();
</script>

<style lang="scss" scoped>
.admin-stat-card {
  height: 100%;
  padding: 18px;
  border: 1px solid #dfe4ea;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 1px 2px rgba(30, 42, 56, 0.04);
}
.stat-heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}
.stat-icon {
  display: grid;
  place-items: center;
  width: 39px;
  height: 39px;
  border-radius: 10px;
}
.stat-badge {
  padding: 4px 7px;
  border-radius: 999px;
  color: #287a56;
  background: #edf8f3;
  font-size: 9.5px;
  font-weight: 750;
}
.stat-value {
  margin-top: 15px;
  color: #172033;
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -0.8px;
  line-height: 1;
}
.stat-label {
  margin-top: 5px;
  color: #445166;
  font-size: 12.5px;
  font-weight: 700;
}
.stat-hint {
  margin-top: 3px;
  color: #929cab;
  font-size: 10.5px;
}
</style>
