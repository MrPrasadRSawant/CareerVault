<template>
  <section class="brand-panel" aria-label="CareerVault overview">
    <span class="decorative-orbit decorative-orbit--one"></span>
    <span class="decorative-orbit decorative-orbit--two"></span>

    <div class="brand-content">
      <div class="brand-lockup">
        <div class="brand-mark">CV</div>
        <div class="brand-name">Career<span>Vault</span></div>
      </div>

      <div class="brand-copy">
        <div class="brand-eyebrow">Your career workspace</div>
        <h2>Keep every opportunity moving forward.</h2>
        <p>
          Organize applications, documents, interviews, and follow-ups in one
          focused place.
        </p>
      </div>

      <div class="workspace-preview" aria-hidden="true">
        <div class="preview-toolbar">
          <span class="preview-logo">CV</span>
          <span class="preview-search"></span>
          <span class="preview-avatar"></span>
        </div>
        <div class="preview-content">
          <div class="preview-heading">
            <div><span></span><span></span></div>
            <i></i>
          </div>
          <div class="preview-stats">
            <div
              ><span class="stat-icon stat-icon--blue"></span><strong>24</strong
              ><small>Opportunities</small></div
            >
            <div
              ><span class="stat-icon stat-icon--violet"></span
              ><strong>11</strong><small>Applications</small></div
            >
            <div
              ><span class="stat-icon stat-icon--amber"></span><strong>3</strong
              ><small>Interviews</small></div
            >
          </div>
          <div class="preview-panels">
            <div class="preview-chart">
              <span></span><span></span><span></span><span></span>
            </div>
            <div class="preview-list">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>
      </div>

      <ul class="brand-features">
        <li
          ><q-icon name="check_circle" /><span
            >Private, organized, and built for your job search</span
          ></li
        >
        <li
          ><q-icon name="check_circle" /><span
            >See your complete application pipeline at a glance</span
          ></li
        >
      </ul>
    </div>

    <div class="brand-footer">© {{ currentYear }} CareerVault</div>
  </section>
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
  padding: 44px clamp(38px, 5vw, 76px) 32px;
  color: #fff;
  background:
    radial-gradient(
      circle at 82% 12%,
      rgba(116, 178, 255, 0.48),
      transparent 30%
    ),
    radial-gradient(circle at 8% 88%, rgba(99, 91, 223, 0.5), transparent 34%),
    linear-gradient(145deg, #0f4fae 0%, #1769e0 52%, #315cca 100%);
}

.decorative-orbit {
  position: absolute;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 50%;
  pointer-events: none;
}

.decorative-orbit--one {
  width: 420px;
  height: 420px;
  top: -245px;
  right: -125px;
}

.decorative-orbit--two {
  width: 270px;
  height: 270px;
  bottom: -165px;
  left: -90px;
}

.brand-content {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 590px;
  margin: auto;
}

.brand-lockup {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-mark {
  display: grid;
  place-items: center;
  width: 38px;
  height: 38px;
  border-radius: 9px;
  color: #1769e0;
  background: #fff;
  box-shadow: 0 7px 20px rgba(14, 52, 109, 0.22);
  font-size: 13px;
  font-weight: 900;
}

.brand-name {
  color: #fff;
  font-size: 20px;
  font-weight: 800;
  letter-spacing: -0.45px;

  span {
    color: #bcd7ff;
  }
}

.brand-copy {
  margin-top: clamp(34px, 6vh, 62px);
}
.brand-eyebrow {
  color: #c9defe;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}
.brand-copy h2 {
  max-width: 500px;
  margin: 9px 0 10px;
  color: #fff;
  font-size: clamp(28px, 2.4vw, 40px);
  font-weight: 780;
  letter-spacing: -1.2px;
  line-height: 1.12;
}
.brand-copy p {
  max-width: 500px;
  margin: 0;
  color: #dbe8ff;
  font-size: 14px;
  line-height: 1.65;
}

.workspace-preview {
  width: min(100%, 545px);
  margin-top: 28px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.36);
  border-radius: 13px;
  background: #f5f7fa;
  box-shadow: 0 24px 55px rgba(8, 39, 91, 0.3);
  transform: perspective(1000px) rotateY(-1.5deg);
}

.preview-toolbar {
  display: flex;
  align-items: center;
  gap: 9px;
  height: 38px;
  padding: 0 11px;
  border-bottom: 1px solid #e2e7ed;
  background: #fff;
}
.preview-logo {
  display: grid;
  place-items: center;
  width: 21px;
  height: 21px;
  border-radius: 5px;
  color: #fff;
  background: #1769e0;
  font-size: 7px;
  font-weight: 900;
}
.preview-search {
  width: 110px;
  height: 15px;
  border-radius: 8px;
  background: #eef1f5;
}
.preview-avatar {
  width: 18px;
  height: 18px;
  margin-left: auto;
  border-radius: 50%;
  background: linear-gradient(135deg, #1769e0, #635bdf);
}
.preview-content {
  padding: 15px;
}
.preview-heading {
  display: flex;
  justify-content: space-between;
}
.preview-heading div {
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.preview-heading span {
  display: block;
  width: 100px;
  height: 7px;
  border-radius: 4px;
  background: #cad2dd;
}
.preview-heading span:last-child {
  width: 145px;
  height: 5px;
  background: #e0e5eb;
}
.preview-heading i {
  width: 70px;
  height: 22px;
  border-radius: 11px;
  background: #1769e0;
}
.preview-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 9px;
  margin-top: 15px;
}
.preview-stats > div {
  display: grid;
  grid-template-columns: 25px 1fr;
  grid-template-rows: 1fr 1fr;
  column-gap: 8px;
  padding: 10px;
  border: 1px solid #e2e7ed;
  border-radius: 8px;
  background: #fff;
}
.preview-stats strong {
  color: #253247;
  font-size: 13px;
  line-height: 1;
}
.preview-stats small {
  color: #919aa8;
  font-size: 7px;
}
.stat-icon {
  grid-row: 1 / 3;
  width: 25px;
  height: 25px;
  border-radius: 7px;
}
.stat-icon--blue {
  background: #e7f0ff;
}
.stat-icon--violet {
  background: #efedff;
}
.stat-icon--amber {
  background: #fff2d7;
}
.preview-panels {
  display: grid;
  grid-template-columns: 1.3fr 0.8fr;
  gap: 9px;
  margin-top: 9px;
}
.preview-chart,
.preview-list {
  height: 83px;
  padding: 10px;
  border: 1px solid #e2e7ed;
  border-radius: 8px;
  background: #fff;
}
.preview-chart {
  display: flex;
  align-items: flex-end;
  gap: 8px;
}
.preview-chart span {
  flex: 1;
  border-radius: 3px 3px 0 0;
  background: #dce9ff;
}
.preview-chart span:nth-child(1) {
  height: 35%;
}
.preview-chart span:nth-child(2) {
  height: 62%;
}
.preview-chart span:nth-child(3) {
  height: 48%;
}
.preview-chart span:nth-child(4) {
  height: 78%;
  background: #4d91ed;
}
.preview-list {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
}
.preview-list span {
  height: 8px;
  border-radius: 4px;
  background: #e4e8ee;
}
.preview-list span:nth-child(2) {
  width: 78%;
}
.preview-list span:nth-child(3) {
  width: 88%;
}

.brand-features {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin: 20px 0 0;
  padding: 0;
  list-style: none;
}
.brand-features li {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #e2ecff;
  font-size: 11.5px;
}
.brand-features .q-icon {
  color: #9de9c6;
  font-size: 17px;
}
.brand-footer {
  position: relative;
  z-index: 1;
  margin-top: 22px;
  color: rgba(255, 255, 255, 0.58);
  font-size: 11px;
}

@media (max-height: 760px) {
  .brand-panel {
    padding-top: 30px;
  }
  .brand-copy {
    margin-top: 28px;
  }
  .workspace-preview {
    margin-top: 20px;
  }
  .brand-features {
    margin-top: 14px;
  }
}

@media (max-width: 1023px) {
  .brand-panel {
    display: none;
  }
}
</style>
