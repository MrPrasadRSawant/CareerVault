<template>
  <q-input
    :model-value="displayValue"
    :label="label"
    :outlined="outlined"
    :filled="filled"
    :dense="dense"
    readonly
    clearable
    class="professional-date-field"
    @clear="clearValue"
  >
    <template #prepend><q-icon name="event" color="primary" /></template>
    <template #append>
      <q-icon name="calendar_month" class="cursor-pointer" color="primary">
        <q-popup-proxy
          cover
          transition-show="scale"
          transition-hide="scale"
          class="date-popup"
        >
          <q-date
            :model-value="modelValue || undefined"
            mask="YYYY-MM-DD"
            today-btn
            color="primary"
            @update:model-value="selectValue"
          >
            <div
              class="row items-center justify-between q-pa-sm date-popup-actions"
            >
              <q-btn
                flat
                no-caps
                color="primary"
                label="Clear"
                @click="clearValue"
              />
              <q-btn flat no-caps color="primary" label="Done" v-close-popup />
            </div>
          </q-date>
        </q-popup-proxy>
      </q-icon>
    </template>
  </q-input>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = withDefaults(
  defineProps<{
    modelValue: string | null | undefined;
    label: string;
    outlined?: boolean;
    filled?: boolean;
    dense?: boolean;
  }>(),
  { outlined: true, filled: false, dense: true }
);

const emit = defineEmits<{
  (event: "update:modelValue", value: string | null): void;
}>();

const displayValue = computed(() => {
  if (!props.modelValue) return "";
  const [year, month, day] = props.modelValue.split("-");
  return year && month && day
    ? `${day} ${monthName(Number(month))} ${year}`
    : props.modelValue;
});

function monthName(month: number): string {
  return new Intl.DateTimeFormat("en", { month: "short" }).format(
    new Date(2020, month - 1, 1)
  );
}

function selectValue(value: string | null) {
  emit("update:modelValue", value || null);
}
function clearValue() {
  emit("update:modelValue", null);
}
</script>

<style lang="scss" scoped>
.professional-date-field :deep(.q-field__control),
.professional-date-field :deep(.q-field__native) {
  cursor: pointer;
}
.date-popup {
  border-radius: 14px;
  box-shadow: 0 14px 36px rgba(16, 42, 67, 0.2);
}
.date-popup-actions {
  border-top: 1px solid #edf2f5;
}
</style>
