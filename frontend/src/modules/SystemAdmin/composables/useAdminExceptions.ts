import { computed, ref } from "vue";
import {
  adminApi,
  type AdminExceptionLog,
  type AdminExceptionLogDetail,
  type AdminExceptionOverview
} from "@/api/admin";

const PAGE_SIZE = 25;

const emptyOverview = (): AdminExceptionOverview => ({
  exceptions_last_24_hours: 0,
  exceptions_last_7_days: 0,
  unique_fingerprints_last_24_hours: 0,
  retention_days: 0
});

export function useAdminExceptions() {
  const overview = ref<AdminExceptionOverview>(emptyOverview());
  const items = ref<AdminExceptionLog[]>([]);
  const detail = ref<AdminExceptionLogDetail | null>(null);
  const total = ref(0);
  const page = ref(1);
  const search = ref("");
  const loading = ref(false);
  const detailLoading = ref(false);
  const error = ref<string | null>(null);

  const maxPage = computed(() =>
    Math.max(1, Math.ceil(total.value / PAGE_SIZE))
  );

  async function loadLogs() {
    loading.value = true;
    error.value = null;
    try {
      const searchTerm = search.value.trim();
      const response = await adminApi.exceptionLogs({
        ...(searchTerm ? { search: searchTerm } : {}),
        limit: PAGE_SIZE,
        offset: (page.value - 1) * PAGE_SIZE
      });
      items.value = response.items;
      total.value = response.total;
    } catch {
      error.value = "Exception logs could not be loaded.";
    } finally {
      loading.value = false;
    }
  }

  async function load() {
    loading.value = true;
    error.value = null;
    try {
      const [overviewResponse, logsResponse] = await Promise.all([
        adminApi.exceptionOverview(),
        adminApi.exceptionLogs({ limit: PAGE_SIZE, offset: 0 })
      ]);
      overview.value = overviewResponse;
      items.value = logsResponse.items;
      total.value = logsResponse.total;
      page.value = 1;
    } catch {
      error.value = "Exception logs could not be loaded.";
    } finally {
      loading.value = false;
    }
  }

  async function applySearch() {
    page.value = 1;
    await loadLogs();
  }

  async function changePage(nextPage: number) {
    page.value = nextPage;
    await loadLogs();
  }

  async function openDetail(item: AdminExceptionLog) {
    detailLoading.value = true;
    detail.value = null;
    try {
      detail.value = await adminApi.exceptionLog(item.id);
    } finally {
      detailLoading.value = false;
    }
  }

  return {
    overview,
    items,
    detail,
    total,
    page,
    maxPage,
    search,
    loading,
    detailLoading,
    error,
    load,
    loadLogs,
    applySearch,
    changePage,
    openDetail
  };
}
