<template>
  <div v-if="items.length > 0" class="list-wrap">
    <div v-for="item in items" :key="item.id" class="row-item">
      <div class="icon-block">
        <q-icon name="schedule" size="18px" />
      </div>
      <div class="row-main">
        <div class="row-title">{{ item.subject || "Follow-up" }}</div>
        <div class="row-sub">Application #{{ item.application_id }}</div>
      </div>
      <span class="row-date">{{ formatDate(item.scheduled_at) }}</span>
    </div>
  </div>
  <div v-else class="empty-state">
    <q-icon name="event_repeat" size="28px" color="grey-4" />
    <div>No pending follow-ups</div>
  </div>
</template>

<script setup lang="ts">
import type { FollowUp } from "@/api/followUps";
import { formatDate } from "../utils";

defineOptions({ name: "FollowUpsCard" });

defineProps<{
  items: FollowUp[];
}>();
</script>

<style lang="scss" scoped>
.list-wrap {
  display: flex;
  flex-direction: column;
}

.row-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f1f5f9;

  &:last-child {
    border-bottom: none;
  }
}

.icon-block {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: rgba(255, 183, 3, 0.15);
  color: #b98b00;
  flex-shrink: 0;
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
}

.row-date {
  font-size: 12px;
  color: #94a3b8;
  white-space: nowrap;
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
