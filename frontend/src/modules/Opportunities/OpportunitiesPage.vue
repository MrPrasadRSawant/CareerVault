<template>
  <q-page class="opportunities-page">
    <OpportunityToolbar
      :importing="importing"
      :selected-count="selectedRows.length"
      @create="openCreate"
      @template="downloadTemplate"
      @export="openExport"
      @import="importCsv"
      @bulk-delete="confirmBulkDelete"
      @clear-selection="selectedRows = []"
    />

    <OpportunityFilters
      v-model="filters"
      :status-options="statusOptions"
      :result-count="filteredOpportunities.length"
      @clear="clearFilters"
    />

    <OpportunityTable
      v-model:selected-rows="selectedRows"
      :rows="filteredOpportunities"
      :loading="loading"
      :status-options="statusOptions"
      :updating-status-ids="updatingStatusIds"
      :view-opportunity="openView"
      @view="openView"
      @edit="openEdit"
      @convert="openApplicationConversion"
      @delete="confirmDelete"
      @status-change="updateStatus"
    />

    <OpportunityFormDialog
      v-model="formDialog"
      :editing-opportunity="editingOpportunity"
      :saving="saving"
      :status-options="statusOptions"
      @save="saveOpportunity"
    />
    <OpportunityViewDialog
      v-if="viewDialog"
      v-model="viewDialog"
      :opportunity="selectedOpportunity"
      @edit="openEdit"
    />
    <ApplicationFormDialog
      v-model="applicationDialog"
      :opportunities="opportunities"
      :resumes="resumes"
      :saving="savingApplication"
      :initial-opportunity-id="convertingOpportunity?.id ?? null"
      lock-opportunity
      @save="convertToApplication"
    />
    <OpportunityExportDialog
      v-model="exportDialog"
      :row-count="filteredOpportunities.length"
      @export="exportFiltered"
    />
  </q-page>
</template>

<script setup lang="ts">
import { onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import ApplicationFormDialog from "@/modules/Applications/components/ApplicationFormDialog.vue";
import OpportunityExportDialog from "./components/OpportunityExportDialog.vue";
import OpportunityFilters from "./components/OpportunityFilters.vue";
import OpportunityFormDialog from "./components/OpportunityFormDialog.vue";
import OpportunityTable from "./components/OpportunityTable.vue";
import OpportunityToolbar from "./components/OpportunityToolbar.vue";
import OpportunityViewDialog from "./components/OpportunityViewDialog.vue";
import { useOpportunities } from "./composables/useOpportunities";
import { opportunityStatusOptions } from "./utils";

defineOptions({ name: "OpportunitiesPage" });

const statusOptions = opportunityStatusOptions;
const route = useRoute();
const {
  loading,
  saving,
  savingApplication,
  importing,
  opportunities,
  resumes,
  filters,
  selectedRows,
  editingOpportunity,
  selectedOpportunity,
  formDialog,
  viewDialog,
  exportDialog,
  applicationDialog,
  convertingOpportunity,
  updatingStatusIds,
  filteredOpportunities,
  load,
  clearFilters,
  openCreate,
  openEdit,
  openView,
  openApplicationConversion,
  convertToApplication,
  saveOpportunity,
  updateStatus,
  confirmDelete,
  confirmBulkDelete,
  downloadTemplate,
  importCsv,
  openExport,
  exportFiltered
} = useOpportunities();

watch(
  () => route.query.search,
  value => {
    filters.value.search = typeof value === "string" ? value : "";
  },
  { immediate: true }
);

onMounted(load);
</script>

<style lang="scss" scoped>
.opportunities-page {
  padding: 24px;
  max-width: 1500px;
  margin: 0 auto;
}
@media (max-width: 700px) {
  .opportunities-page {
    padding: 16px;
  }
}
</style>
