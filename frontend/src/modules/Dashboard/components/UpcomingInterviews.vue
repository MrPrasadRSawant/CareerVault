<template>
  <div v-if="items.length > 0" class="list-wrap">
    <div v-for="item in items" :key="item.id" class="row-item">
      <div class="date-block">
        <div class="date-day">{{ dayMonth(item.scheduled_at) }}</div>
        <div class="date-time">{{ time(item.scheduled_at) }}</div>
      </div>
      <div class="row-main">
        <div class="row-title">{{ item.title }}</div>
        <div v-if="item.type" class="row-sub">{{ item.type }}</div>
      </div>
      <q-icon name="chevron_right" size="18px" class="row-chevron" />
    </div>
  </div>
  <div v-else class="empty-state">
    <q-icon name="event_available" size="28px" color="grey-4" />
    <div>No upcoming interviews</div>
  </div>
</template>

<script setup lang="ts">
import { formatDayMonth, formatTime } from "../utils";
import type { UpcomingInterviewRow } from "../composables/useDashboard";

defineOptions({ name: "UpcomingInterviews" });

defineProps<{
  items: UpcomingInterviewRow[];
}>();

const dayMonth = formatDayMonth;
const time = formatTime;
</script>

<style lang="scss" scoped>
.list-wrap {
  display: flex;
  flex-direction: column;
}

.row-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 0;
  border-bottom: 1px solid #f1f5f9;

  &:last-child {
    border-bottom: none;
  }
}

.date-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 58px;
  padding: 6px 0;
  border-radius: 10px;
  background: rgba(33, 158, 188, 0.1);
  color: #219ebc;
}

.date-day {
  font-size: 13px;
  font-weight: 700;
  line-height: 1.2;
}

.date-time {
  font-size: 11px;
  color: #1b7f99;
}

.row-main {
  flex: 1;
  min-width: 0;
}

.row-title {
  font-size: 14px;
  font-weight: 600;
  color: #023047;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.row-sub {
  margin-top: 2px;
  font-size: 12.5px;
  color: #94a3b8;
  text-transform: capitalize;
}

.row-chevron {
  color: #cbd5e1;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 28px 0;
  font-size: 13px;
  color: #94a3b8;
}
</style>
