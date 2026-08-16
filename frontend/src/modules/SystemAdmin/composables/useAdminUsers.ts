import { computed, ref, watch } from "vue";
import { useQuasar } from "quasar";
import { adminApi, type AdminUser, type AdminUserQuery } from "@/api/admin";
import type { UserRole } from "@/api/auth";

export function useAdminUsers() {
  const $q = useQuasar();
  const users = ref<AdminUser[]>([]);
  const total = ref(0);
  const loading = ref(false);
  const updatingIds = ref<string[]>([]);
  const search = ref("");
  const activeFilter = ref<boolean | null>(null);
  const roleFilter = ref<UserRole | null>(null);
  const page = ref(1);
  const pageSize = 20;
  const pageCount = computed(() =>
    Math.max(1, Math.ceil(total.value / pageSize))
  );

  async function load() {
    loading.value = true;
    const query: AdminUserQuery = {
      limit: pageSize,
      offset: (page.value - 1) * pageSize
    };
    const normalizedSearch = search.value.trim();
    if (normalizedSearch) query.search = normalizedSearch;
    if (activeFilter.value !== null) query.is_active = activeFilter.value;
    if (roleFilter.value !== null) query.role = roleFilter.value;
    try {
      const response = await adminApi.users(query);
      users.value = response.items;
      total.value = response.total;
    } catch {
      $q.notify({
        type: "negative",
        message: "Could not load user accounts"
      });
    } finally {
      loading.value = false;
    }
  }

  function clearFilters() {
    search.value = "";
    activeFilter.value = null;
    roleFilter.value = null;
  }

  function confirmStatusChange(user: AdminUser) {
    if (user.role === "system_admin") {
      $q.notify({
        type: "warning",
        message: "System administrator accounts are protected"
      });
      return;
    }
    const nextActive = !user.is_active;
    $q.dialog({
      title: nextActive ? "Unblock user?" : "Block user?",
      message: nextActive
        ? `${user.full_name} will be able to sign in again.`
        : `${user.full_name} will be unable to sign in. Their account data will be preserved.`,
      cancel: true,
      persistent: true,
      ok: {
        label: nextActive ? "Unblock" : "Block",
        color: nextActive ? "primary" : "negative",
        unelevated: true
      }
    }).onOk(async () => {
      updatingIds.value = [...updatingIds.value, user.id];
      try {
        const updated = await adminApi.setUserActive(user.id, nextActive);
        users.value = users.value.map(item =>
          item.id === updated.id ? updated : item
        );
        $q.notify({
          type: "positive",
          message: nextActive
            ? "User account unblocked"
            : "User account blocked"
        });
      } catch {
        $q.notify({
          type: "negative",
          message: "Could not update account access"
        });
      } finally {
        updatingIds.value = updatingIds.value.filter(id => id !== user.id);
      }
    });
  }

  watch([search, activeFilter, roleFilter], () => {
    if (page.value !== 1) page.value = 1;
    else void load();
  });
  watch(page, () => void load());

  return {
    users,
    total,
    loading,
    updatingIds,
    search,
    activeFilter,
    roleFilter,
    page,
    pageCount,
    load,
    clearFilters,
    confirmStatusChange
  };
}
