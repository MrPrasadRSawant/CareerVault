<template>
  <q-card flat bordered class="notification-card">
    <q-inner-loading :showing="loading" color="primary" />

    <div v-if="!loading && notifications.length === 0" class="empty-state">
      <div class="empty-icon"
        ><q-icon name="notifications_none" size="34px"
      /></div>
      <div class="empty-title">No notifications found</div>
      <div class="empty-copy">
        New opportunities and recruiter responses will appear here.
      </div>
    </div>

    <q-list v-else separator class="notification-list">
      <q-item
        v-for="notification in notifications"
        :key="notification.id"
        class="notification-item"
        :class="{ 'notification-item--unseen': !notification.is_seen }"
      >
        <q-item-section avatar top>
          <div
            class="type-icon"
            :style="{
              color: typeDetails(notification.type).color,
              background: typeDetails(notification.type).background
            }"
          >
            <q-icon :name="typeDetails(notification.type).icon" size="21px" />
          </div>
        </q-item-section>

        <q-item-section>
          <div class="item-heading">
            <q-item-label class="notification-title">
              {{ notification.title }}
            </q-item-label>
            <span
              v-if="!notification.is_seen"
              class="unseen-dot"
              aria-label="Unseen"
            />
          </div>
          <q-item-label class="notification-message">
            {{ notification.message }}
          </q-item-label>
          <div class="notification-meta">
            <span class="type-label">{{
              typeDetails(notification.type).label
            }}</span>
            <span aria-hidden="true">·</span>
            <span>{{ formatNotificationDate(notification.created_at) }}</span>
            <span aria-hidden="true">·</span>
            <span :class="notification.is_seen ? 'seen-label' : 'unseen-label'">
              {{ notification.is_seen ? "Seen" : "Unseen" }}
            </span>
          </div>
        </q-item-section>

        <q-item-section side top class="item-actions">
          <q-btn
            flat
            no-caps
            dense
            color="primary"
            icon="open_in_new"
            label="Open"
            @click="$emit('open', notification)"
          />
          <q-btn
            flat
            no-caps
            dense
            :icon="notification.is_seen ? 'mark_email_unread' : 'done'"
            :label="notification.is_seen ? 'Mark unseen' : 'Mark seen'"
            :color="notification.is_seen ? 'blue-grey-7' : 'primary'"
            :loading="updatingIds.includes(notification.id)"
            @click="$emit('set-seen', notification, !notification.is_seen)"
          />
        </q-item-section>
      </q-item>
    </q-list>
  </q-card>
</template>

<script setup lang="ts">
import type { Notification, NotificationType } from "@/api/notifications";
import { formatNotificationDate, notificationTypeDetails } from "../utils";

defineProps<{
  notifications: Notification[];
  loading: boolean;
  updatingIds: string[];
}>();
defineEmits<{
  (event: "open", notification: Notification): void;
  (event: "set-seen", notification: Notification, isSeen: boolean): void;
}>();

function typeDetails(type: NotificationType) {
  return notificationTypeDetails[type];
}
</script>

<style lang="scss" scoped>
.notification-card {
  position: relative;
  min-height: 180px;
  overflow: hidden;
  border-color: var(--cv-border);
  border-radius: 14px;
  box-shadow: var(--cv-shadow-card);
}
.notification-item {
  min-height: 112px;
  padding: 18px 20px;
  background: var(--cv-surface);
  transition: background 0.18s ease;
}
.notification-item--unseen {
  border-left: 3px solid var(--cv-primary);
  background: linear-gradient(90deg, #f1f8fb 0%, var(--cv-surface) 34%);
  padding-left: 17px;
}
.notification-item:hover {
  background: var(--cv-surface-soft);
}
.type-icon {
  display: grid;
  width: 42px;
  height: 42px;
  place-items: center;
  border-radius: 12px;
}
.item-heading {
  display: flex;
  align-items: center;
  gap: 8px;
}
.notification-title {
  color: var(--cv-navy);
  font-size: 14px;
  font-weight: 750;
}
.unseen-dot {
  width: 8px;
  height: 8px;
  flex: 0 0 auto;
  border-radius: 50%;
  background: var(--cv-primary);
  box-shadow: 0 0 0 3px rgba(31, 111, 139, 0.12);
}
.notification-message {
  max-width: 780px;
  margin-top: 5px;
  color: var(--cv-text-strong);
  font-size: 13px;
  line-height: 1.5;
}
.notification-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 9px;
  color: var(--cv-muted-light);
  font-size: 11px;
}
.type-label {
  font-weight: 700;
}
.unseen-label {
  color: var(--cv-primary-dark);
  font-weight: 700;
}
.seen-label {
  color: var(--cv-muted-light);
}
.item-actions {
  display: flex;
  align-items: flex-end;
  gap: 2px;
  min-width: 126px;
}
.empty-state {
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
  min-height: 260px;
  padding: 30px;
  text-align: center;
}
.empty-icon {
  display: grid;
  width: 64px;
  height: 64px;
  place-items: center;
  border-radius: 18px;
  background: var(--cv-primary-soft);
  color: var(--cv-primary);
}
.empty-title {
  margin-top: 14px;
  color: var(--cv-navy);
  font-size: 16px;
  font-weight: 750;
}
.empty-copy {
  margin-top: 4px;
  color: var(--cv-muted-light);
  font-size: 12px;
}
@media (max-width: 700px) {
  .notification-item {
    align-items: flex-start;
    flex-wrap: wrap;
    padding: 16px;
  }
  .notification-item--unseen {
    padding-left: 13px;
  }
  .item-actions {
    width: 100%;
    align-items: center;
    flex-direction: row;
    justify-content: flex-end;
    padding-top: 8px;
  }
}
</style>
