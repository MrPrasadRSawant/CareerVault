<template>
  <div class="auth-page">
    <BrandPanel />

    <div class="form-panel">
      <div class="mobile-brand">
        <div class="mobile-brand-mark">CV</div>
        <span>Career<span class="accent">Vault</span></span>
      </div>

      <div class="form-inner">
        <div class="form-heading">
          <div class="form-eyebrow">
            <q-icon name="verified_user" size="15px" />
            Secure access
          </div>
          <h1>{{ title }}</h1>
          <p>{{ subtitle }}</p>
        </div>

        <slot />

        <p class="form-hint">{{ footerText }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import BrandPanel from "./BrandPanel.vue";

defineOptions({ name: "AuthLayout" });

withDefaults(
  defineProps<{
    title: string;
    subtitle: string;
    footerText?: string;
  }>(),
  {
    footerText: "Your career data is private and securely stored."
  }
);
</script>

<style lang="scss" scoped>
.auth-page {
  display: flex;
  min-height: 100vh;
  background: #f3f5f7;
}

.form-panel {
  flex: 0 0 48%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 32px;
  background: #fff;
}

.form-inner {
  width: 100%;
  max-width: 405px;
  display: flex;
  flex-direction: column;
  padding: 0;
}

.mobile-brand-mark {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border-radius: 8px;
  color: #fff;
  background: #1769e0;
  box-shadow: 0 5px 14px rgba(23, 105, 224, 0.2);
  font-size: 12px;
  font-weight: 900;
  letter-spacing: -0.4px;
}

.form-heading {
  margin-bottom: 28px;

  .form-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 12px;
    padding: 5px 9px;
    border-radius: 999px;
    color: #1769e0;
    background: #edf4ff;
    font-size: 10.5px;
    font-weight: 750;
    letter-spacing: 0.35px;
    text-transform: uppercase;
  }

  h1 {
    margin: 0 0 8px;
    font-size: 27px;
    font-weight: 750;
    color: #172033;
    letter-spacing: -0.45px;
  }

  p {
    margin: 0;
    font-size: 15px;
    color: #748094;
  }
}

.form-hint {
  margin: 22px 0 0;
  font-size: 11.5px;
  line-height: 1.6;
  text-align: center;
  color: #98a2b1;
}

.mobile-brand {
  display: none;
  align-items: center;
  gap: 10px;
  margin-bottom: 36px;
  font-size: 18px;
  font-weight: 800;
  color: #172033;
}

.accent {
  color: #1769e0;
}

@media (max-width: 1023px) {
  .form-panel {
    flex-basis: 100%;
    background:
      radial-gradient(
        circle at 12% 8%,
        rgba(23, 105, 224, 0.09),
        transparent 34%
      ),
      #f3f5f7;
  }

  .mobile-brand {
    display: flex;
    align-self: flex-start;
  }
}

@media (max-width: 540px) {
  .form-panel {
    justify-content: flex-start;
    padding: 22px 16px;
  }

  .mobile-brand {
    margin-bottom: 22px;
  }

  .form-inner {
    max-width: none;
    padding: 28px 22px 24px;
    border: 1px solid #dfe4ea;
    border-radius: 14px;
    background: #fff;
    box-shadow: 0 10px 32px rgba(30, 42, 56, 0.08);
  }
}
</style>
