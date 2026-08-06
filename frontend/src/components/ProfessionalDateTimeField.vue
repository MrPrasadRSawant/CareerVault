<template>
  <q-input
    :model-value="displayValue"
    :label="label"
    :outlined="outlined"
    :filled="filled"
    :dense="dense"
    readonly
    clearable
    class="professional-date-time-field"
    @clear="clearValue"
  >
    <template #prepend><q-icon name="event" color="primary" /></template>
    <template #append>
      <q-icon name="calendar_month" class="cursor-pointer" color="primary">
        <q-popup-proxy
          cover
          transition-show="scale"
          transition-hide="scale"
          class="date-time-popup"
        >
          <q-card flat>
            <div class="date-time-pickers">
              <q-date v-model="datePart" mask="YYYY-MM-DD" color="primary" />
              <q-time v-model="timePart" format24h color="primary" />
            </div>
            <div
              class="row items-center justify-between q-pa-sm date-time-actions"
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
          </q-card>
        </q-popup-proxy>
      </q-icon>
    </template>
  </q-input>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";

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
  (event: "update:modelValue", value: string): void;
}>();
const datePart = ref("");
const timePart = ref("09:00");

watch(
  () => props.modelValue,
  value => {
    datePart.value = value?.slice(0, 10) || "";
    timePart.value = value?.slice(11, 16) || "09:00";
  },
  { immediate: true }
);

const displayValue = computed(() => {
  if (!datePart.value) return "";
  const [year, month, day] = datePart.value.split("-");
  const date =
    year && month && day
      ? `${day} ${new Intl.DateTimeFormat("en", { month: "short" }).format(new Date(2020, Number(month) - 1, 1))} ${year}`
      : datePart.value;
  return `${date}, ${timePart.value}`;
});

watch([datePart, timePart], () => {
  if (datePart.value)
    emit("update:modelValue", `${datePart.value}T${timePart.value}`);
});

function clearValue() {
  datePart.value = "";
  timePart.value = "09:00";
  emit("update:modelValue", "");
}
</script>

<style lang="scss" scoped>
.professional-date-time-field :deep(.q-field__control),
.professional-date-time-field :deep(.q-field__native) {
  cursor: pointer;
}
.date-time-popup {
  border-radius: 14px;
  box-shadow: 0 14px 36px rgba(16, 42, 67, 0.2);
}
.date-time-pickers {
  display: flex;
  align-items: stretch;
  gap: 4px;
  padding: 4px;
}
.date-time-actions {
  border-top: 1px solid #edf2f5;
}
@media (max-width: 560px) {
  .date-time-pickers {
    flex-direction: column;
  }
}
</style>
