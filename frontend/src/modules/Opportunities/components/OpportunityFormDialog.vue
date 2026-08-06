<template>
  <q-dialog
    :model-value="modelValue"
    persistent
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <q-card class="opportunity-dialog">
      <q-card-section class="dialog-header">
        <div>
          <div class="dialog-title">{{
            editingOpportunity ? "Edit opportunity" : "New opportunity"
          }}</div>
          <div class="dialog-subtitle"
            >Capture enough context to make a confident application
            decision.</div
          >
        </div>
        <q-btn flat round dense icon="close" v-close-popup />
      </q-card-section>
      <q-card-section class="dialog-body">
        <q-form class="q-gutter-md" @submit.prevent="save">
          <q-stepper
            v-model="wizardStep"
            flat
            animated
            class="opportunity-stepper"
          >
            <q-step
              :name="1"
              title="Role"
              caption="Essentials"
              icon="work_outline"
              :done="wizardStep > 1"
            >
              <div class="form-section-title">Role and company</div>
              <div class="row q-col-gutter-md">
                <div class="col-12 col-md-7"
                  ><q-input
                    v-model="form.title"
                    outlined
                    label="Role title *"
                    :rules="[isRequired]"
                /></div>
                <div class="col-12 col-md-5"
                  ><q-input
                    v-model="form.company_name"
                    outlined
                    label="Company name"
                /></div>
                <div class="col-12 col-md-6"
                  ><q-input
                    v-model="form.job_location"
                    outlined
                    label="Job location"
                    placeholder="Remote, London, Hybrid…"
                /></div>
                <div class="col-12 col-md-6"
                  ><q-input
                    v-model="form.experience_level"
                    outlined
                    label="Expected experience"
                    placeholder="3–5 years"
                /></div>
              </div>
            </q-step>
            <q-step
              :name="2"
              title="Source"
              caption="Original links"
              icon="link"
              :done="wizardStep > 2"
            >
              <div class="wizard-intro"
                >Keep the original links and posting date so this opportunity is
                easy to revisit.</div
              >
              <div class="form-section-title">Links and discovery</div>
              <div class="row q-col-gutter-md">
                <div class="col-12"
                  ><q-input
                    v-model="form.post_url"
                    outlined
                    label="Post URL"
                    type="url"
                /></div>
                <div class="col-12 col-md-6"
                  ><q-input
                    v-model="form.company_career_page"
                    outlined
                    label="Company career page"
                    type="url"
                /></div>
                <div class="col-12 col-md-6"
                  ><q-input
                    v-model="form.company_url"
                    outlined
                    label="Company website"
                    type="url"
                /></div>
                <div class="col-12 col-md-6"
                  ><ProfessionalDateTimeField
                    v-model="form.posted_on_utc"
                    label="Posted date/time (UTC)"
                    hint="Optional — stored in UTC"
                /></div>
              </div>
            </q-step>
            <q-step
              :name="3"
              title="Evaluate"
              caption="Next action"
              icon="fact_check"
            >
              <div class="wizard-intro"
                >Add context to decide whether this role should move to Saved or
                Applied.</div
              >
              <div class="form-section-title">Assessment</div>
              <div class="row q-col-gutter-md">
                <div class="col-12 col-md-6"
                  ><q-select
                    v-model="form.status"
                    outlined
                    emit-value
                    map-options
                    label="Opportunity status"
                    :options="statusOptions"
                /></div>
                <div class="col-12"
                  ><q-input
                    v-model="form.required_skills"
                    outlined
                    label="Skills asked for"
                    hint="Separate skills with commas"
                /></div>
                <div class="col-12"
                  ><q-input
                    v-model="form.description"
                    outlined
                    label="Job description"
                    type="textarea"
                    autogrow
                /></div>
              </div>
            </q-step>
          </q-stepper>
          <div class="dialog-actions">
            <q-btn flat no-caps label="Cancel" v-close-popup />
            <q-btn
              v-if="wizardStep > 1"
              flat
              no-caps
              label="Back"
              icon="arrow_back"
              @click="wizardStep -= 1"
            />
            <q-btn
              v-if="wizardStep < 3"
              unelevated
              no-caps
              color="primary"
              label="Continue"
              icon-right="arrow_forward"
              @click="nextStep"
            />
            <q-btn
              v-if="wizardStep === 3"
              unelevated
              no-caps
              color="primary"
              :label="editingOpportunity ? 'Save changes' : 'Save opportunity'"
              type="submit"
              :loading="saving"
            />
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { reactive, ref, watch } from "vue";
import type {
  Opportunity,
  OpportunityCreate,
  OpportunityStatus
} from "@/api/opportunities";
import { normalizeDateTime, toLocalDateTime } from "../utils";
import ProfessionalDateTimeField from "@/components/ProfessionalDateTimeField.vue";

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

const props = defineProps<{
  modelValue: boolean;
  editingOpportunity: Opportunity | null;
  saving: boolean;
  statusOptions: { label: string; value: OpportunityStatus }[];
}>();
const emit = defineEmits<{
  (event: "update:modelValue", value: boolean): void;
  (event: "save", id: string | null, payload: OpportunityCreate): void;
}>();

const wizardStep = ref(1);
const form = reactive<OpportunityForm>(emptyForm());

function emptyForm(): OpportunityForm {
  return {
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
    status: "saved"
  };
}

watch([() => props.modelValue, () => props.editingOpportunity], ([open]) => {
  if (!open) return;
  wizardStep.value = 1;
  const opportunity = props.editingOpportunity;
  Object.assign(
    form,
    opportunity
      ? {
          title: opportunity.title,
          company_name: opportunity.company_name ?? "",
          post_url: opportunity.post_url ?? "",
          company_career_page: opportunity.company_career_page ?? "",
          company_url: opportunity.company_url ?? "",
          posted_on_utc: toLocalDateTime(opportunity.posted_on_utc),
          job_location: opportunity.job_location ?? "",
          description: opportunity.description ?? "",
          required_skills: opportunity.required_skills?.join(", ") ?? "",
          experience_level: opportunity.experience_level ?? "",
          status: opportunity.status
        }
      : emptyForm()
  );
});

function isRequired(value: string | null) {
  return (value ?? "").trim().length > 0 || "Role title is required";
}
function nextStep() {
  if (wizardStep.value === 1 && !isRequired(form.title)) return;
  wizardStep.value = Math.min(3, wizardStep.value + 1);
}
function save() {
  if (!isRequired(form.title)) return;
  emit("save", props.editingOpportunity?.id ?? null, {
    title: form.title.trim(),
    company_name: form.company_name || null,
    post_url: form.post_url || null,
    company_career_page: form.company_career_page || null,
    company_url: form.company_url || null,
    posted_on_utc: normalizeDateTime(form.posted_on_utc),
    job_location: form.job_location || null,
    description: form.description || null,
    required_skills: form.required_skills
      .split(",")
      .map(value => value.trim())
      .filter(Boolean),
    experience_level: form.experience_level || null,
    status: form.status
  });
}
</script>

<style lang="scss" scoped>
.opportunity-dialog {
  width: min(760px, 94vw);
  max-width: 760px;
}
.dialog-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  border-bottom: 1px solid #edf2f5;
}
.dialog-title {
  color: #102a43;
  font-size: 20px;
  font-weight: 750;
}
.dialog-subtitle {
  margin-top: 4px;
  color: #829ab1;
  font-size: 12px;
}
.dialog-body {
  max-height: 72vh;
  overflow-y: auto;
}
.opportunity-stepper {
  background: transparent;
}
.opportunity-stepper :deep(.q-stepper__header) {
  border: 1px solid #e7eef2;
  border-radius: 10px;
  background: #f8fafb;
  box-shadow: none;
}
.opportunity-stepper :deep(.q-stepper__tab) {
  min-height: 64px;
  padding: 12px 16px;
}
.opportunity-stepper :deep(.q-stepper__step-inner) {
  padding: 18px 2px 4px;
}
.wizard-intro {
  margin-bottom: 16px;
  color: #627d98;
  font-size: 13px;
  line-height: 1.5;
}
.form-section-title {
  margin-top: 10px;
  color: #1f6f8b;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}
.dialog-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  padding-top: 18px;
}
@media (max-width: 700px) {
  .opportunity-dialog {
    width: 100%;
    max-width: none;
  }
  .dialog-body {
    max-height: calc(100vh - 150px);
    padding: 16px;
  }
  .dialog-actions {
    position: sticky;
    bottom: -16px;
    margin: 8px -16px -16px;
    padding: 12px 16px;
    background: #fff;
    border-top: 1px solid #edf2f5;
  }
}
</style>
