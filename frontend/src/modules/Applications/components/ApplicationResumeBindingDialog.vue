<template>
  <q-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <q-card class="binding-card">
      <q-card-section class="row items-center"
        ><div
          ><div class="text-h6">Bind a tailored resume</div
          ><div class="text-caption text-grey-7"
            >Choose the exact version used for this application.</div
          ></div
        ><q-space /><q-btn flat round dense icon="close" v-close-popup
      /></q-card-section>
      <q-card-section>
        <div class="application-context q-mb-md"
          ><span>APPLICATION</span
          ><strong>{{
            application?.opportunity?.title || "Selected application"
          }}</strong></div
        >
        <q-select
          v-model="selectedResumeId"
          filled
          clearable
          label="Resume"
          :options="resumeOptions"
          emit-value
          map-options
          hint="Clear this field to remove the current binding"
        />
        <div v-if="application?.resume" class="current-resume q-mt-md"
          ><q-icon name="description" color="primary" /><div
            ><span>Currently attached</span
            ><strong>{{ application.resume.name }}</strong
            ><small v-if="application.resume.version">{{
              application.resume.version
            }}</small></div
          ></div
        >
      </q-card-section>
      <q-card-actions align="right"
        ><q-btn flat label="Cancel" v-close-popup /><q-btn
          color="primary"
          label="Save binding"
          :loading="saving"
          @click="save"
      /></q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import type { Resume } from "@/api/resumes";
import type { ApplicationRow } from "../types";

const props = defineProps<{
  modelValue: boolean;
  application: ApplicationRow | null;
  resumes: Resume[];
  saving: boolean;
}>();
const emit = defineEmits<{
  (event: "update:modelValue", value: boolean): void;
  (event: "save", resumeId: string | null): void;
}>();
const selectedResumeId = ref<string | null>(null);
const resumeOptions = computed(() =>
  props.resumes.map(resume => ({
    label: `${resume.name}${resume.version ? ` · ${resume.version}` : ""}`,
    value: resume.id
  }))
);
watch(
  [() => props.modelValue, () => props.application],
  ([open, application]) => {
    if (open) selectedResumeId.value = application?.resume_id ?? null;
  }
);
function save() {
  emit("save", selectedResumeId.value);
}
</script>

<style lang="scss" scoped>
.binding-card {
  width: min(520px, 94vw);
}
.application-context {
  border-left: 3px solid var(--cv-primary);
  padding-left: 10px;
}
.application-context span,
.current-resume span {
  display: block;
  color: var(--cv-muted-light);
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
.application-context strong {
  display: block;
  margin-top: 3px;
  color: var(--cv-navy);
  font-size: 14px;
}
.current-resume {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  border-radius: 9px;
  background: var(--cv-page);
  padding: 10px;
}
.current-resume strong,
.current-resume small {
  display: block;
  margin-top: 2px;
  color: var(--cv-text-strong);
}
.current-resume small {
  color: var(--cv-muted);
  font-size: 11px;
}
</style>
