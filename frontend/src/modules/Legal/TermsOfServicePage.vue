<template>
  <div class="terms-page">
    <header class="terms-header">
      <router-link :to="homeRoute" class="brand-link">
        <span class="brand-mark">CV</span>
        <span class="brand-name">Career<span>Vault</span></span>
      </router-link>
      <q-btn
        outline
        no-caps
        color="primary"
        :label="
          auth.isAuthenticated ? 'Back to CareerVault' : 'Back to sign in'
        "
        :to="homeRoute"
      />
    </header>

    <main class="terms-shell">
      <div class="document-heading">
        <div class="document-icon"><q-icon name="gavel" /></div>
        <div>
          <div class="eyebrow">Legal</div>
          <h1>Terms of Service</h1>
          <p v-if="terms">
            Version {{ terms.version }} · Updated
            {{ formatDate(terms.updated_at) }}
          </p>
        </div>
      </div>

      <section v-if="loading" class="document-state">
        <q-spinner color="primary" size="34px" />
        <span>Loading Terms of Service…</span>
      </section>
      <article
        v-else-if="terms"
        class="terms-document"
        v-html="terms.content_html"
      ></article>
      <section v-else class="document-state document-state--error">
        <q-icon name="error_outline" size="30px" />
        <span>The Terms of Service could not be loaded.</span>
        <q-btn flat no-caps color="primary" label="Try again" @click="load" />
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { legalApi, type TermsOfService } from "@/api/legal";
import { useAuthStore } from "@/stores/auth";

defineOptions({ name: "TermsOfServicePage" });

const auth = useAuthStore();
const terms = ref<TermsOfService | null>(null);
const loading = ref(true);
const homeRoute = computed(() => {
  if (!auth.isAuthenticated) return { name: "login" };
  return auth.isSystemAdmin
    ? { name: "system-admin-overview" }
    : { name: "dashboard" };
});

function formatDate(value: string) {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "long"
  }).format(new Date(value));
}

async function load() {
  loading.value = true;
  try {
    terms.value = await legalApi.termsOfService();
  } catch {
    terms.value = null;
  } finally {
    loading.value = false;
  }
}

onMounted(load);
</script>

<style scoped lang="scss">
.terms-page {
  min-height: 100vh;
  color: #253247;
  background:
    radial-gradient(circle at 8% 0%, rgba(23, 105, 224, 0.1), transparent 30%),
    #f3f5f7;
}
.terms-header {
  display: flex;
  min-height: 68px;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  border-bottom: 1px solid #e0e5eb;
  background: rgba(255, 255, 255, 0.96);
}
.brand-link {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #172033;
  text-decoration: none;
}
.brand-mark {
  display: grid;
  place-items: center;
  width: 35px;
  height: 35px;
  border-radius: 8px;
  color: #fff;
  background: #1769e0;
  font-size: 12px;
  font-weight: 900;
}
.brand-name {
  font-size: 19px;
  font-weight: 800;
}
.brand-name span,
.eyebrow {
  color: #1769e0;
}
.terms-shell {
  width: min(860px, calc(100% - 32px));
  margin: 42px auto 70px;
}
.document-heading {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}
.document-icon {
  display: grid;
  flex: 0 0 52px;
  place-items: center;
  height: 52px;
  border-radius: 13px;
  color: #1769e0;
  background: #e7f0ff;
  font-size: 26px;
}
.eyebrow {
  font-size: 10.5px;
  font-weight: 800;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}
.document-heading h1 {
  margin: 1px 0 2px;
  color: #172033;
  font-size: 30px;
  letter-spacing: -0.6px;
}
.document-heading p {
  margin: 0;
  color: #8290a3;
  font-size: 12px;
}
.terms-document,
.document-state {
  padding: 38px 44px;
  border: 1px solid #dfe5eb;
  border-radius: 15px;
  background: #fff;
  box-shadow: 0 10px 30px rgba(31, 45, 61, 0.06);
}
.terms-document {
  color: #445166;
  font-size: 14.5px;
  line-height: 1.75;
}
.terms-document :deep(h1) {
  margin: 0 0 22px;
  color: #172033;
  font-size: 25px;
}
.terms-document :deep(h2) {
  margin: 26px 0 7px;
  color: #263449;
  font-size: 17px;
}
.terms-document :deep(a) {
  color: #1769e0;
}
.terms-document :deep(li) {
  margin: 5px 0;
}
.document-state {
  display: flex;
  min-height: 260px;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #768398;
}
.document-state--error {
  color: #b63442;
}
@media (max-width: 600px) {
  .terms-header {
    padding: 0 16px;
  }
  .brand-name {
    display: none;
  }
  .terms-shell {
    margin-top: 26px;
  }
  .terms-document,
  .document-state {
    padding: 25px 22px;
  }
  .document-heading h1 {
    font-size: 25px;
  }
}
</style>
