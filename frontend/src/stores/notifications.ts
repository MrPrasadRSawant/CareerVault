import { computed, ref } from "vue";
import { defineStore } from "pinia";
import { notificationApi } from "@/api/notifications";

export const useNotificationStore = defineStore("notifications", () => {
  const unseenCount = ref(0);
  const loadingCount = ref(false);
  const badgeLabel = computed(() =>
    unseenCount.value > 99 ? "99+" : String(unseenCount.value)
  );

  async function refreshUnseenCount(): Promise<void> {
    if (!localStorage.getItem("cv_token") || loadingCount.value) return;
    loadingCount.value = true;
    try {
      unseenCount.value = await notificationApi.unseenCount();
    } catch {
      // The badge is supplementary; API errors are handled on the list page.
    } finally {
      loadingCount.value = false;
    }
  }

  function clear(): void {
    unseenCount.value = 0;
  }

  return { unseenCount, badgeLabel, refreshUnseenCount, clear };
});
