<template>
  <q-page class="opportunities-page">
    <div class="page-header">
      <div>
        <div class="page-title">Opportunities</div>
        <div class="page-subtitle">
          Your opportunity inbox—from scraped leads to roles ready to apply for.
        </div>
      </div>

      <div class="page-actions">
        <q-btn flat no-caps icon="download" label="CSV template" @click="downloadTemplate" />
        <q-btn flat no-caps icon="upload_file" label="Import CSV" :loading="importing" @click="openCsvPicker" />
        <q-btn unelevated no-caps color="primary" icon="add" label="New opportunity" @click="openCreate" />
        <input ref="csvInput" type="file" accept=".csv,text/csv" hidden @change="onCsvSelected" />
      </div>
    </div>

    <div class="workspace-toolbar">
      <q-input
        v-model="filter"
        dense
        outlined
        clearable
        debounce="250"
        class="search-input"
        placeholder="Search role, company or location"
      >
        <template #prepend><q-icon name="search" /></template>
      </q-input>
      <q-select
        v-model="statusFilter"
        dense
        outlined
        emit-value
        map-options
        clearable
        class="status-filter"
        label="All statuses"
        :options="statusOptions"
      />
      <div class="workspace-count">
        {{ filteredOpportunities.length }} {{ filteredOpportunities.length === 1 ? "opportunity" : "opportunities" }}
      </div>
    </div>

    <div class="panel-card">
      <q-table
        v-model:pagination="pagination"
        :rows="filteredOpportunities"
        :columns="columns"
        row-key="id"
        :loading="loading"
        flat
        bordered
        hide-pagination
        no-data-label="No opportunities match your filters"
      >
        <template #loading>
          <q-inner-loading showing color="primary" />
        </template>

        <template #body-cell-title="props">
          <q-td :props="props">
            <button class="role-link" type="button" @click="openView(props.row)">
              <span class="role-title">{{ props.row.title }}</span>
              <span class="role-source">Posted {{ formatDate(props.row.posted_on_utc) }}</span>
            </button>
          </q-td>
        </template>

        <template #body-cell-company_name="props">
          <q-td :props="props">
            <span class="company-name">{{ props.row.company_name || "—" }}</span>
          </q-td>
        </template>

        <template #body-cell-status="props">
          <q-td :props="props">
            <span class="status-chip" :style="statusStyle(props.row.status)">
              {{ statusLabel(props.row.status) }}
            </span>
          </q-td>
        </template>

        <template #body-cell-posted_on_utc="props">
          <q-td :props="props" class="date-cell">
            {{ formatDate(props.row.posted_on_utc) }}
          </q-td>
        </template>

        <template #body-cell-job_location="props">
          <q-td :props="props">
            <span class="location-cell">
              <q-icon name="place" size="15px" />
              {{ props.row.job_location || "Not specified" }}
            </span>
          </q-td>
        </template>

        <template #body-cell-actions="props">
          <q-td :props="props" class="actions-cell">
            <q-btn flat round dense icon="visibility" color="primary" @click="openView(props.row)">
              <q-tooltip>View opportunity</q-tooltip>
            </q-btn>
            <q-btn flat round dense icon="edit" color="primary" @click="openEdit(props.row)">
              <q-tooltip>Edit opportunity</q-tooltip>
            </q-btn>
            <q-btn flat round dense icon="delete_outline" color="negative" @click="confirmDelete(props.row)">
              <q-tooltip>Delete opportunity</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>

      <div v-if="!loading && filteredOpportunities.length > 0" class="table-footer">
        <span>Showing {{ firstVisibleRow }}–{{ lastVisibleRow }} of {{ filteredOpportunities.length }}</span>
        <q-pagination
          v-model="pagination.page"
          :max="pageCount"
          :max-pages="6"
          boundary-numbers
          direction-links
          color="primary"
          active-color="primary"
        />
      </div>
    </div>

    <q-dialog v-model="formDialog" persistent>
      <q-card class="opportunity-dialog">
        <q-card-section class="dialog-header">
          <div>
            <div class="dialog-title">{{ editingId ? "Edit opportunity" : "New opportunity" }}</div>
            <div class="dialog-subtitle">Capture enough context to make a confident application decision.</div>
          </div>
          <q-btn flat round dense icon="close" v-close-popup />
        </q-card-section>

        <q-card-section class="dialog-body">
          <q-form class="q-gutter-md" @submit.prevent="saveOpportunity">
            <q-stepper v-model="wizardStep" flat animated class="opportunity-stepper">
            <q-step :name="1" title="Role" caption="Essentials" icon="work_outline" :done="wizardStep > 1">
            <div class="form-section-title">Role and company</div>
            <div class="row q-col-gutter-md">
              <div class="col-12 col-md-7">
                <q-input v-model="form.title" outlined label="Role title *" :rules="[isRequired]" />
              </div>
              <div class="col-12 col-md-5">
                <q-input v-model="form.company_name" outlined label="Company name" />
              </div>
              <div class="col-12 col-md-6">
                <q-input v-model="form.job_location" outlined label="Job location" placeholder="Remote, London, Hybrid…" />
              </div>
              <div class="col-12 col-md-6">
                <q-input v-model="form.experience_level" outlined label="Expected experience" placeholder="3–5 years" />
              </div>
            </div>

            </q-step>
            <q-step :name="2" title="Source" caption="Original links" icon="link" :done="wizardStep > 2">
            <div class="wizard-intro">Keep the original links and posting date so this opportunity is easy to revisit.</div>
            <div class="form-section-title">Links and discovery</div>
            <div class="row q-col-gutter-md">
              <div class="col-12">
                <q-input v-model="form.post_url" outlined label="Post URL" type="url" />
              </div>
              <div class="col-12 col-md-6">
                <q-input v-model="form.company_career_page" outlined label="Company career page" type="url" />
              </div>
              <div class="col-12 col-md-6">
                <q-input v-model="form.company_url" outlined label="Company website" type="url" />
              </div>
              <div class="col-12 col-md-6">
                <q-input v-model="form.posted_on_utc" outlined label="Posted date/time (UTC)" type="datetime-local" hint="Optional — stored in UTC" />
              </div>
            </div>

            </q-step>
            <q-step :name="3" title="Evaluate" caption="Next action" icon="fact_check">
            <div class="wizard-intro">Add context to decide whether this role should move to Saved or Applied.</div>
            <div class="form-section-title">Assessment</div>
            <div class="row q-col-gutter-md">
              <div class="col-12 col-md-6">
                <q-select v-model="form.status" outlined emit-value map-options label="Opportunity status" :options="statusOptions" />
              </div>
              <div class="col-12">
                <q-input v-model="form.required_skills" outlined label="Skills asked for" hint="Separate skills with commas" />
              </div>
              <div class="col-12">
                <q-input v-model="form.description" outlined label="Job description" type="textarea" autogrow />
              </div>
            </div>

            </q-step>
            </q-stepper>
            <div class="dialog-actions wizard-actions">
              <q-btn flat no-caps label="Cancel" v-close-popup />
              <q-btn v-if="wizardStep > 1" flat no-caps label="Back" icon="arrow_back" @click="wizardStep -= 1" />
              <q-btn v-if="wizardStep < 3" unelevated no-caps color="primary" label="Continue" icon-right="arrow_forward" @click="nextWizardStep" />
              <q-btn v-if="wizardStep === 3" unelevated no-caps color="primary" :label="editingId ? 'Save changes' : 'Save opportunity'" type="submit" :loading="saving" />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-dialog v-model="viewDialog">
      <q-card v-if="selectedOpportunity" class="opportunity-dialog view-dialog">
        <q-card-section class="dialog-header">
          <div>
            <div class="dialog-title">{{ selectedOpportunity.title }}</div>
            <div class="dialog-subtitle">{{ selectedOpportunity.company_name || "Company not specified" }}</div>
          </div>
          <q-btn flat round dense icon="close" v-close-popup />
        </q-card-section>
        <q-card-section class="view-body">
          <div class="view-status-row">
            <span class="status-chip" :style="statusStyle(selectedOpportunity.status)">{{ statusLabel(selectedOpportunity.status) }}</span>
            <span v-if="selectedOpportunity.job_location"><q-icon name="place" /> {{ selectedOpportunity.job_location }}</span>
          </div>
          <div class="view-links">
            <q-btn v-if="selectedOpportunity.post_url" flat no-caps color="primary" icon="open_in_new" label="Open job post" @click="openUrl(selectedOpportunity.post_url)" />
            <q-btn v-if="selectedOpportunity.company_career_page" flat no-caps color="primary" icon="business" label="Career page" @click="openUrl(selectedOpportunity.company_career_page)" />
            <q-btn v-if="selectedOpportunity.company_url" flat no-caps color="primary" icon="language" label="Company website" @click="openUrl(selectedOpportunity.company_url)" />
          </div>
          <div class="view-grid">
            <div><span>Posted</span><strong>{{ formatDate(selectedOpportunity.posted_on_utc) }}</strong></div>
            <div><span>Experience</span><strong>{{ selectedOpportunity.experience_level || "Not specified" }}</strong></div>
            <div><span>Created</span><strong>{{ formatDate(selectedOpportunity.created_on_utc) }}</strong></div>
          </div>
          <div v-if="selectedOpportunity.required_skills?.length" class="view-block">
            <span class="view-label">Skills requested</span>
            <div class="skill-list"><q-chip v-for="skill in selectedOpportunity.required_skills" :key="skill" dense outline color="primary">{{ skill }}</q-chip></div>
          </div>
          <div v-if="selectedOpportunity.description" class="view-block">
            <span class="view-label">Job description</span>
            <p class="view-text">{{ selectedOpportunity.description }}</p>
          </div>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat no-caps label="Edit" color="primary" @click="openEditFromView" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from "vue";
import { useQuasar, type QTableProps } from "quasar";
import { opportunityApi } from "@/api/opportunities";
import type { Opportunity, OpportunityCreate, OpportunityStatus } from "@/api/opportunities";
import { OPPORTUNITY_STATUS_COLORS, OPPORTUNITY_STATUS_LABELS } from "@/modules/shared/statusColors";

defineOptions({ name: "OpportunitiesPage" });

const $q = useQuasar();
const csvInput = ref<HTMLInputElement | null>(null);
const opportunities = ref<Opportunity[]>([]);
const loading = ref(false);
const saving = ref(false);
const importing = ref(false);
const filter = ref("");
const statusFilter = ref<OpportunityStatus | null>(null);
const formDialog = ref(false);
const wizardStep = ref(1);
const viewDialog = ref(false);
const editingId = ref<string | null>(null);
const selectedOpportunity = ref<Opportunity | null>(null);
const pagination = ref({ page: 1, rowsPerPage: 10 });

const columns: QTableProps["columns"] = [
  { name: "title", required: true, label: "Role", align: "left", field: "title", sortable: true },
  { name: "company_name", label: "Company", align: "left", field: "company_name", sortable: true },
  { name: "status", label: "Status", align: "left", field: "status", sortable: true },
  { name: "job_location", label: "Location", align: "left", field: "job_location" },
  { name: "posted_on_utc", label: "Posted", align: "left", field: "posted_on_utc", sortable: true },
  { name: "actions", label: "", align: "right", field: "id" }
];

const statusOptions = Object.entries(OPPORTUNITY_STATUS_LABELS)
  .filter(([value]) => value !== "interviewing" && value !== "offered")
  .map(([value, label]) => ({ label, value }));

interface OpportunityForm {
  title: string;
  company_name: string;
  post_url: string;
  company_career_page: string;
  company_url: string;
  posted_on_utc: string;
  job_location: string;
  description: string;
  required_skills: string;
  experience_level: string;
  status: OpportunityStatus;
}

const emptyForm = (): OpportunityForm => ({
  title: "",
  company_name: "",
  post_url: "",
  company_career_page: "",
  company_url: "",
  posted_on_utc: "",
  job_location: "",
  description: "",
  required_skills: "",
  experience_level: "",
  status: "draft",
});

const form = reactive(emptyForm());

const filteredOpportunities = computed(() => {
  const term = filter.value.trim().toLowerCase();
  return opportunities.value.filter(opportunity => {
    const matchesStatus = !statusFilter.value || opportunity.status === statusFilter.value;
    if (!matchesStatus) return false;
    if (!term) return true;
    return [opportunity.title, opportunity.company_name, opportunity.job_location]
      .filter(Boolean)
      .some(value => value!.toLowerCase().includes(term));
  });
});

const pageCount = computed(() => Math.max(1, Math.ceil(filteredOpportunities.value.length / pagination.value.rowsPerPage)));
const firstVisibleRow = computed(() => (pagination.value.page - 1) * pagination.value.rowsPerPage + 1);
const lastVisibleRow = computed(() => Math.min(pagination.value.page * pagination.value.rowsPerPage, filteredOpportunities.value.length));

watch([filter, statusFilter], () => { pagination.value.page = 1; });
watch(pageCount, value => { if (pagination.value.page > value) pagination.value.page = value; });

function isRequired(value: string | null) {
  return (value ?? "").trim().length > 0 || "Role title is required";
}

function statusLabel(status: OpportunityStatus): string { return OPPORTUNITY_STATUS_LABELS[status]; }
function statusStyle(status: OpportunityStatus) { return { background: OPPORTUNITY_STATUS_COLORS[status], color: "#fff" }; }
function formatDate(value: string | null | undefined): string { return value ? new Date(value).toLocaleDateString() : "—"; }
function openUrl(url: string) { window.open(url, "_blank", "noopener,noreferrer"); }

async function loadOpportunities() {
  loading.value = true;
  try { opportunities.value = await opportunityApi.list(); }
  catch { $q.notify({ type: "negative", message: "Could not load opportunities" }); }
  finally { loading.value = false; }
}

function openCreate() { editingId.value = null; wizardStep.value = 1; Object.assign(form, emptyForm()); formDialog.value = true; }

function openEdit(opportunity: Opportunity) {
  editingId.value = opportunity.id;
  wizardStep.value = 1;
  Object.assign(form, { ...emptyForm(), ...opportunity, required_skills: opportunity.required_skills?.join(", ") ?? "", posted_on_utc: toLocalDateTime(opportunity.posted_on_utc) });
  formDialog.value = true;
}

function nextWizardStep() {
  if (wizardStep.value === 1 && !isRequired(form.title)) {
    $q.notify({ type: "warning", message: "Add a role title before continuing" });
    return;
  }
  wizardStep.value = Math.min(3, wizardStep.value + 1);
}

function openView(opportunity: Opportunity) { selectedOpportunity.value = opportunity; viewDialog.value = true; }
function openEditFromView() { if (selectedOpportunity.value) { viewDialog.value = false; openEdit(selectedOpportunity.value); } }

function toLocalDateTime(value: string | null): string {
  if (!value) return "";
  const date = new Date(value);
  const offset = date.getTimezoneOffset() * 60000;
  return new Date(date.getTime() - offset).toISOString().slice(0, 16);
}

function normalizeDateTime(value: string): string | null {
  if (!value) return null;
  return value.length === 16 ? `${value}:00Z` : value;
}

function toPayload(): OpportunityCreate {
  return {
    title: form.title.trim(), company_name: form.company_name || null, post_url: form.post_url || null,
    company_career_page: form.company_career_page || null, company_url: form.company_url || null,
    posted_on_utc: normalizeDateTime(form.posted_on_utc), job_location: form.job_location || null,
    description: form.description || null, required_skills: form.required_skills.split(",").map(value => value.trim()).filter(Boolean),
    experience_level: form.experience_level || null, status: form.status
  };
}

async function saveOpportunity() {
  saving.value = true;
  try {
    if (editingId.value) await opportunityApi.update(editingId.value, toPayload());
    else await opportunityApi.create(toPayload());
    $q.notify({ type: "positive", message: editingId.value ? "Opportunity updated" : "Opportunity created" });
    formDialog.value = false;
    await loadOpportunities();
  } catch { $q.notify({ type: "negative", message: "Could not save opportunity" }); }
  finally { saving.value = false; }
}

async function confirmDelete(opportunity: Opportunity) {
  $q.dialog({ title: "Delete opportunity?", message: `This will remove “${opportunity.title}” from your inbox.`, cancel: true, persistent: true, ok: { label: "Delete", color: "negative", unelevated: true } }).onOk(async () => {
    try { await opportunityApi.remove(opportunity.id); $q.notify({ type: "positive", message: "Opportunity deleted" }); await loadOpportunities(); }
    catch { $q.notify({ type: "negative", message: "Could not delete opportunity" }); }
  });
}

function openCsvPicker() { csvInput.value?.click(); }

function downloadTemplate() {
  const headers = ["role", "company_name", "post_url", "company_career_page", "company_url", "posted_on_utc", "job_description", "skills_asked", "expected_work_experience", "job_location"];
  const blob = new Blob([`${headers.join(",")}\n`], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a"); anchor.href = url; anchor.download = "careervault-opportunities-template.csv"; anchor.click(); URL.revokeObjectURL(url);
}

function parseCsv(text: string): string[][] {
  const rows: string[][] = []; let row: string[] = []; let cell = ""; let quoted = false;
  for (let index = 0; index < text.length; index += 1) {
    const char = text[index]; const next = text[index + 1];
    if (char === '"' && quoted && next === '"') { cell += '"'; index += 1; }
    else if (char === '"') quoted = !quoted;
    else if (char === "," && !quoted) { row.push(cell.trim()); cell = ""; }
    else if ((char === "\n" || char === "\r") && !quoted) { if (char === "\r" && next === "\n") index += 1; row.push(cell.trim()); if (row.some(Boolean)) rows.push(row); row = []; cell = ""; }
    else cell += char;
  }
  if (cell || row.length) { row.push(cell.trim()); rows.push(row); }
  return rows;
}

async function onCsvSelected(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (!file) return;
  importing.value = true;
  try {
    const rows = parseCsv(await file.text());
    if (rows.length < 2) throw new Error("CSV has no rows");
    const headers = rows[0]!.map(header => header.trim().toLowerCase());
    const value = (row: string[], name: string) => row[headers.indexOf(name)]?.trim() || null;
    let imported = 0;
    for (const row of rows.slice(1)) {
      const title = value(row, "role");
      if (!title) continue;
      await opportunityApi.create({ title, company_name: value(row, "company_name"), post_url: value(row, "post_url"), company_career_page: value(row, "company_career_page"), company_url: value(row, "company_url"), posted_on_utc: normalizeDateTime(value(row, "posted_on_utc") ?? ""), description: value(row, "job_description"), required_skills: (value(row, "skills_asked") ?? "").split(/[;,]/).map(skill => skill.trim()).filter(Boolean), experience_level: value(row, "expected_work_experience"), job_location: value(row, "job_location"), status: "draft" });
      imported += 1;
    }
    $q.notify({ type: "positive", message: `${imported} opportunities imported as drafts` });
    await loadOpportunities();
  } catch { $q.notify({ type: "negative", message: "Could not import CSV. Download the template to check the column names." }); }
  finally { importing.value = false; if (csvInput.value) csvInput.value.value = ""; }
}

onMounted(loadOpportunities);
</script>

<style lang="scss" scoped>
.opportunities-page { padding: 24px; max-width: 1500px; margin: 0 auto; }
.page-header, .workspace-toolbar { display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
.page-header { margin-bottom: 22px; }
.page-title { color: #102a43; font-size: 26px; font-weight: 750; letter-spacing: -0.4px; }
.page-subtitle { margin-top: 4px; color: #627d98; font-size: 14px; }
.page-actions { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.workspace-toolbar { justify-content: flex-start; margin-bottom: 14px; }
.search-input { flex: 1 1 340px; max-width: 520px; }
.status-filter { width: 190px; }
.workspace-count { margin-left: auto; color: #829ab1; font-size: 13px; }
.panel-card { overflow: hidden; background: #fff; border: 1px solid #dce6eb; border-radius: 14px; box-shadow: 0 2px 8px rgba(16, 42, 67, 0.06); }
.role-link { display: flex; flex-direction: column; align-items: flex-start; gap: 3px; padding: 0; border: 0; background: transparent; color: inherit; cursor: pointer; text-align: left; }
.role-title { color: #102a43; font-size: 14px; font-weight: 700; }
.role-link:hover .role-title { color: #1f6f8b; text-decoration: underline; }
.role-source { color: #829ab1; font-size: 11px; }
.company-name { color: #334e68; font-weight: 600; }
.location-cell { display: inline-flex; align-items: center; gap: 5px; color: #627d98; font-size: 13px; }
.date-cell { color: #627d98; font-size: 13px; white-space: nowrap; }
.status-chip { display: inline-block; padding: 4px 10px; border-radius: 999px; font-size: 11px; font-weight: 700; white-space: nowrap; }
.actions-cell { white-space: nowrap; }
.table-footer { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 14px 16px; border-top: 1px solid #edf2f5; color: #829ab1; font-size: 12px; }
.opportunity-dialog { width: min(760px, 94vw); max-width: 760px; }
.dialog-header { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; border-bottom: 1px solid #edf2f5; }
.dialog-title { color: #102a43; font-size: 20px; font-weight: 750; }
.dialog-subtitle { margin-top: 4px; color: #829ab1; font-size: 12px; }
.dialog-body { max-height: 72vh; overflow-y: auto; }
.opportunity-stepper { background: transparent; }
.opportunity-stepper :deep(.q-stepper__header) { border: 1px solid #e7eef2; border-radius: 10px; background: #f8fafb; box-shadow: none; }
.opportunity-stepper :deep(.q-stepper__tab) { min-height: 64px; padding: 12px 16px; }
.opportunity-stepper :deep(.q-stepper__step-inner) { padding: 18px 2px 4px; }
.wizard-intro { margin-bottom: 16px; color: #627d98; font-size: 13px; line-height: 1.5; }
.form-section-title { margin-top: 10px; color: #1f6f8b; font-size: 11px; font-weight: 800; letter-spacing: 0.8px; text-transform: uppercase; }
.dialog-actions { display: flex; align-items: center; justify-content: flex-end; gap: 8px; padding-top: 18px; }
.view-body { display: flex; flex-direction: column; gap: 18px; }
.view-status-row, .view-links { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; color: #627d98; font-size: 13px; }
.view-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; padding: 14px; border: 1px solid #e7eef2; border-radius: 10px; background: #f8fafb; }
.view-grid div { display: flex; flex-direction: column; gap: 4px; }
.view-grid span, .view-label { color: #829ab1; font-size: 11px; font-weight: 700; letter-spacing: 0.4px; text-transform: uppercase; }
.view-grid strong { color: #243b53; font-size: 13px; }
.view-block { display: flex; flex-direction: column; gap: 8px; }
.skill-list { display: flex; flex-wrap: wrap; gap: 4px; }
.view-text { margin: 0; color: #334e68; font-size: 13px; line-height: 1.6; white-space: pre-wrap; }
@media (max-width: 700px) {
  .opportunities-page { padding: 16px; }
  .page-actions { width: 100%; }
  .page-actions .q-btn { flex: 1; }
  .workspace-count { width: 100%; margin-left: 0; }
  .table-footer { align-items: flex-start; flex-direction: column; }
  .view-grid { grid-template-columns: repeat(2, 1fr); }
  .opportunity-dialog { width: 100%; max-width: none; }
  .dialog-body { max-height: calc(100vh - 150px); padding: 16px; }
  .opportunity-stepper :deep(.q-stepper__header) { border-radius: 8px; }
  .opportunity-stepper :deep(.q-stepper__tab) { min-height: 52px; padding: 8px 10px; }
  .opportunity-stepper :deep(.q-stepper__label) { font-size: 12px; }
  .opportunity-stepper :deep(.q-stepper__caption) { display: none; }
  .opportunity-stepper :deep(.q-stepper__step-inner) { padding-top: 14px; }
  .dialog-actions { position: sticky; bottom: -16px; margin: 8px -16px -16px; padding: 12px 16px; background: #fff; border-top: 1px solid #edf2f5; }
}
</style>
