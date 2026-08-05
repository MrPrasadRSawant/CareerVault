<template>
  <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
    <q-input
      v-model="email"
      type="email"
      label="Email address"
      outlined
      rounded
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
      rounded
      class="form-input"
      :rules="[isRequired]"
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
  onSubmit,
  onReset
} = useLogin();

const showPassword = ref(false);
</script>

<style lang="scss" scoped>
.form-input {
  :deep(.q-field__control) {
    height: 48px;
  }

  :deep(.q-field__control::before) {
    border-color: #cbd5e1;
  }
}

.signin-btn {
  height: 48px;
  margin-top: 8px;
  border-radius: 24px;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.3px;
  background: linear-gradient(135deg, #219ebc 0%, #1b7f99 100%);
  box-shadow: 0 10px 24px rgba(33, 158, 188, 0.35);

  :deep(.q-spinner) {
    color: #fff;
  }
}

.register-btn {
  height: 48px;
  border-radius: 24px;
  font-size: 15px;
  font-weight: 500;
  color: #023047;
  border-color: #cbd5e1;

  :deep(span) {
    color: #023047;
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
