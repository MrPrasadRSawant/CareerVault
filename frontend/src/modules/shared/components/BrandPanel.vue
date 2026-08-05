<template>
  <div class="brand-panel">
    <div class="glow glow--teal"></div>
    <div class="glow glow--blue"></div>
    <div class="glow glow--amber"></div>

    <div class="brand-content">
      <div class="brand-mark">
        <q-icon name="rocket_launch" size="26px" />
      </div>
      <div class="brand-name"> Career<span>Vault</span> </div>
      <div class="brand-tagline">
        One place to manage your entire job search.
      </div>

      <div class="brand-divider"></div>

      <ul class="brand-features">
        <li class="brand-feature">
          <q-icon name="check_circle" size="20px" />
          <span>Track opportunities and applications</span>
        </li>
        <li class="brand-feature">
          <q-icon name="description" size="20px" />
          <span>Store resumes and cover letters</span>
        </li>
        <li class="brand-feature">
          <q-icon name="event_available" size="20px" />
          <span>Stay on top of interviews & follow-ups</span>
        </li>
      </ul>
    </div>

    <div class="brand-footer">© {{ currentYear }} CareerVault</div>
  </div>
</template>

<script setup lang="ts">
defineOptions({ name: "BrandPanel" });

const currentYear = new Date().getFullYear();
</script>

<style lang="scss" scoped>
.brand-panel {
  position: relative;
  flex: 0 0 52%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden;
  padding: 56px 64px;
  background: linear-gradient(155deg, #023047 0%, #023047 45%, #034d6b 100%);
}

.glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(90px);
  opacity: 0.55;
  pointer-events: none;
}

.glow--teal {
  width: 380px;
  height: 380px;
  top: -140px;
  right: -120px;
  background: #219ebc;
}

.glow--blue {
  width: 320px;
  height: 320px;
  bottom: -120px;
  left: -110px;
  background: #8ecae6;
  opacity: 0.35;
}

.glow--amber {
  width: 180px;
  height: 180px;
  bottom: 30%;
  right: 12%;
  background: #ffb703;
  opacity: 0.22;
}

.brand-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 420px;
}

.brand-mark {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  border-radius: 16px;
  color: #fff;
  background: linear-gradient(135deg, #219ebc 0%, #8ecae6 100%);
  box-shadow: 0 12px 30px rgba(33, 158, 188, 0.45);
}

.brand-name {
  font-size: 34px;
  font-weight: 700;
  letter-spacing: -0.5px;
  color: #fff;

  span {
    color: #ffb703;
  }
}

.brand-tagline {
  font-size: 17px;
  line-height: 1.6;
  color: #b6d6e2;
}

.brand-divider {
  width: 48px;
  height: 4px;
  border-radius: 2px;
  background: linear-gradient(90deg, #ffb703 0%, #fb8500 100%);
}

.brand-features {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.brand-feature {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #dcebf1;
  font-size: 15px;

  .q-icon {
    color: #8ecae6;
  }
}

.brand-footer {
  position: relative;
  z-index: 1;
  font-size: 13px;
  color: #7fa3b3;
}

@media (max-width: 1023px) {
  .brand-panel {
    display: none;
  }
}
</style>
