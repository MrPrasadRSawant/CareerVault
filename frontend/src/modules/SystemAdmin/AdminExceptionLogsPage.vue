<template>
  <q-page class="exceptions-page">
    <header class="page-header">
      <div>
        <div class="eyebrow">Incident troubleshooting</div>
        <h1>Exception logs</h1>
        <p
          >Investigate unexpected server errors using safe diagnostic
          context.</p
        >
      </div>
      <q-btn
        outline
        no-caps
        color="primary"
        icon="refresh"
        label="Refresh"
        :loading="loading"
        @click="load"
      />
    </header>

    <section class="metric-grid" aria-label="Exception summary">
      <article class="metric-card">
        <q-icon name="error_outline" class="danger" />
        <div
          ><span>Last 24 hours</span
          ><strong>{{ overview.exceptions_last_24_hours }}</strong></div
        >
      </article>
      <article class="metric-card">
        <q-icon name="date_range" />
        <div
          ><span>Last 7 days</span
          ><strong>{{ overview.exceptions_last_7_days }}</strong></div
        >
      </article>
      <article class="metric-card">
        <q-icon name="fingerprint" />
        <div
          ><span>Unique issues · 24h</span
          ><strong>{{
            overview.unique_fingerprints_last_24_hours
          }}</strong></div
        >
      </article>
      <article class="metric-card">
        <q-icon name="inventory_2" />
        <div
          ><span>Retention</span
          ><strong>{{ overview.retention_days }} days</strong></div
        >
      </article>
    </section>

    <q-banner class="privacy-banner">
      <template #avatar><q-icon name="shield" /></template>
      Request bodies, authorization tokens, cookies, and query values are not
      stored. Sensitive values in exception messages and traces are redacted.
    </q-banner>

    <section class="logs-card">
      <div class="toolbar">
        <div>
          <h2>Recorded exceptions</h2>
          <p>{{ total.toLocaleString() }} unexpected server errors</p>
        </div>
        <q-input
          v-model="search"
          dense
          outlined
          clearable
          debounce="300"
          class="search-input"
          placeholder="Request ID, exception, route, user..."
          @keyup.enter="applySearch"
          @clear="applySearch"
        >
          <template #prepend><q-icon name="search" /></template>
          <template #append>
            <q-btn flat round dense icon="arrow_forward" @click="applySearch" />
          </template>
        </q-input>
      </div>

      <q-linear-progress v-if="loading" indeterminate color="primary" />
      <div v-if="error" class="state-message error-message">
        <q-icon name="error_outline" /> {{ error }}
      </div>
      <div v-else-if="!loading && items.length === 0" class="state-message">
        <q-icon name="check_circle_outline" /> No exception logs found.
      </div>

      <div v-else class="log-list">
        <article v-for="item in items" :key="item.id" class="log-row">
          <div class="status-code">{{ item.status_code }}</div>
          <div class="log-main">
            <div class="log-title-line">
              <strong>{{ item.exception_type }}</strong>
              <span class="method">{{ item.method }}</span>
              <code>{{ item.route_template }}</code>
            </div>
            <p>{{ item.message }}</p>
            <div class="metadata">
              <span
                ><q-icon name="schedule" />
                {{ formatDate(item.occurred_at) }}</span
              >
              <span><q-icon name="tag" /> {{ item.request_id }}</span>
              <span v-if="item.user_email"
                ><q-icon name="person_outline" /> {{ item.user_email }}</span
              >
              <span><q-icon name="dns" /> {{ item.app_environment }}</span>
            </div>
          </div>
          <q-btn
            flat
            no-caps
            color="primary"
            label="Inspect"
            icon-right="chevron_right"
            @click="showDetail(item)"
          />
        </article>
      </div>

      <div v-if="total > 25" class="pagination-row">
        <q-pagination
          :model-value="page"
          :max="maxPage"
          :max-pages="7"
          direction-links
          boundary-links
          @update:model-value="changePage"
        />
      </div>
    </section>

    <q-dialog v-model="detailOpen" maximized-transition persistent>
      <q-card class="detail-dialog">
        <q-card-section class="detail-header">
          <div>
            <div class="eyebrow">Exception detail</div>
            <h2>{{ detail?.exception_type || "Loading..." }}</h2>
          </div>
          <q-btn flat round icon="close" aria-label="Close" v-close-popup />
        </q-card-section>

        <q-linear-progress v-if="detailLoading" indeterminate color="primary" />
        <template v-if="detail">
          <q-card-section class="detail-grid">
            <div
              ><span>Request ID</span><code>{{ detail.request_id }}</code></div
            >
            <div
              ><span>Occurred</span
              ><strong>{{ formatDate(detail.occurred_at) }}</strong></div
            >
            <div
              ><span>Route</span
              ><code>{{ detail.method }} {{ detail.route_template }}</code></div
            >
            <div
              ><span>User</span
              ><strong>{{
                detail.user_email || "Unauthenticated"
              }}</strong></div
            >
            <div
              ><span>IP address</span
              ><strong>{{ detail.ip_address || "Unavailable" }}</strong></div
            >
            <div
              ><span>Fingerprint</span
              ><code>{{ detail.fingerprint.slice(0, 16) }}</code></div
            >
          </q-card-section>
          <q-card-section>
            <h3>Sanitized message</h3>
            <div class="message-box">{{ detail.message }}</div>
          </q-card-section>
          <q-card-section>
            <div class="trace-heading">
              <h3>Sanitized stack trace</h3>
              <q-btn
                flat
                dense
                no-caps
                icon="content_copy"
                label="Copy"
                @click="copyTrace"
              />
            </div>
            <pre class="traceback">{{ detail.traceback }}</pre>
          </q-card-section>
        </template>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useQuasar } from "quasar";
import type { AdminExceptionLog } from "@/api/admin";
import { useAdminExceptions } from "./composables/useAdminExceptions";

defineOptions({ name: "AdminExceptionLogsPage" });

const $q = useQuasar();
const detailOpen = ref(false);
const {
  overview,
  items,
  detail,
  total,
  page,
  maxPage,
  search,
  loading,
  detailLoading,
  error,
  load,
  applySearch,
  changePage,
  openDetail
} = useAdminExceptions();

function formatDate(value: string) {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "medium"
  }).format(new Date(value));
}

async function showDetail(item: AdminExceptionLog) {
  detailOpen.value = true;
  await openDetail(item);
}

async function copyTrace() {
  if (!detail.value) return;
  await navigator.clipboard.writeText(detail.value.traceback);
  $q.notify({ type: "positive", message: "Stack trace copied" });
}

onMounted(load);
</script>

<style scoped lang="scss">
.exceptions-page {
  padding: 30px;
  color: #253247;
}
.page-header {
  display: flex;
  max-width: 1180px;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin: 0 auto 20px;
}
.eyebrow {
  color: #1769e0;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}
h1 {
  margin: 3px 0;
  font-size: 28px;
  letter-spacing: -0.6px;
}
.page-header p,
.toolbar p {
  margin: 0;
  color: #758195;
}
.metric-grid {
  display: grid;
  max-width: 1180px;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  margin: 0 auto 14px;
}
.metric-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border: 1px solid #e1e6ec;
  border-radius: 11px;
  background: #fff;
}
.metric-card > .q-icon {
  padding: 9px;
  border-radius: 9px;
  color: #1769e0;
  background: #edf4ff;
  font-size: 21px;
}
.metric-card > .danger {
  color: #bd3443;
  background: #fff0f2;
}
.metric-card span,
.metric-card strong {
  display: block;
}
.metric-card span {
  color: #7d8899;
  font-size: 10.5px;
  font-weight: 650;
}
.metric-card strong {
  margin-top: 2px;
  font-size: 19px;
}
.privacy-banner,
.logs-card {
  max-width: 1180px;
  margin-right: auto;
  margin-left: auto;
}
.privacy-banner {
  margin-bottom: 14px;
  border: 1px solid #dce8fb;
  border-radius: 10px;
  color: #52657f;
  background: #f4f8ff;
  font-size: 12px;
}
.privacy-banner .q-icon {
  color: #1769e0;
}
.logs-card {
  overflow: hidden;
  border: 1px solid #e1e6ec;
  border-radius: 12px;
  background: #fff;
}
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 18px 20px;
}
.toolbar h2 {
  margin: 0;
  font-size: 17px;
}
.toolbar p {
  font-size: 11px;
}
.search-input {
  width: min(390px, 100%);
}
.log-row {
  display: grid;
  grid-template-columns: 48px minmax(0, 1fr) auto;
  align-items: start;
  gap: 14px;
  padding: 17px 20px;
  border-top: 1px solid #edf0f3;
}
.status-code {
  display: grid;
  place-items: center;
  width: 44px;
  height: 30px;
  border-radius: 7px;
  color: #b52f3a;
  background: #fff0f2;
  font-size: 12px;
  font-weight: 800;
}
.log-title-line {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}
.log-title-line strong {
  font-size: 13px;
}
.log-title-line code,
.method {
  padding: 3px 6px;
  border-radius: 5px;
  color: #536177;
  background: #f1f4f7;
  font-size: 10px;
}
.method {
  color: #1769e0;
  background: #edf4ff;
  font-weight: 800;
}
.log-main p {
  overflow: hidden;
  margin: 7px 0;
  color: #5c687a;
  font-size: 12px;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.metadata {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  color: #8792a2;
  font-size: 10px;
}
.metadata span {
  display: flex;
  align-items: center;
  gap: 4px;
}
.state-message {
  display: flex;
  min-height: 180px;
  align-items: center;
  justify-content: center;
  gap: 7px;
  color: #738095;
}
.state-message .q-icon {
  color: #22a06b;
  font-size: 23px;
}
.error-message .q-icon {
  color: #bd3443;
}
.pagination-row {
  display: flex;
  justify-content: flex-end;
  padding: 14px 20px;
  border-top: 1px solid #edf0f3;
}
.detail-dialog {
  width: min(980px, 94vw);
  max-width: 980px;
  max-height: 90vh;
  border-radius: 14px;
}
.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e6eaf0;
}
.detail-header h2 {
  margin: 2px 0 0;
  font-size: 19px;
}
.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}
.detail-grid > div {
  padding: 11px;
  border-radius: 8px;
  background: #f6f8fa;
}
.detail-grid span,
.detail-grid strong,
.detail-grid code {
  display: block;
}
.detail-grid span {
  margin-bottom: 4px;
  color: #8590a0;
  font-size: 9px;
  font-weight: 750;
  text-transform: uppercase;
}
.detail-grid strong,
.detail-grid code {
  overflow-wrap: anywhere;
  font-size: 11px;
}
h3 {
  margin: 0 0 8px;
  font-size: 13px;
}
.message-box {
  padding: 12px;
  border-left: 3px solid #e15a67;
  color: #4c596c;
  background: #fff6f7;
  font-size: 12px;
  overflow-wrap: anywhere;
}
.trace-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.traceback {
  overflow: auto;
  max-height: 330px;
  margin: 0;
  padding: 14px;
  border-radius: 8px;
  color: #dce7f5;
  background: #172235;
  font-family: Consolas, monospace;
  font-size: 11px;
  line-height: 1.55;
  white-space: pre-wrap;
}
@media (max-width: 850px) {
  .metric-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .log-row {
    grid-template-columns: 42px minmax(0, 1fr);
  }
  .log-row > .q-btn {
    grid-column: 2;
    justify-self: start;
  }
}
@media (max-width: 600px) {
  .exceptions-page {
    padding: 20px 12px;
  }
  .page-header,
  .toolbar {
    align-items: stretch;
    flex-direction: column;
  }
  .metric-grid,
  .detail-grid {
    grid-template-columns: 1fr;
  }
  .search-input {
    width: 100%;
  }
  .log-row {
    padding: 14px;
  }
  .metadata span:nth-child(2) {
    display: none;
  }
}
</style>
