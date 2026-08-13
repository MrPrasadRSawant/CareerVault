<template>
  <q-page class="email-follow-ups-page">
    <EmailFollowUpToolbar
      :loading="loading"
      @refresh="load"
      @create="openCreate"
    />
    <EmailFollowUpFilters
      :filters="filters"
      :result-count="filteredGroups.length"
      @clear="clearFilters"
    />
    <EmailFollowUpGroupTable
      :groups="filteredGroups"
      :loading="loading"
      @view="openView"
      @edit="openEdit"
      @delete="remove"
    />
    <EmailFollowUpFormDialog
      v-model="showForm"
      :editing-email="editingEmail"
      :applications="applicationChoices"
      :saving="saving"
      @save="save"
    />
    <EmailFollowUpViewDialog
      v-model="showView"
      :email="viewedEmail"
      :application-label="viewedApplicationLabel"
      @edit="openEditFromView"
    />
  </q-page>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import type { EmailFollowUp, EmailFollowUpPayload } from "@/api/emailFollowUps";
import EmailFollowUpFilters from "./components/EmailFollowUpFilters.vue";
import EmailFollowUpFormDialog from "./components/EmailFollowUpFormDialog.vue";
import EmailFollowUpGroupTable from "./components/EmailFollowUpGroupTable.vue";
import EmailFollowUpToolbar from "./components/EmailFollowUpToolbar.vue";
import EmailFollowUpViewDialog from "./components/EmailFollowUpViewDialog.vue";
import { useEmailFollowUps } from "./composables/useEmailFollowUps";

defineOptions({ name: "EmailFollowUpsPage" });

const {
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
} = useEmailFollowUps();
const showForm = ref(false);
const showView = ref(false);
const editingEmail = ref<EmailFollowUp | null>(null);
const viewedEmail = ref<EmailFollowUp | null>(null);
const viewedApplicationLabel = computed(() => {
  const group = groups.value.find(
    item => item.application_id === viewedEmail.value?.application_id
  );
  return group
    ? `${group.opportunity_title}${group.company_name ? ` · ${group.company_name}` : ""}`
    : "Application email";
});

function openCreate() {
  editingEmail.value = null;
  showForm.value = true;
}

function openEdit(email: EmailFollowUp) {
  editingEmail.value = email;
  showForm.value = true;
}

function openView(email: EmailFollowUp) {
  viewedEmail.value = email;
  showView.value = true;
}

function openEditFromView(email: EmailFollowUp) {
  showView.value = false;
  openEdit(email);
}

async function save(payload: EmailFollowUpPayload) {
  const successful = editingEmail.value
    ? await update(editingEmail.value, payload)
    : await create(payload);
  if (successful) showForm.value = false;
}
</script>

<style lang="scss" scoped>
.email-follow-ups-page {
  max-width: 1500px;
  margin: 0 auto;
  padding: 24px;
}
@media (max-width: 700px) {
  .email-follow-ups-page {
    padding: 16px;
  }
}
</style>
