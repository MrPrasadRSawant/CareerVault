<template>
  <q-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <q-card class="dialog-card">
      <q-card-section class="row items-center"
        ><div class="text-h6">New application</div><q-space /><q-btn
          flat
          round
          dense
          icon="close"
          v-close-popup
      /></q-card-section>
      <q-card-section>
        <q-form class="q-gutter-sm" @submit.prevent="submit">
          <q-select
            v-model="form.opportunity_id"
            filled
            label="Opportunity *"
            :options="opportunityOptions"
            :disable="lockOpportunity"
            use-input
            input-debounce="0"
            emit-value
            map-options
            :rules="[value => !!value || 'Choose an opportunity']"
            @filter="filterOpportunities"
          />
          <q-select
            v-model="form.status"
            filled
            label="Status"
            :options="statusOptions"
            emit-value
            map-options
          />
          <q-select
            v-model="form.resume_id"
            filled
            clearable
            label="Tailored resume"
            :options="resumeOptions"
            emit-value
            map-options
            hint="Bind the version used for this application"
          />
          <ProfessionalDateField
            v-model="form.applied_date"
            filled
            :outlined="false"
            label="Applied date"
          />
          <q-input
            v-model="form.notes"
            filled
            label="Notes"
            type="textarea"
            autogrow
          />
          <div class="row justify-end q-gutter-sm q-mt-sm"
            ><q-btn flat label="Cancel" color="primary" v-close-popup /><q-btn
              color="primary"
              label="Save application"
              type="submit"
              :loading="saving"
          /></div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from "vue";
import type { ApplicationStatus } from "@/api/applications";
import type { Opportunity } from "@/api/opportunities";
import type { Resume } from "@/api/resumes";
import { applicationStatusOptions } from "../utils";
import ProfessionalDateField from "@/components/ProfessionalDateField.vue";

const props = withDefaults(
  defineProps<{
    modelValue: boolean;
    opportunities: Opportunity[];
    resumes: Resume[];
    saving: boolean;
    initialOpportunityId?: string | null;
    lockOpportunity?: boolean;
  }>(),
  {
    initialOpportunityId: null,
    lockOpportunity: false
  }
);
const emit = defineEmits<{
  (event: "update:modelValue", value: boolean): void;
  (
    event: "save",
    value: {
      opportunity_id: string;
      resume_id: string | null;
      status: ApplicationStatus;
      applied_date: string | null;
      notes: string | null;
    }
  ): void;
}>();
const statusOptions = applicationStatusOptions;
const selectableOpportunityOptions = computed(() =>
  props.opportunities
    .filter(
      opportunity =>
        opportunity.status === "applied" ||
        (props.lockOpportunity && opportunity.id === props.initialOpportunityId)
    )
    .map(opportunity => ({
    label: `${opportunity.title}${opportunity.company_name ? ` · ${opportunity.company_name}` : ""}`,
    value: opportunity.id
    }))
);
const opportunityOptions = ref(selectableOpportunityOptions.value);
const resumeOptions = computed(() =>
  props.resumes.map(resume => ({
    label: `${resume.name} (${resume.version || "untitled version"})`,
    value: resume.id
  }))
);
const form = reactive<{
  opportunity_id: string | null;
  resume_id: string | null;
  status: ApplicationStatus;
  applied_date: string;
  notes: string;
}>({
  opportunity_id: null,
  resume_id: null,
  status: "applied",
  applied_date: new Date().toISOString().slice(0, 10),
  notes: ""
});
watch(
  () => props.modelValue,
  open => {
    if (open) {
      opportunityOptions.value = selectableOpportunityOptions.value;
      Object.assign(form, {
        opportunity_id: props.initialOpportunityId,
        resume_id: null,
        status: "applied",
        applied_date: new Date().toISOString().slice(0, 10),
        notes: ""
      });
    }
  }
);
watch(selectableOpportunityOptions, options => {
  opportunityOptions.value = options;
});

function filterOpportunities(
  value: string,
  update: (callback: () => void) => void
) {
  update(() => {
    const search = value.trim().toLowerCase();
    opportunityOptions.value = search
      ? selectableOpportunityOptions.value.filter(option =>
          option.label.toLowerCase().includes(search)
        )
      : selectableOpportunityOptions.value;
  });
}
function submit() {
  if (!form.opportunity_id) return;
  emit("save", {
    opportunity_id: form.opportunity_id,
    resume_id: form.resume_id,
    status: form.status,
    applied_date: form.applied_date || null,
    notes: form.notes || null
  });
}
</script>

<style lang="scss" scoped>
.dialog-card {
  width: min(520px, 94vw);
}
</style>
