<template>
  <div v-if="items.length > 0" class="list-wrap">
    <router-link
      v-for="item in items"
      :key="item.id"
      :to="{ name: 'opportunities' }"
      class="row-item"
    >
      <span
        class="status-dot"
        :style="{ background: statusColor(item.status) }"
      ></span>
      <div class="row-main">
        <div class="row-title">{{ item.title }}</div>
        <div class="row-sub">{{ statusLabel(item.status) }}</div>
      </div>
      <span class="row-date">{{ formatDate(item.created_at) }}</span>
    </router-link>
  </div>
  <div v-else class="empty-state">
    <q-icon name="work_outline" size="28px" color="grey-4" />
    <div>No opportunities yet</div>
  </div>
</template>

<script setup lang="ts">
import type { Opportunity, OpportunityStatus } from "@/api/opportunities";
import {
  OPPORTUNITY_STATUS_COLORS,
  OPPORTUNITY_STATUS_LABELS
} from "@/modules/shared/statusColors";
import { formatDate } from "../utils";

defineOptions({ name: "RecentOpportunities" });

defineProps<{
  items: Opportunity[];
}>();

function statusColor(status: OpportunityStatus): string {
  return OPPORTUNITY_STATUS_COLORS[status];
}

function statusLabel(status: OpportunityStatus): string {
  return OPPORTUNITY_STATUS_LABELS[status];
}
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
  padding: 12px 8px;
  border-bottom: 1px solid #f1f5f9;
  border-radius: 8px;
  text-decoration: none;
  transition: background 0.15s ease;

  &:last-child {
    border-bottom: none;
  }

  &:hover {
    background: #f8fafc;
  }
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
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
