<template>
  <q-page class="notifications-page">
    <NotificationToolbar
      :loading="loading"
      :marking-all="markingAll"
      :unseen-count="unseenCount"
      @refresh="load"
      @mark-all-seen="markAllSeen"
    />
    <NotificationFilters
      :active-tab="activeTab"
      :search="search"
      :total-count="notifications.length"
      :unseen-count="unseenCount"
      :seen-count="seenCount"
      @update:active-tab="activeTab = $event"
      @update:search="search = $event"
    />
    <NotificationList
      :notifications="filteredNotifications"
      :loading="loading"
      :updating-ids="updatingIds"
      @open="openNotification"
      @set-seen="setSeen"
    />
  </q-page>
</template>

<script setup lang="ts">
import NotificationFilters from "./components/NotificationFilters.vue";
import NotificationList from "./components/NotificationList.vue";
import NotificationToolbar from "./components/NotificationToolbar.vue";
import { useNotifications } from "./composables/useNotifications";

defineOptions({ name: "NotificationsPage" });

const {
  notifications,
  filteredNotifications,
  activeTab,
  search,
  unseenCount,
  seenCount,
  loading,
  updatingIds,
  markingAll,
  load,
  setSeen,
  markAllSeen,
  openNotification
} = useNotifications();
</script>

<style lang="scss" scoped>
.notifications-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}
@media (max-width: 700px) {
  .notifications-page {
    padding: 16px;
  }
}
</style>
