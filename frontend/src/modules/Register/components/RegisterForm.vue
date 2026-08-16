<template>
  <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
    <q-input
      v-model="fullName"
      label="Full name"
      outlined
      class="form-input"
      :rules="[isRequired]"
      autocomplete="name"
    >
      <template #prepend>
        <q-icon name="person_outline" />
      </template>
    </q-input>

    <q-input
      v-model="email"
      type="email"
      label="Email address"
      outlined
      class="form-input"
      :rules="[isRequired, isEmail]"
      autocomplete="email"
    >
      <template #prepend>
        <q-icon name="mail_outline" />
      </template>
    </q-input>

    <q-input
      v-model="password"
      :type="showPassword ? 'text' : 'password'"
      label="Password"
      outlined
      class="form-input"
      :hint="`${passwordMinimumLength}–${passwordMaximumLength} characters`"
      :maxlength="passwordMaximumLength"
      :rules="[isRequired, passwordLength]"
      autocomplete="new-password"
    >
      <template #prepend>
        <q-icon name="lock_outline" />
      </template>
      <template #append>
        <q-btn
          flat
          round
          dense
          :icon="showPassword ? 'visibility_off' : 'visibility'"
          :aria-label="showPassword ? 'Hide password' : 'Show password'"
          @click="showPassword = !showPassword"
        />
      </template>
    </q-input>

    <q-input
      v-model="confirmPassword"
      :type="showConfirmPassword ? 'text' : 'password'"
      label="Confirm password"
      outlined
      class="form-input"
      :rules="[isRequired, passwordMatches]"
      :maxlength="passwordMaximumLength"
      autocomplete="new-password"
    >
      <template #prepend>
        <q-icon name="lock_outline" />
      </template>
      <template #append>
        <q-btn
          flat
          round
          dense
          :icon="showConfirmPassword ? 'visibility_off' : 'visibility'"
          :aria-label="showConfirmPassword ? 'Hide password' : 'Show password'"
          @click="showConfirmPassword = !showConfirmPassword"
        />
      </template>
    </q-input>

    <q-btn
      type="submit"
      label="Create account"
      unelevated
      no-caps
      class="submit-btn full-width"
      :loading="submitting"
      :disabled="!canSubmit && !submitting"
    />

    <div class="divider">
      <span>or</span>
    </div>

    <q-btn
      type="button"
      label="Already have an account? Sign in"
      unelevated
      no-caps
      outline
      class="signin-btn full-width"
      :to="{ name: 'login' }"
    />
  </q-form>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRegister } from "../composables/useRegister";

defineOptions({ name: "RegisterForm" });

const {
  fullName,
  email,
  password,
  confirmPassword,
  submitting,
  canSubmit,
  isRequired,
  isEmail,
  passwordLength,
  passwordMinimumLength,
  passwordMaximumLength,
  passwordMatches,
  onSubmit,
  onReset
} = useRegister();

const showPassword = ref(false);
const showConfirmPassword = ref(false);
</script>

<style lang="scss" scoped>
.form-input {
  :deep(.q-field__control) {
    height: 48px;
    border-radius: 9px;
  }

  :deep(.q-field__control::before) {
    border-color: #d3d9e1;
  }
}

.submit-btn {
  height: 48px;
  margin-top: 8px;
  border-radius: 9px;
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.3px;
  background: #1769e0;
  box-shadow: 0 7px 18px rgba(23, 105, 224, 0.22);

  :deep(.q-spinner) {
    color: #fff;
  }
}

.signin-btn {
  height: 48px;
  border-radius: 9px;
  font-size: 15px;
  font-weight: 500;
  color: #1769e0;
  border-color: #c9d3e1;

  :deep(span) {
    color: #1769e0;
  }
}

.divider {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 4px 0;
  color: #94a3b8;
  font-size: 13px;

  &::before,
  &::after {
    content: "";
    flex: 1;
    height: 1px;
    background: #e2e8f0;
  }
}
</style>
