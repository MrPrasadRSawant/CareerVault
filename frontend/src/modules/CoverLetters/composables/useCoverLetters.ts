import { computed, onMounted, reactive, ref } from "vue";
import { useQuasar } from "quasar";
import { coverLetterApi } from "@/api/coverLetters";
import { defaultCoverLetterFilters, tabMatches } from "../utils";
import type {
  CoverLetterFilters,
  CoverLetterRow,
  CoverLetterTabKey
} from "../types";

export function useCoverLetters() {
  const $q = useQuasar();
  const letters = ref<CoverLetterRow[]>([]);
  const loading = ref(false);
  const saving = ref(false);
  const activeTab = ref<CoverLetterTabKey>("all");
  const filters = reactive<CoverLetterFilters>(defaultCoverLetterFilters());

  const filteredRows = computed(() =>
    letters.value.filter(row => {
      const search = filters.search.trim().toLowerCase();
      const haystack = [row.name, row.file_name, row.content]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      if (search && !haystack.includes(search)) return false;
      if (!tabMatches(row, activeTab.value)) return false;
      const createdDate = row.created_at.slice(0, 10);
      if (filters.createdFrom && createdDate < filters.createdFrom) return false;
      if (filters.createdTo && createdDate > filters.createdTo) return false;
      return true;
    })
  );

  const tabCounts = computed<Record<CoverLetterTabKey, number>>(() => ({
    all: letters.value.length,
    "with-content": letters.value.filter(row => tabMatches(row, "with-content")).length,
    empty: letters.value.filter(row => tabMatches(row, "empty")).length
  }));

  async function load(): Promise<void> {
    loading.value = true;
    try {
      letters.value = await coverLetterApi.list();
    } catch {
      $q.notify({ type: "negative", message: "Could not load cover letters" });
    } finally {
      loading.value = false;
    }
  }

  function clearFilters(): void {
    Object.assign(filters, defaultCoverLetterFilters());
    activeTab.value = "all";
  }

  async function createLetter(payload: {
    name: string;
    content: string | null;
  }): Promise<boolean> {
    saving.value = true;
    try {
      const created = await coverLetterApi.create(payload);
      letters.value.unshift(created);
      $q.notify({ type: "positive", message: "Letter created" });
      return true;
    } catch {
      $q.notify({ type: "negative", message: "Could not create letter" });
      return false;
    } finally {
      saving.value = false;
    }
  }

  async function updateLetter(
    id: string,
    payload: { name: string; content: string | null }
  ): Promise<boolean> {
    saving.value = true;
    try {
      const updated = await coverLetterApi.update(id, payload);
      const index = letters.value.findIndex(l => l.id === id);
      if (index !== -1) letters.value[index] = updated;
      $q.notify({ type: "positive", message: "Letter updated" });
      return true;
    } catch {
      $q.notify({ type: "negative", message: "Could not update letter" });
      return false;
    } finally {
      saving.value = false;
    }
  }

  async function deleteLetter(row: CoverLetterRow): Promise<void> {
    const confirmed = await new Promise<boolean>(resolve => {
      $q.dialog({
        title: "Delete letter?",
        message: `Remove "${row.name}"? This cannot be undone.`,
        cancel: true,
        persistent: true
      })
        .onOk(() => resolve(true))
        .onCancel(() => resolve(false));
    });
    if (!confirmed) return;
    try {
      await coverLetterApi.remove(row.id);
      letters.value = letters.value.filter(l => l.id !== row.id);
      $q.notify({ type: "positive", message: "Letter deleted" });
    } catch {
      $q.notify({ type: "negative", message: "Could not delete letter" });
    }
  }

  onMounted(load);

  return {
    letters,
    filteredRows,
    tabCounts,
    filters,
    activeTab,
    loading,
    saving,
    load,
    clearFilters,
    createLetter,
    updateLetter,
    deleteLetter
  };
}
