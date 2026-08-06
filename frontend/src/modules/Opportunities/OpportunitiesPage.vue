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
    <OpportunityExportDialog
      v-model="exportDialog"
      :row-count="filteredOpportunities.length"
      @export="exportFiltered"
    />
  </q-page>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
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
const {
  loading,
  saving,
  importing,
  filters,
  selectedRows,
  editingOpportunity,
  selectedOpportunity,
  formDialog,
  viewDialog,
  exportDialog,
  updatingStatusIds,
  filteredOpportunities,
  load,
  clearFilters,
  openCreate,
  openEdit,
  openView,
  saveOpportunity,
  updateStatus,
  confirmDelete,
  confirmBulkDelete,
  downloadTemplate,
  importCsv,
  openExport,
  exportFiltered
} = useOpportunities();

onMounted(load);
</script>

<style lang="scss" scoped>
.opportunities-page { padding: 24px; max-width: 1500px; margin: 0 auto; }
@media (max-width: 700px) { .opportunities-page { padding: 16px; } }
</style>
