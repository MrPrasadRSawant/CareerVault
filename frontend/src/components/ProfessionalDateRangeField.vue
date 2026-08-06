<template>
  <q-input
    :model-value="displayValue"
    :label="label"
    outlined
    dense
    readonly
    clearable
    class="professional-date-range-field"
    @clear="clearValue"
  >
    <template #prepend><q-icon name="date_range" color="primary" /></template>
    <template #append>
      <q-icon name="calendar_month" class="cursor-pointer" color="primary">
        <q-popup-proxy
          cover
          transition-show="scale"
          transition-hide="scale"
          class="date-popup"
        >
          <q-date
            :model-value="rangeValue"
            mask="YYYY-MM-DD"
            range
            today-btn
            color="primary"
            @update:model-value="selectRange"
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

const props = defineProps<{ from: string; to: string; label: string }>();
const emit = defineEmits<{
  (event: "update:from", value: string): void;
  (event: "update:to", value: string): void;
}>();

const rangeValue = computed(() => {
  if (!props.from) return undefined;
  return { from: props.from, to: props.to || props.from };
});

const displayValue = computed(() => {
  if (!props.from) return "";
  const from = formatDate(props.from);
  return props.to ? `${from} – ${formatDate(props.to)}` : from;
});

function formatDate(value: string): string {
  const [year, month, day] = value.split("-");
  return year && month && day
    ? `${day} ${new Intl.DateTimeFormat("en", { month: "short" }).format(new Date(2020, Number(month) - 1, 1))} ${year}`
    : value;
}

function selectRange(value: unknown) {
  if (typeof value === "string") {
    emit("update:from", value);
    emit("update:to", "");
    return;
  }
  if (value && typeof value === "object" && "from" in value) {
    const selected = value as { from?: string; to?: string };
    emit("update:from", selected.from || "");
    emit("update:to", selected.to || "");
  }
}

function clearValue() {
  emit("update:from", "");
  emit("update:to", "");
}
</script>

<style lang="scss" scoped>
.professional-date-range-field :deep(.q-field__control),
.professional-date-range-field :deep(.q-field__native) {
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
