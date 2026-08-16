<template>
  <q-page class="settings-page">
    <header class="page-header">
      <div>
        <div class="eyebrow">Platform administration</div>
        <h1>Platform settings</h1>
        <p>Control account registration capacity and login security.</p>
      </div>
    </header>

    <div v-if="loading" class="loading-state">
      <q-spinner color="primary" size="36px" />
      <span>Loading platform settings…</span>
    </div>

    <template v-else-if="settings">
      <section class="usage-grid" aria-label="Today's registration usage">
        <article class="metric-card">
          <q-icon name="person_add" />
          <div>
            <span>Registered today</span>
            <strong>
              {{ settings.registrations_used_today.toLocaleString() }}
            </strong>
          </div>
        </article>
        <article class="metric-card">
          <q-icon name="group_add" />
          <div>
            <span>Remaining today</span>
            <strong>
              {{ settings.registrations_remaining_today.toLocaleString() }}
            </strong>
          </div>
        </article>
        <article class="metric-card">
          <q-icon name="event" />
          <div>
            <span>Counter date</span>
            <strong>{{ settings.counter_date_utc }}</strong>
            <small>UTC</small>
          </div>
        </article>
      </section>

      <section class="setting-card">
        <div class="setting-copy">
          <div class="setting-icon"><q-icon name="how_to_reg" /></div>
          <div>
            <h2>Daily registration limit</h2>
            <p>
              Maximum number of new applicant accounts that can be created in
              one UTC calendar day. Existing users can still sign in when this
              limit is reached.
            </p>
          </div>
        </div>

        <q-form class="setting-form" @submit="save">
          <q-input
            v-model.number="dailyLimit"
            type="number"
            outlined
            label="Accounts per day"
            hint="Allowed range: 1 to 1,000,000"
            :min="1"
            :max="1000000"
            :rules="[validateLimit]"
          />
          <q-btn
            type="submit"
            color="primary"
            unelevated
            no-caps
            label="Save limit"
            :loading="saving"
            :disable="!hasChanges"
          />
        </q-form>

        <div class="notice">
          <q-icon name="info_outline" />
          <span>
            If today's usage already exceeds a newly lowered limit, new
            registrations remain paused until the counter resets at 00:00 UTC.
          </span>
        </div>
      </section>

      <section v-if="securitySettings" class="setting-card">
        <div class="setting-copy">
          <div class="setting-icon security-icon">
            <q-icon name="lock_clock" />
          </div>
          <div>
            <h2>Failed login protection</h2>
            <p>
              Temporarily lock an account after consecutive invalid-password
              attempts. A successful login resets the failure count.
            </p>
          </div>
        </div>

        <q-form class="setting-form security-form" @submit="saveSecurity">
          <q-input
            v-model.number="failedAttemptLimit"
            type="number"
            outlined
            label="Failed attempts before lock"
            hint="Allowed range: 1 to 100"
            :min="1"
            :max="100"
            :rules="[validateAttemptLimit]"
          />
          <q-input
            v-model.number="lockoutDurationMinutes"
            type="number"
            outlined
            label="Lock duration in minutes"
            hint="Allowed range: 1 to 1,440"
            :min="1"
            :max="1440"
            :rules="[validateLockoutDuration]"
          />
          <q-btn
            type="submit"
            color="primary"
            unelevated
            no-caps
            label="Save protection"
            :loading="savingSecurity"
            :disable="!hasSecurityChanges"
          />
        </q-form>

        <div class="notice security-notice">
          <q-icon name="shield" />
          <span>
            Updated values apply to newly created locks. Existing active locks
            keep their current expiry. Every login attempt remains a separate
            audit event.
          </span>
        </div>
      </section>

      <section v-if="passwordPolicy" class="setting-card">
        <div class="setting-copy">
          <div class="setting-icon password-icon">
            <q-icon name="password" />
          </div>
          <div>
            <h2>Password length</h2>
            <p>
              Set the accepted password character range for registration and
              login. Both values must remain within 8–20 characters.
            </p>
          </div>
        </div>

        <q-form class="setting-form security-form" @submit="savePasswordPolicy">
          <q-input
            v-model.number="passwordMinimumLength"
            type="number"
            outlined
            label="Minimum characters"
            hint="Allowed range: 8 to 20"
            :min="8"
            :max="20"
            :rules="[validatePasswordMinimum]"
          />
          <q-input
            v-model.number="passwordMaximumLength"
            type="number"
            outlined
            label="Maximum characters"
            hint="Allowed range: 8 to 20"
            :min="8"
            :max="20"
            :rules="[validatePasswordMaximum]"
          />
          <q-btn
            type="submit"
            color="primary"
            unelevated
            no-caps
            label="Save password policy"
            :loading="savingPasswordPolicy"
            :disable="!hasPasswordPolicyChanges"
          />
        </q-form>

        <div class="notice">
          <q-icon name="info_outline" />
          <span>
            Changes apply immediately. Ensure existing users' passwords remain
            inside the selected range so they can continue signing in.
          </span>
        </div>
      </section>
    </template>

    <div v-else class="error-state">
      <q-icon name="error_outline" />
      <span>Platform settings could not be loaded.</span>
      <q-btn flat no-caps color="primary" label="Try again" @click="load" />
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useQuasar } from "quasar";
import {
  adminApi,
  type LoginSecuritySettings,
  type PasswordPolicySettings,
  type RegistrationSettings
} from "@/api/admin";

defineOptions({ name: "AdminSettingsPage" });

const $q = useQuasar();
const settings = ref<RegistrationSettings | null>(null);
const securitySettings = ref<LoginSecuritySettings | null>(null);
const passwordPolicy = ref<PasswordPolicySettings | null>(null);
const dailyLimit = ref<number | null>(null);
const failedAttemptLimit = ref<number | null>(null);
const lockoutDurationMinutes = ref<number | null>(null);
const passwordMinimumLength = ref<number | null>(null);
const passwordMaximumLength = ref<number | null>(null);
const loading = ref(true);
const saving = ref(false);
const savingSecurity = ref(false);
const savingPasswordPolicy = ref(false);

const hasChanges = computed(
  () =>
    dailyLimit.value !== null &&
    dailyLimit.value !== settings.value?.daily_registration_limit
);
const hasSecurityChanges = computed(
  () =>
    failedAttemptLimit.value !== null &&
    (failedAttemptLimit.value !==
      securitySettings.value?.failed_login_attempt_limit ||
      lockoutDurationMinutes.value !==
        securitySettings.value?.lockout_duration_minutes)
);
const hasPasswordPolicyChanges = computed(
  () =>
    passwordMinimumLength.value !== null &&
    passwordMaximumLength.value !== null &&
    (passwordMinimumLength.value !== passwordPolicy.value?.minimum_length ||
      passwordMaximumLength.value !== passwordPolicy.value?.maximum_length)
);

function validateLimit(value: number | null) {
  return (
    (value !== null &&
      Number.isInteger(value) &&
      value >= 1 &&
      value <= 1_000_000) ||
    "Enter a whole number from 1 to 1,000,000"
  );
}

function validateAttemptLimit(value: number | null) {
  return (
    (value !== null &&
      Number.isInteger(value) &&
      value >= 1 &&
      value <= 100) ||
    "Enter a whole number from 1 to 100"
  );
}

function validateLockoutDuration(value: number | null) {
  return (
    (value !== null &&
      Number.isInteger(value) &&
      value >= 1 &&
      value <= 1_440) ||
    "Enter a whole number from 1 to 1,440"
  );
}

function validatePasswordMinimum(value: number | null) {
  return (
    (value !== null &&
      Number.isInteger(value) &&
      value >= 8 &&
      value <= 20 &&
      (passwordMaximumLength.value === null ||
        value <= passwordMaximumLength.value)) ||
    "Minimum must be 8–20 and not exceed maximum"
  );
}

function validatePasswordMaximum(value: number | null) {
  return (
    (value !== null &&
      Number.isInteger(value) &&
      value >= 8 &&
      value <= 20 &&
      (passwordMinimumLength.value === null ||
        value >= passwordMinimumLength.value)) ||
    "Maximum must be 8–20 and not be below minimum"
  );
}

async function load() {
  loading.value = true;
  try {
    [settings.value, securitySettings.value, passwordPolicy.value] =
      await Promise.all([
      adminApi.registrationSettings(),
      adminApi.loginSecuritySettings(),
      adminApi.passwordPolicySettings()
    ]);
    dailyLimit.value = settings.value.daily_registration_limit;
    failedAttemptLimit.value =
      securitySettings.value.failed_login_attempt_limit;
    lockoutDurationMinutes.value =
      securitySettings.value.lockout_duration_minutes;
    passwordMinimumLength.value = passwordPolicy.value.minimum_length;
    passwordMaximumLength.value = passwordPolicy.value.maximum_length;
  } catch {
    settings.value = null;
    securitySettings.value = null;
    passwordPolicy.value = null;
  } finally {
    loading.value = false;
  }
}

async function saveSecurity() {
  if (
    failedAttemptLimit.value === null ||
    lockoutDurationMinutes.value === null ||
    validateAttemptLimit(failedAttemptLimit.value) !== true ||
    validateLockoutDuration(lockoutDurationMinutes.value) !== true
  ) {
    return;
  }
  savingSecurity.value = true;
  try {
    securitySettings.value = await adminApi.updateLoginSecuritySettings(
      failedAttemptLimit.value,
      lockoutDurationMinutes.value
    );
    failedAttemptLimit.value =
      securitySettings.value.failed_login_attempt_limit;
    lockoutDurationMinutes.value =
      securitySettings.value.lockout_duration_minutes;
    $q.notify({ type: "positive", message: "Login protection updated" });
  } catch {
    $q.notify({
      type: "negative",
      message: "Could not update login protection"
    });
  } finally {
    savingSecurity.value = false;
  }
}

async function savePasswordPolicy() {
  if (
    passwordMinimumLength.value === null ||
    passwordMaximumLength.value === null ||
    validatePasswordMinimum(passwordMinimumLength.value) !== true ||
    validatePasswordMaximum(passwordMaximumLength.value) !== true
  ) {
    return;
  }
  savingPasswordPolicy.value = true;
  try {
    passwordPolicy.value = await adminApi.updatePasswordPolicySettings(
      passwordMinimumLength.value,
      passwordMaximumLength.value
    );
    passwordMinimumLength.value = passwordPolicy.value.minimum_length;
    passwordMaximumLength.value = passwordPolicy.value.maximum_length;
    $q.notify({ type: "positive", message: "Password policy updated" });
  } catch {
    $q.notify({
      type: "negative",
      message: "Could not update the password policy"
    });
  } finally {
    savingPasswordPolicy.value = false;
  }
}

async function save() {
  if (dailyLimit.value === null || validateLimit(dailyLimit.value) !== true) {
    return;
  }
  saving.value = true;
  try {
    settings.value = await adminApi.updateRegistrationSettings(dailyLimit.value);
    dailyLimit.value = settings.value.daily_registration_limit;
    $q.notify({ type: "positive", message: "Daily registration limit updated" });
  } catch {
    $q.notify({
      type: "negative",
      message: "Could not update the registration limit"
    });
  } finally {
    saving.value = false;
  }
}

onMounted(load);
</script>

<style scoped lang="scss">
.settings-page {
  padding: 30px;
  color: #253247;
}
.page-header {
  max-width: 1080px;
  margin: 0 auto 22px;
}
.eyebrow {
  color: #1769e0;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}
h1 {
  margin: 4px 0;
  font-size: 28px;
  letter-spacing: -0.6px;
}
.page-header p,
.setting-copy p {
  margin: 0;
  color: #748095;
}
.usage-grid,
.setting-card,
.loading-state,
.error-state {
  max-width: 1080px;
  margin-right: auto;
  margin-left: auto;
}
.usage-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 16px;
}
.metric-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px;
  border: 1px solid #e1e6ec;
  border-radius: 12px;
  background: #fff;
}
.metric-card > .q-icon {
  padding: 10px;
  border-radius: 10px;
  color: #1769e0;
  background: #edf4ff;
  font-size: 23px;
}
.metric-card span,
.metric-card strong,
.metric-card small {
  display: block;
}
.metric-card span {
  color: #7b8798;
  font-size: 11px;
  font-weight: 650;
}
.metric-card strong {
  margin-top: 2px;
  color: #223047;
  font-size: 21px;
}
.metric-card small {
  color: #9aa4b2;
  font-size: 9px;
}
.setting-card {
  padding: 24px;
  border: 1px solid #e1e6ec;
  border-radius: 13px;
  background: #fff;
  box-shadow: 0 3px 12px rgba(31, 45, 61, 0.04);
}
.setting-card + .setting-card {
  margin-top: 16px;
}
.setting-copy {
  display: flex;
  gap: 14px;
}
.setting-icon {
  display: grid;
  flex: 0 0 42px;
  place-items: center;
  height: 42px;
  border-radius: 10px;
  color: #1769e0;
  background: #edf4ff;
  font-size: 22px;
}
.security-icon {
  color: #8b5e00;
  background: #fff4d6;
}
.password-icon {
  color: #7657c9;
  background: #f1edff;
}
h2 {
  margin: 0 0 5px;
  font-size: 17px;
}
.setting-copy p {
  max-width: 720px;
  line-height: 1.55;
}
.setting-form {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  max-width: 520px;
  margin-top: 24px;
}
.security-form {
  max-width: 760px;
}
.setting-form .q-field {
  flex: 1;
}
.setting-form .q-btn {
  min-height: 48px;
  padding: 0 22px;
  border-radius: 8px;
}
.notice {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-top: 16px;
  padding: 11px 13px;
  border-radius: 8px;
  color: #5f6d80;
  background: #f5f8fc;
  font-size: 12px;
}
.security-notice .q-icon {
  color: #22a06b;
}
.loading-state,
.error-state {
  display: flex;
  min-height: 260px;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #778397;
}
.error-state .q-icon {
  color: #c33b4a;
  font-size: 24px;
}
@media (max-width: 700px) {
  .settings-page {
    padding: 20px 14px;
  }
  .usage-grid {
    grid-template-columns: 1fr;
  }
  .setting-form {
    display: block;
  }
  .setting-form .q-btn {
    width: 100%;
    margin-top: 8px;
  }
}
</style>
