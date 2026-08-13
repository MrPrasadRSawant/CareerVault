import { computed, onMounted, ref } from "vue";
import { useQuasar } from "quasar";
import { useRouter } from "vue-router";
import { notificationApi, type Notification } from "@/api/notifications";
import { useNotificationStore } from "@/stores/notifications";
import type { NotificationTab } from "../types";

export function useNotifications() {
  const $q = useQuasar();
  const router = useRouter();
  const notificationStore = useNotificationStore();
  const notifications = ref<Notification[]>([]);
  const activeTab = ref<NotificationTab>("all");
  const search = ref("");
  const loading = ref(false);
  const updatingIds = ref<string[]>([]);
  const markingAll = ref(false);

  const unseenCount = computed(
    () => notifications.value.filter(item => !item.is_seen).length
  );
  const seenCount = computed(
    () => notifications.value.filter(item => item.is_seen).length
  );
  const filteredNotifications = computed(() => {
    const query = search.value.trim().toLowerCase();
    return notifications.value.filter(notification => {
      if (activeTab.value === "unseen" && notification.is_seen) return false;
      if (activeTab.value === "seen" && !notification.is_seen) return false;
      if (!query) return true;
      return [notification.title, notification.message]
        .join(" ")
        .toLowerCase()
        .includes(query);
    });
  });

  async function load(): Promise<void> {
    loading.value = true;
    try {
      notifications.value = await notificationApi.list();
      await notificationStore.refreshUnseenCount();
    } catch {
      $q.notify({ type: "negative", message: "Could not load notifications" });
    } finally {
      loading.value = false;
    }
  }

  async function setSeen(notification: Notification, isSeen: boolean) {
    if (notification.is_seen === isSeen) return;
    updatingIds.value = [...updatingIds.value, notification.id];
    try {
      const updated = await notificationApi.setSeen(notification.id, isSeen);
      const index = notifications.value.findIndex(
        item => item.id === updated.id
      );
      if (index !== -1) notifications.value[index] = updated;
      await notificationStore.refreshUnseenCount();
    } catch {
      $q.notify({
        type: "negative",
        message: "Could not update notification status"
      });
    } finally {
      updatingIds.value = updatingIds.value.filter(
        id => id !== notification.id
      );
    }
  }

  async function markAllSeen(): Promise<void> {
    if (!unseenCount.value) return;
    markingAll.value = true;
    try {
      await notificationApi.markAllSeen();
      notifications.value = notifications.value.map(notification => ({
        ...notification,
        is_seen: true,
        seen_at: notification.seen_at ?? new Date().toISOString()
      }));
      await notificationStore.refreshUnseenCount();
      $q.notify({
        type: "positive",
        message: "All notifications marked as seen"
      });
    } catch {
      $q.notify({
        type: "negative",
        message: "Could not mark notifications as seen"
      });
    } finally {
      markingAll.value = false;
    }
  }

  async function openNotification(notification: Notification): Promise<void> {
    if (!notification.is_seen) await setSeen(notification, true);
    await router.push(notification.action_path);
  }

  onMounted(load);

  return {
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
  };
}
