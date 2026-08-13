import { computed, onMounted, reactive, ref } from "vue";
import { useQuasar } from "quasar";
import { applicationApi } from "@/api/applications";
import {
  emailFollowUpApi,
  type EmailFollowUp,
  type EmailFollowUpGroup,
  type EmailFollowUpPayload
} from "@/api/emailFollowUps";
import { opportunityApi } from "@/api/opportunities";
import { useNotificationStore } from "@/stores/notifications";
import type { ApplicationChoice, EmailFollowUpFilters } from "../types";

export function useEmailFollowUps() {
  const $q = useQuasar();
  const notificationStore = useNotificationStore();
  const groups = ref<EmailFollowUpGroup[]>([]);
  const applicationChoices = ref<ApplicationChoice[]>([]);
  const loading = ref(false);
  const saving = ref(false);
  const filters = reactive<EmailFollowUpFilters>({
    search: "",
    outcome: "all"
  });

  const filteredGroups = computed(() => {
    const query = filters.search.trim().toLowerCase();
    return groups.value.filter(group => {
      if (
        filters.outcome !== "all" &&
        !group.emails.some(email => email.outcome === filters.outcome)
      ) {
        return false;
      }
      if (!query) return true;
      const text = [
        group.opportunity_title,
        group.company_name,
        ...group.emails.flatMap(email => [
          email.subject,
          email.sender_email,
          email.sender_name,
          email.reason,
          email.reason_category
        ])
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      return text.includes(query);
    });
  });

  async function load(): Promise<void> {
    loading.value = true;
    try {
      const [groupList, applications, opportunities] = await Promise.all([
        emailFollowUpApi.list(),
        applicationApi.list(),
        opportunityApi.list()
      ]);
      groups.value = groupList;
      applicationChoices.value = applications.map(application => {
        const opportunity = opportunities.find(
          item => item.id === application.opportunity_id
        );
        const title = opportunity?.title ?? "Unknown opportunity";
        const company = opportunity?.company_name
          ? ` · ${opportunity.company_name}`
          : "";
        return { applicationId: application.id, label: `${title}${company}` };
      });
    } catch {
      $q.notify({
        type: "negative",
        message: "Could not load email follow-ups"
      });
    } finally {
      loading.value = false;
    }
  }

  async function create(payload: EmailFollowUpPayload): Promise<boolean> {
    saving.value = true;
    try {
      await emailFollowUpApi.create(payload);
      await load();
      await notificationStore.refreshUnseenCount();
      $q.notify({ type: "positive", message: "Email follow-up recorded" });
      return true;
    } catch {
      $q.notify({
        type: "negative",
        message: "Could not record email follow-up"
      });
      return false;
    } finally {
      saving.value = false;
    }
  }

  async function update(
    email: EmailFollowUp,
    payload: EmailFollowUpPayload
  ): Promise<boolean> {
    saving.value = true;
    try {
      await emailFollowUpApi.update(email.id, payload);
      await load();
      $q.notify({ type: "positive", message: "Email follow-up updated" });
      return true;
    } catch {
      $q.notify({
        type: "negative",
        message: "Could not update email follow-up"
      });
      return false;
    } finally {
      saving.value = false;
    }
  }

  async function remove(email: EmailFollowUp): Promise<void> {
    const confirmed = await new Promise<boolean>(resolve => {
      $q.dialog({
        title: "Delete email follow-up?",
        message: `Remove “${email.subject}” from this application’s email chain?`,
        cancel: true,
        persistent: true
      })
        .onOk(() => resolve(true))
        .onCancel(() => resolve(false));
    });
    if (!confirmed) return;
    try {
      await emailFollowUpApi.remove(email.id);
      await load();
      $q.notify({ type: "positive", message: "Email follow-up deleted" });
    } catch {
      $q.notify({
        type: "negative",
        message: "Could not delete email follow-up"
      });
    }
  }

  function clearFilters(): void {
    filters.search = "";
    filters.outcome = "all";
  }

  onMounted(load);

  return {
    groups,
    filteredGroups,
    applicationChoices,
    filters,
    loading,
    saving,
    load,
    create,
    update,
    remove,
    clearFilters
  };
}
