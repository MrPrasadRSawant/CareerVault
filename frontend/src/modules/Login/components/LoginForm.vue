<template>
  <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
    <q-input
      v-model="email"
      type="email"
      label="Email address"
      outlined
      class="form-input"
      :rules="[isRequired, isEmail]"
      autocomplete="email"
      data-autofocus
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
      :rules="[isRequired, passwordLength]"
      :maxlength="passwordMaximumLength"
      :hint="`${passwordMinimumLength}–${passwordMaximumLength} characters`"
      autocomplete="current-password"
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

    <q-btn
      type="submit"
      label="Sign in"
      unelevated
      no-caps
      class="signin-btn full-width"
      :loading="submitting"
      :disabled="!canSubmit && !submitting"
    />

    <div class="divider">
      <span>or</span>
    </div>

    <q-btn
      type="button"
      label="Create an account"
      unelevated
      no-caps
      outline
      class="register-btn full-width"
      :to="{ name: 'register' }"
    />
  </q-form>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useLogin } from "../composables/useLogin";

defineOptions({ name: "LoginForm" });

const {
  email,
  password,
  submitting,
  canSubmit,
  isRequired,
  isEmail,
  passwordLength,
  passwordMinimumLength,
  passwordMaximumLength,
  onSubmit,
  onReset
} = useLogin();

const showPassword = ref(false);
</script>

<style lang="scss" scoped>
.form-input {
  :deep(.q-field__control) {
    height: 48px;
    border-radius: 9px;
    background: #f9fafc;
  }

  :deep(.q-field__control::before) {
    border-color: #d3d9e1;
  }

  :deep(.q-field__control:hover::before) {
    border-color: #aab5c4;
  }

  :deep(.q-field__prepend),
  :deep(.q-field__append) {
    color: #7c8798;
  }

  &.q-field--focused :deep(.q-field__control) {
    background: #fff;
    box-shadow: 0 0 0 3px rgba(23, 105, 224, 0.08);
  }
}

.signin-btn {
  height: 48px;
  margin-top: 8px;
  border-radius: 9px;
  color: #fff;
  background: #1769e0;
  box-shadow: 0 8px 20px rgba(23, 105, 224, 0.25);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0;

  &:hover {
    background: #145bc2;
    box-shadow: 0 10px 24px rgba(23, 105, 224, 0.3);
  }

  :deep(.q-spinner) {
    color: #fff;
  }
}

.register-btn {
  height: 48px;
  border-radius: 9px;
  color: #1769e0;
  border-color: #c9d3e1;
  font-size: 14px;
  font-weight: 650;

  :deep(span) {
    color: #1769e0;
  }
}

.divider {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 4px 0;
  color: #98a2b1;
  font-size: 12px;

  &::before,
  &::after {
    content: "";
    flex: 1;
    height: 1px;
    background: #e5e9ee;
  }
}
</style>
