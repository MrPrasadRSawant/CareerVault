<template>
  <q-page class="security-page">
    <div class="page-header">
      <div>
        <div class="page-kicker">Incident readiness</div>
        <h1>Login activity</h1>
        <p>
          Review authentication outcomes and session metadata without accessing
          users' career information.
        </p>
      </div>
      <q-btn
        flat
        round
        icon="refresh"
        color="grey-7"
        :loading="loading"
        aria-label="Refresh login activity"
        @click="load"
      >
        <q-tooltip>Refresh activity</q-tooltip>
      </q-btn>
    </div>

    <div class="stats-grid">
      <AdminStatCard
        icon="login"
        label="Successful logins"
        :value="overview.successful_logins_last_24_hours"
        hint="During the last 24 hours"
        accent="#249267"
      />
      <AdminStatCard
        icon="gpp_bad"
        label="Failed logins"
        :value="overview.failed_logins_last_24_hours"
        hint="During the last 24 hours"
        accent="#c94b55"
      />
      <AdminStatCard
        icon="devices"
        label="Active sessions"
        :value="overview.active_sessions"
        hint="Valid sessions not signed out"
        accent="#1769e0"
      />
      <AdminStatCard
        icon="history"
        label="Retention period"
        :value="overview.retention_days"
        hint="Days before automatic removal"
        accent="#635bdf"
      />
    </div>

    <div class="privacy-banner">
      <q-icon name="privacy_tip" />
      <div>
        <strong>Security metadata only</strong>
        <span>
          IP addresses and user-agent strings are restricted to incident review.
          Passwords, access tokens, request content, and career data are never
          recorded here.
        </span>
      </div>
    </div>

    <section class="activity-card">
      <q-tabs
        v-model="tab"
        dense
        no-caps
        align="left"
        active-color="primary"
        indicator-color="primary"
        class="activity-tabs"
      >
        <q-tab name="events" icon="fact_check" label="Login events" />
        <q-tab name="sessions" icon="schedule" label="Sessions" />
      </q-tabs>

      <div class="filters">
        <q-input
          v-model="search"
          dense
          outlined
          clearable
          debounce="300"
          placeholder="Search account name or email"
          class="search-field"
        >
          <template #prepend><q-icon name="search" /></template>
        </q-input>
        <q-select
          v-model="roleFilter"
          dense
          outlined
          clearable
          emit-value
          map-options
          label="Role"
          :options="roleOptions"
          class="filter-field"
        />
        <q-select
          v-if="tab === 'events'"
          v-model="outcomeFilter"
          dense
          outlined
          clearable
          emit-value
          map-options
          label="Outcome"
          :options="outcomeOptions"
          class="filter-field"
        />
        <q-btn
          v-if="search || roleFilter !== null || outcomeFilter !== null"
          flat
          no-caps
          icon="restart_alt"
          label="Clear"
          @click="clearFilters"
        />
        <span class="result-count"
          >{{ total }} {{ tab === "events" ? "events" : "sessions" }}</span
        >
      </div>

      <q-table
        v-if="tab === 'events'"
        flat
        :rows="events"
        :columns="eventColumns"
        row-key="id"
        :loading="loading"
        hide-pagination
        no-data-label="No authentication events match these filters"
      >
        <template #body-cell-account="props">
          <q-td :props="props">
            <div v-if="props.row.account_known" class="account-cell">
              <UserInitialsAvatar
                :name="props.row.user_name || 'Known User'"
                size="36px"
                font-size="10px"
              />
              <div>
                <strong>{{ props.row.user_name }}</strong>
                <span>{{ props.row.user_email }}</span>
                <small>{{ roleLabel(props.row.role) }}</small>
              </div>
            </div>
            <div v-else class="account-cell">
              <q-avatar size="36px" class="unknown-avatar">
                <q-icon name="person_search" />
              </q-avatar>
              <div>
                <strong>Unknown account</strong>
                <span>Reference {{ props.row.unknown_account_reference }}</span>
                <small>No email stored</small>
              </div>
            </div>
          </q-td>
        </template>
        <template #body-cell-outcome="props">
          <q-td :props="props">
            <span
              class="status-chip"
              :class="
                props.row.outcome === 'success'
                  ? 'status-chip--success'
                  : 'status-chip--failure'
              "
            >
              <i></i>{{ outcomeLabel(props.row.outcome) }}
            </span>
          </q-td>
        </template>
        <template #body-cell-event_type="props">
          <q-td :props="props">{{ eventLabel(props.row.event_type) }}</q-td>
        </template>
        <template #body-cell-occurred_at="props">
          <q-td :props="props">
            <div class="date-cell">
              <strong>{{ formatDate(props.row.occurred_at) }}</strong>
              <span>{{ formatTime(props.row.occurred_at) }}</span>
            </div>
          </q-td>
        </template>
        <template #body-cell-client="props">
          <q-td :props="props">
            <div class="client-cell">
              <strong>{{ clientSummary(props.row.user_agent) }}</strong>
              <span>{{ props.row.ip_address || "IP unavailable" }}</span>
              <q-tooltip v-if="props.row.user_agent" max-width="420px">{{
                props.row.user_agent
              }}</q-tooltip>
            </div>
          </q-td>
        </template>
        <template #body-cell-reason="props">
          <q-td :props="props">
            <span class="reason-text">{{
              failureReasonLabel(props.row.failure_reason)
            }}</span>
          </q-td>
        </template>
      </q-table>

      <q-table
        v-else
        flat
        :rows="sessions"
        :columns="sessionColumns"
        row-key="started_at"
        :loading="loading"
        hide-pagination
        no-data-label="No sessions match these filters"
      >
        <template #body-cell-account="props">
          <q-td :props="props">
            <div class="account-cell">
              <UserInitialsAvatar
                :name="props.row.user_name"
                size="36px"
                font-size="10px"
              />
              <div>
                <strong>{{ props.row.user_name }}</strong>
                <span>{{ props.row.user_email }}</span>
                <small>{{ roleLabel(props.row.role) }}</small>
              </div>
            </div>
          </q-td>
        </template>
        <template #body-cell-status="props">
          <q-td :props="props">
            <span
              class="status-chip"
              :class="`status-chip--${props.row.status}`"
            >
              <i></i>{{ sessionStatusLabel(props.row.status) }}
            </span>
          </q-td>
        </template>
        <template #body-cell-started_at="props">
          <q-td :props="props">
            <div class="date-cell">
              <strong>{{ formatDate(props.row.started_at) }}</strong>
              <span>{{ formatTime(props.row.started_at) }}</span>
            </div>
          </q-td>
        </template>
        <template #body-cell-duration="props">
          <q-td :props="props">
            <div class="duration-cell">
              <strong>{{ formatDuration(props.row.duration_seconds) }}</strong>
              <span>{{ durationBasisLabel(props.row.duration_basis) }}</span>
            </div>
          </q-td>
        </template>
        <template #body-cell-last_seen_at="props">
          <q-td :props="props">{{
            formatDateTime(props.row.last_seen_at)
          }}</q-td>
        </template>
        <template #body-cell-client="props">
          <q-td :props="props">
            <div class="client-cell">
              <strong>{{ clientSummary(props.row.user_agent) }}</strong>
              <span>{{ props.row.ip_address || "IP unavailable" }}</span>
              <q-tooltip v-if="props.row.user_agent" max-width="420px">{{
                props.row.user_agent
              }}</q-tooltip>
            </div>
          </q-td>
        </template>
      </q-table>

      <div v-if="!loading && total > 0" class="table-footer">
        <span>Showing {{ firstRecord }}–{{ lastRecord }} of {{ total }}</span>
        <q-pagination
          v-model="page"
          :max="pageCount"
          :max-pages="6"
          boundary-numbers
          direction-links
          color="primary"
        />
      </div>
    </section>
  </q-page>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";
import type { QTableProps } from "quasar";
import type {
  AuthFailureReason,
  AuthOutcome,
  AuthSessionStatus
} from "@/api/admin";
import type { UserRole } from "@/api/auth";
import AdminStatCard from "./components/AdminStatCard.vue";
import UserInitialsAvatar from "./components/UserInitialsAvatar.vue";
import { useAdminSecurity } from "./composables/useAdminSecurity";

defineOptions({ name: "AdminSecurityPage" });

const roleOptions = [
  { label: "Job Applicant", value: "job_applicant" },
  { label: "System Admin", value: "system_admin" }
];
const outcomeOptions = [
  { label: "Success", value: "success" },
  { label: "Failure", value: "failure" }
];
const eventColumns: QTableProps["columns"] = [
  { name: "account", label: "Account", field: "user_name", align: "left" },
  { name: "outcome", label: "Outcome", field: "outcome", align: "left" },
  {
    name: "event_type",
    label: "Event",
    field: "event_type",
    align: "left"
  },
  {
    name: "occurred_at",
    label: "Occurred",
    field: "occurred_at",
    align: "left",
    sortable: true
  },
  {
    name: "client",
    label: "Client and IP",
    field: "ip_address",
    align: "left"
  },
  { name: "reason", label: "Reason", field: "failure_reason", align: "left" }
];
const sessionColumns: QTableProps["columns"] = [
  { name: "account", label: "Account", field: "user_name", align: "left" },
  { name: "status", label: "Status", field: "status", align: "left" },
  {
    name: "started_at",
    label: "Started",
    field: "started_at",
    align: "left",
    sortable: true
  },
  {
    name: "duration",
    label: "Session time",
    field: "duration_seconds",
    align: "left"
  },
  {
    name: "last_seen_at",
    label: "Last activity",
    field: "last_seen_at",
    align: "left"
  },
  { name: "client", label: "Client and IP", field: "ip_address", align: "left" }
];
const {
  overview,
  events,
  sessions,
  total,
  loading,
  tab,
  search,
  roleFilter,
  outcomeFilter,
  page,
  pageCount,
  load,
  clearFilters
} = useAdminSecurity();
const firstRecord = computed(() =>
  total.value === 0 ? 0 : (page.value - 1) * 20 + 1
);
const lastRecord = computed(() => Math.min(page.value * 20, total.value));

const roleLabel = (role: UserRole | null) =>
  role === "system_admin"
    ? "System Admin"
    : role === "job_applicant"
      ? "Job Applicant"
      : "Role unavailable";
const outcomeLabel = (outcome: AuthOutcome) =>
  outcome === "success" ? "Success" : "Failure";
const eventLabel = (event: string) =>
  event === "registration" ? "Registration sign-in" : "Login";
const failureReasonLabel = (reason: AuthFailureReason | null) => {
  if (reason === "account_blocked") return "Blocked account";
  if (reason === "temporarily_locked") return "Temporary security lock";
  if (reason === "role_not_allowed") return "Role not allowed";
  if (reason === "invalid_credentials") return "Invalid credentials";
  return "—";
};
const sessionStatusLabel = (status: AuthSessionStatus) => {
  if (status === "active") return "Active";
  if (status === "expired") return "Expired";
  return "Signed out";
};
const durationBasisLabel = (basis: string) => {
  if (basis === "ongoing") return "Ongoing";
  if (basis === "estimated_last_activity") return "Estimated from activity";
  return "Exact at sign-out";
};
const formatDate = (value: string) =>
  new Intl.DateTimeFormat("en", {
    month: "short",
    day: "numeric",
    year: "numeric"
  }).format(new Date(value));
const formatTime = (value: string) =>
  new Intl.DateTimeFormat("en", {
    hour: "numeric",
    minute: "2-digit",
    second: "2-digit"
  }).format(new Date(value));
const formatDateTime = (value: string) =>
  `${formatDate(value)}, ${formatTime(value)}`;
const formatDuration = (seconds: number) => {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = seconds % 60;
  if (hours > 0) return `${hours}h ${minutes}m`;
  if (minutes > 0) return `${minutes}m ${remainingSeconds}s`;
  return `${remainingSeconds}s`;
};
const clientSummary = (userAgent: string | null) => {
  if (!userAgent) return "Unknown client";
  const browser = /Edg\//.test(userAgent)
    ? "Edge"
    : /Firefox\//.test(userAgent)
      ? "Firefox"
      : /Chrome\//.test(userAgent)
        ? "Chrome"
        : /Safari\//.test(userAgent)
          ? "Safari"
          : "Other browser";
  const platform = /Windows/.test(userAgent)
    ? "Windows"
    : /Android/.test(userAgent)
      ? "Android"
      : /iPhone|iPad/.test(userAgent)
        ? "iOS"
        : /Mac OS/.test(userAgent)
          ? "macOS"
          : /Linux/.test(userAgent)
            ? "Linux"
            : "Unknown OS";
  return `${browser} · ${platform}`;
};

onMounted(load);
</script>

<style lang="scss" scoped>
.security-page {
  max-width: 1360px;
  margin: 0 auto;
  padding: 26px 28px 42px;
}
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 21px;
}
.page-kicker {
  margin-bottom: 4px;
  color: #1769e0;
  font-size: 10.5px;
  font-weight: 750;
  letter-spacing: 0.6px;
  text-transform: uppercase;
}
.page-header h1 {
  margin: 0;
  color: #172033;
  font-size: 25px;
  font-weight: 780;
  letter-spacing: -0.45px;
}
.page-header p {
  margin: 4px 0 0;
  color: #748094;
  font-size: 13px;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}
.privacy-banner {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin: 16px 0;
  padding: 12px 14px;
  border: 1px solid #dce6f3;
  border-radius: 11px;
  color: #617087;
  background: #f6f9fd;
}
.privacy-banner .q-icon {
  flex: 0 0 auto;
  color: #1769e0;
  font-size: 20px;
}
.privacy-banner strong,
.privacy-banner span {
  display: block;
}
.privacy-banner strong {
  color: #3d4b60;
  font-size: 11px;
}
.privacy-banner span {
  margin-top: 2px;
  font-size: 10px;
  line-height: 1.45;
}
.activity-card {
  overflow: hidden;
  border: 1px solid #dfe4ea;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 1px 2px rgba(30, 42, 56, 0.04);
}
.activity-tabs {
  padding: 7px 12px 0;
  border-bottom: 1px solid #e7ebef;
}
.filters {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  border-bottom: 1px solid #edf0f3;
}
.search-field {
  flex: 1;
  max-width: 400px;
}
.filter-field {
  width: 170px;
}
.result-count {
  margin-left: auto;
  color: #8a95a5;
  font-size: 11px;
}
.account-cell {
  display: flex;
  align-items: center;
  gap: 9px;
  min-width: 220px;
}
.account-cell strong,
.account-cell span,
.account-cell small {
  display: block;
}
.account-cell strong {
  color: #354154;
  font-size: 11.5px;
}
.account-cell span {
  margin-top: 1px;
  color: #8591a2;
  font-size: 9.5px;
}
.account-cell small {
  margin-top: 2px;
  color: #1769e0;
  font-size: 8.5px;
  font-weight: 650;
}
.unknown-avatar {
  color: #7b8798;
  background: #edf0f4;
}
.status-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 8px;
  border-radius: 999px;
  font-size: 9px;
  font-weight: 700;
}
.status-chip i {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}
.status-chip--success,
.status-chip--active {
  color: #287a56;
  background: #edf8f3;
}
.status-chip--failure {
  color: #b13d47;
  background: #fff0f1;
}
.status-chip--ended {
  color: #56677d;
  background: #edf1f5;
}
.status-chip--expired {
  color: #966122;
  background: #fff4e5;
}
.date-cell strong,
.date-cell span,
.client-cell strong,
.client-cell span,
.duration-cell strong,
.duration-cell span {
  display: block;
}
.date-cell strong,
.client-cell strong,
.duration-cell strong {
  color: #49566a;
  font-size: 10.5px;
}
.date-cell span,
.client-cell span,
.duration-cell span {
  margin-top: 2px;
  color: #929cab;
  font-size: 9px;
}
.client-cell {
  max-width: 170px;
  cursor: help;
}
.reason-text {
  color: #657287;
  font-size: 10px;
}
.table-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 13px 15px;
  border-top: 1px solid #edf0f3;
  color: #8a95a5;
  font-size: 10.5px;
}

@media (max-width: 1100px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .filters {
    flex-wrap: wrap;
  }
  .result-count {
    width: 100%;
    margin-left: 0;
  }
}
@media (max-width: 760px) {
  .security-page {
    padding: 20px 16px 34px;
  }
  .filters {
    align-items: stretch;
    flex-direction: column;
  }
  .search-field,
  .filter-field {
    width: 100%;
    max-width: none;
  }
  .table-footer {
    align-items: flex-start;
    flex-direction: column;
  }
}
@media (max-width: 520px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .page-header {
    align-items: flex-start;
  }
}
</style>
