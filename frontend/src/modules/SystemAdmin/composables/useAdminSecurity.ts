import { computed, ref, watch } from "vue";
import { useQuasar } from "quasar";
import { useRoute } from "vue-router";
import {
  adminApi,
  type AdminAuthSession,
  type AdminAuthSessionQuery,
  type AdminLoginEvent,
  type AdminLoginEventQuery,
  type AdminSecurityOverview,
  type AuthOutcome
} from "@/api/admin";
import type { UserRole } from "@/api/auth";

const emptyOverview = (): AdminSecurityOverview => ({
  successful_logins_last_24_hours: 0,
  failed_logins_last_24_hours: 0,
  active_sessions: 0,
  retention_days: 0
});

export function useAdminSecurity() {
  const $q = useQuasar();
  const route = useRoute();
  const overview = ref<AdminSecurityOverview>(emptyOverview());
  const events = ref<AdminLoginEvent[]>([]);
  const sessions = ref<AdminAuthSession[]>([]);
  const total = ref(0);
  const loading = ref(false);
  const tab = ref<"events" | "sessions">("events");
  const search = ref(
    typeof route.query.search === "string" ? route.query.search : ""
  );
  const roleFilter = ref<UserRole | null>(null);
  const outcomeFilter = ref<AuthOutcome | null>(null);
  const page = ref(1);
  const pageSize = 20;
  const pageCount = computed(() =>
    Math.max(1, Math.ceil(total.value / pageSize))
  );

  async function loadOverview() {
    overview.value = await adminApi.securityOverview();
  }

  async function loadTable() {
    const common = {
      limit: pageSize,
      offset: (page.value - 1) * pageSize
    };
    const normalizedSearch = search.value.trim();
    if (tab.value === "events") {
      const query: AdminLoginEventQuery = { ...common };
      if (normalizedSearch) query.search = normalizedSearch;
      if (roleFilter.value !== null) query.role = roleFilter.value;
      if (outcomeFilter.value !== null) query.outcome = outcomeFilter.value;
      const response = await adminApi.loginEvents(query);
      events.value = response.items;
      total.value = response.total;
    } else {
      const query: AdminAuthSessionQuery = { ...common };
      if (normalizedSearch) query.search = normalizedSearch;
      if (roleFilter.value !== null) query.role = roleFilter.value;
      const response = await adminApi.authSessions(query);
      sessions.value = response.items;
      total.value = response.total;
    }
  }

  async function load() {
    loading.value = true;
    try {
      await Promise.all([loadOverview(), loadTable()]);
    } catch {
      $q.notify({
        type: "negative",
        message: "Could not load authentication activity"
      });
    } finally {
      loading.value = false;
    }
  }

  function clearFilters() {
    search.value = "";
    roleFilter.value = null;
    outcomeFilter.value = null;
  }

  watch([tab, search, roleFilter, outcomeFilter], () => {
    if (page.value !== 1) page.value = 1;
    else void loadTable();
  });
  watch(page, () => void loadTable());

  return {
    overview,
    events,
    sessions,
    total,
    loading,
    tab,
    search,
    roleFilter,
    outcomeFilter,
    page,
    pageCount,
    load,
    clearFilters
  };
}
