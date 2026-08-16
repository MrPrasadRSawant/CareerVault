<template>
  <q-dialog v-model="open" @hide="reset">
    <q-card class="password-dialog">
      <div class="dialog-header">
        <div class="header-icon"><q-icon name="password" /></div>
        <div>
          <h2>Change password</h2>
          <p>Confirm your current password before choosing a new one.</p>
        </div>
        <q-btn
          v-close-popup
          flat
          round
          dense
          icon="close"
          aria-label="Close change password dialog"
          class="close-btn"
        />
      </div>

      <q-separator />

      <q-card-section class="dialog-body">
        <q-form ref="form" class="password-form" @submit="submit">
          <q-input
            v-model="currentPassword"
            outlined
            :type="showCurrent ? 'text' : 'password'"
            label="Current password"
            autocomplete="current-password"
            :rules="[required]"
          >
            <template #prepend><q-icon name="lock_outline" /></template>
            <template #append>
              <q-btn
                flat
                round
                dense
                :icon="showCurrent ? 'visibility_off' : 'visibility'"
                :aria-label="showCurrent ? 'Hide password' : 'Show password'"
                @click="showCurrent = !showCurrent"
              />
            </template>
          </q-input>

          <q-input
            v-model="newPassword"
            outlined
            :type="showNew ? 'text' : 'password'"
            label="New password"
            autocomplete="new-password"
            :maxlength="maximumLength"
            :hint="`${minimumLength}–${maximumLength} characters`"
            :rules="[required, validLength, differentPassword]"
          >
            <template #prepend><q-icon name="key" /></template>
            <template #append>
              <q-btn
                flat
                round
                dense
                :icon="showNew ? 'visibility_off' : 'visibility'"
                :aria-label="showNew ? 'Hide password' : 'Show password'"
                @click="showNew = !showNew"
              />
            </template>
          </q-input>

          <q-input
            v-model="confirmPassword"
            outlined
            :type="showConfirm ? 'text' : 'password'"
            label="Confirm new password"
            autocomplete="new-password"
            :maxlength="maximumLength"
            :rules="[required, passwordsMatch]"
          >
            <template #prepend><q-icon name="check_circle_outline" /></template>
            <template #append>
              <q-btn
                flat
                round
                dense
                :icon="showConfirm ? 'visibility_off' : 'visibility'"
                :aria-label="showConfirm ? 'Hide password' : 'Show password'"
                @click="showConfirm = !showConfirm"
              />
            </template>
          </q-input>

          <div class="security-note">
            <q-icon name="shield" />
            <span
              >Your password is securely hashed and is never stored as readable
              text.</span
            >
          </div>

          <div class="dialog-actions">
            <q-btn v-close-popup flat no-caps label="Cancel" />
            <q-btn
              type="submit"
              color="primary"
              unelevated
              no-caps
              icon="lock_reset"
              label="Update password"
              :loading="submitting"
              :disable="!canSubmit"
            />
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useQuasar } from "quasar";
import { authApi } from "@/api/auth";
import { axios } from "@/api/client";

const props = defineProps<{ modelValue: boolean }>();
const emit = defineEmits<{
  (event: "update:modelValue", value: boolean): void;
}>();

const $q = useQuasar();
const form = ref<{ validate: () => Promise<boolean> } | null>(null);
const currentPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");
const minimumLength = ref(8);
const maximumLength = ref(20);
const showCurrent = ref(false);
const showNew = ref(false);
const showConfirm = ref(false);
const submitting = ref(false);

const open = computed({
  get: () => props.modelValue,
  set: value => emit("update:modelValue", value)
});
const canSubmit = computed(
  () =>
    currentPassword.value.length > 0 &&
    newPassword.value.length >= minimumLength.value &&
    newPassword.value.length <= maximumLength.value &&
    newPassword.value !== currentPassword.value &&
    confirmPassword.value === newPassword.value &&
    !submitting.value
);

function required(value: string) {
  return value.length > 0 || "This field is required";
}
function validLength(value: string) {
  return (
    (value.length >= minimumLength.value &&
      value.length <= maximumLength.value) ||
    `Password must contain ${minimumLength.value}–${maximumLength.value} characters`
  );
}
function differentPassword(value: string) {
  return value !== currentPassword.value || "Choose a different password";
}
function passwordsMatch(value: string) {
  return value === newPassword.value || "Passwords do not match";
}

async function loadPolicy() {
  try {
    const policy = await authApi.passwordPolicy();
    minimumLength.value = policy.minimum_length;
    maximumLength.value = policy.maximum_length;
  } catch {
    // Retain the secure platform defaults if the public policy is unavailable.
  }
}

async function submit() {
  if (!(await form.value?.validate()) || !canSubmit.value) return;
  submitting.value = true;
  try {
    await authApi.changePassword(currentPassword.value, newPassword.value);
    $q.notify({
      type: "positive",
      message: "Your password has been changed successfully"
    });
    open.value = false;
  } catch (error: unknown) {
    const detail = axios.isAxiosError(error)
      ? error.response?.data?.detail
      : null;
    $q.notify({
      type: "negative",
      message:
        typeof detail === "string"
          ? detail
          : "Your password could not be changed. Please try again."
    });
  } finally {
    submitting.value = false;
  }
}

function reset() {
  currentPassword.value = "";
  newPassword.value = "";
  confirmPassword.value = "";
  showCurrent.value = false;
  showNew.value = false;
  showConfirm.value = false;
}

watch(
  () => props.modelValue,
  value => {
    if (value) void loadPolicy();
  }
);
</script>

<style scoped lang="scss">
.password-dialog {
  width: min(470px, calc(100vw - 28px));
  border-radius: 15px;
  color: #29364a;
}
.dialog-header {
  display: flex;
  align-items: flex-start;
  gap: 13px;
  padding: 21px 21px 18px;
}
.header-icon {
  display: grid;
  flex: 0 0 42px;
  place-items: center;
  height: 42px;
  border-radius: 10px;
  color: #1769e0;
  background: #e9f2ff;
  font-size: 22px;
}
.dialog-header h2 {
  margin: 0 0 4px;
  color: #172033;
  font-size: 19px;
  letter-spacing: -0.3px;
}
.dialog-header p {
  margin: 0;
  color: #7b8798;
  font-size: 12px;
  line-height: 1.45;
}
.close-btn {
  margin: -4px -5px 0 auto;
  color: #7d8999;
}
.dialog-body {
  padding: 20px 22px 22px;
}
.password-form {
  display: grid;
  gap: 9px;
}
.password-form :deep(.q-field__control) {
  border-radius: 9px;
}
.password-form :deep(.q-field__prepend) {
  color: #788598;
}
.security-note {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 10px 12px;
  border-radius: 8px;
  color: #5f6d80;
  background: #f4f7fb;
  font-size: 11px;
  line-height: 1.45;
}
.security-note .q-icon {
  color: #249267;
  font-size: 17px;
}
.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 8px;
}
.dialog-actions .q-btn {
  min-height: 42px;
  padding: 0 17px;
  border-radius: 8px;
}
@media (max-width: 500px) {
  .dialog-header {
    padding: 18px 17px 15px;
  }
  .dialog-body {
    padding: 17px;
  }
  .dialog-actions .q-btn {
    flex: 1;
  }
}
</style>
