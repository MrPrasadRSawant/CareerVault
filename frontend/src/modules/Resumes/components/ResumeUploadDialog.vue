<template>
  <q-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <q-card class="upload-card">
      <q-card-section class="row items-center">
        <div
          ><div class="text-h6">Upload tailored resume</div
          ><div class="text-caption text-grey-7"
            >Save a version you can review before an interview.</div
          ></div
        >
        <q-space /><q-btn flat round dense icon="close" v-close-popup />
      </q-card-section>
      <q-card-section>
        <q-form class="q-gutter-sm" @submit.prevent="submit">
          <q-file
            v-model="file"
            filled
            label="Resume file *"
            accept=".pdf,.doc,.docx,.txt,.md"
            clearable
            :rules="[value => !!value || 'Choose a resume file']"
            ><template #prepend><q-icon name="upload_file" /></template
          ></q-file>
          <q-input
            v-model="name"
            filled
            label="Resume name"
            hint="Defaults to the selected filename"
          />
          <q-input
            v-model="version"
            filled
            label="Version or tailoring note"
            hint="Example: Product manager role · August 2026"
          />
          <ProfessionalDateField
            v-model="uploadedOn"
            filled
            :outlined="false"
            label="Uploaded date"
          />
          <div class="row justify-end q-gutter-sm q-mt-sm"
            ><q-btn flat label="Cancel" color="primary" v-close-popup /><q-btn
              color="primary"
              label="Upload resume"
              type="submit"
              :loading="saving"
          /></div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import ProfessionalDateField from "@/components/ProfessionalDateField.vue";

const props = defineProps<{ modelValue: boolean; saving: boolean }>();
const emit = defineEmits<{
  (event: "update:modelValue", value: boolean): void;
  (
    event: "save",
    value: { file: File; name: string; version: string; uploadedOn: string }
  ): void;
}>();
const file = ref<File | null>(null);
const name = ref("");
const version = ref("");
const uploadedOn = ref(today());

watch(
  () => props.modelValue,
  open => {
    if (open) {
      file.value = null;
      name.value = "";
      version.value = "";
      uploadedOn.value = today();
    }
  }
);
function today() {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")}`;
}
function submit() {
  if (file.value)
    emit("save", {
      file: file.value,
      name: name.value.trim(),
      version: version.value.trim(),
      uploadedOn: uploadedOn.value
    });
}
</script>

<style lang="scss" scoped>
.upload-card {
  width: min(560px, 94vw);
}
</style>
