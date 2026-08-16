import { ref } from "vue";
import { useQuasar } from "quasar";
import { adminApi, type AdminOverview } from "@/api/admin";

const emptyOverview = (): AdminOverview => ({
  total_users: 0,
  active_users: 0,
  blocked_users: 0,
  registrations_today: 0,
  new_users_last_7_days: 0,
  new_users_last_30_days: 0,
  role_counts: [],
  registrations_by_day: [],
  registrations_by_month: [],
  registrations_by_year: [],
  recent_users: []
});

export function useAdminDashboard() {
  const $q = useQuasar();
  const overview = ref<AdminOverview>(emptyOverview());
  const loading = ref(false);

  async function load() {
    loading.value = true;
    try {
      overview.value = await adminApi.overview();
    } catch {
      $q.notify({
        type: "negative",
        message: "Could not load user administration overview"
      });
    } finally {
      loading.value = false;
    }
  }

  return { overview, loading, load };
}
