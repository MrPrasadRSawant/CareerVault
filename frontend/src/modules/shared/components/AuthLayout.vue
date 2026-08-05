<template>
  <div class="auth-page">
    <BrandPanel />

    <div class="form-panel">
      <div class="mobile-brand">
        <div class="mobile-brand-mark">
          <q-icon name="rocket_launch" size="20px" />
        </div>
        <span>Career<span class="accent">Vault</span></span>
      </div>

      <div class="form-inner">
        <div class="form-heading">
          <h1>{{ title }}</h1>
          <p>{{ subtitle }}</p>
        </div>

        <slot />

        <p class="form-hint">
          By signing up you agree to the Terms of Service and Privacy Policy.
        </p>
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
  }>(),
  {}
);
</script>

<style lang="scss" scoped>
.auth-page {
  display: flex;
  min-height: 100vh;
}

.form-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 32px;
  background: #f8fafc;
}

.form-inner {
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
}

.form-heading {
  margin-bottom: 28px;

  h1 {
    margin: 0 0 8px;
    font-size: 28px;
    font-weight: 700;
    color: #023047;
    letter-spacing: -0.3px;
  }

  p {
    margin: 0;
    font-size: 15px;
    color: #64748b;
  }
}

.form-hint {
  margin: 24px 0 0;
  font-size: 12.5px;
  line-height: 1.6;
  text-align: center;
  color: #94a3b8;
}

.mobile-brand {
  display: none;
  align-items: center;
  gap: 10px;
  margin-bottom: 36px;
  font-size: 20px;
  font-weight: 700;
  color: #023047;
}

.mobile-brand-mark {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  color: #fff;
  background: linear-gradient(135deg, #219ebc 0%, #8ecae6 100%);
}

.accent {
  color: #fb8500;
}

@media (max-width: 1023px) {
  .mobile-brand {
    display: flex;
    align-self: flex-start;
  }
}
</style>
