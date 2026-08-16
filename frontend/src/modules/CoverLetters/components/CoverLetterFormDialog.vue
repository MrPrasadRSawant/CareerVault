<template>
  <q-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <q-card class="dialog-card">
      <q-card-section class="row items-center">
        <div class="text-h6">
          {{ letter ? "Edit Letter" : "New Letter" }}
        </div>
        <q-space />
        <q-btn flat round dense icon="close" v-close-popup />
      </q-card-section>
      <q-card-section>
        <q-form class="q-gutter-sm" @submit.prevent="submit">
          <q-input
            v-model="form.name"
            filled
            label="Name *"
            :rules="[isRequired]"
          />
          <div class="editor-label">Content</div>
          <CoverLetterEditor v-model="form.content" />
          <div class="row justify-end q-gutter-sm q-mt-sm">
            <q-btn flat label="Cancel" color="primary" v-close-popup />
            <q-btn
              color="primary"
              label="Save"
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
import { reactive, watch } from "vue";
import type { CoverLetter } from "@/api/coverLetters";
import CoverLetterEditor from "./CoverLetterEditor.vue";

const props = defineProps<{
  modelValue: boolean;
  letter: CoverLetter | null;
  saving: boolean;
}>();
const emit = defineEmits<{
  (event: "update:modelValue", value: boolean): void;
  (event: "save", value: { name: string; content: string | null }): void;
}>();

const emptyForm = { name: "", content: "" };
const form = reactive({ ...emptyForm });

watch(
  () => props.modelValue,
  open => {
    if (open && props.letter) {
      form.name = props.letter.name;
      form.content = props.letter.content ?? "";
    } else if (open) {
      form.name = "";
      form.content = "";
    }
  }
);

function isRequired(value: string | null) {
  return (value ?? "").trim().length > 0 || "This field is required";
}

function submit() {
  emit("save", {
    name: form.name,
    content: form.content || null
  });
}
</script>

<style lang="scss" scoped>
.dialog-card {
  width: min(680px, 94vw);
}
.editor-label {
  color: var(--cv-muted);
  font-size: 12px;
  font-weight: 700;
  margin-bottom: 4px;
}
</style>
