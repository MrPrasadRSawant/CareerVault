<template>
  <q-page class="admin-page">
    <div class="page-header">
      <div>
        <div class="page-kicker">{{ todayLabel }}</div>
        <h1>User administration</h1>
        <p>
          Review registrations, account access, and assigned roles. Career
          activity is not available in this workspace.
        </p>
      </div>
      <q-btn
        flat
        round
        icon="refresh"
        color="grey-7"
        :loading="loading"
        aria-label="Refresh user overview"
        @click="load"
      >
        <q-tooltip>Refresh overview</q-tooltip>
      </q-btn>
    </div>

    <template v-if="loading">
      <div class="stats-grid">
        <q-skeleton
          v-for="i in 4"
          :key="i"
          height="164px"
          class="skeleton-card"
        />
      </div>
      <q-skeleton height="280px" class="skeleton-card q-mt-md" />
      <q-skeleton height="330px" class="skeleton-card q-mt-md" />
    </template>

    <template v-else>
      <div class="stats-grid">
        <AdminStatCard
          icon="group"
          label="Total users"
          :value="overview.total_users"
          :hint="`${overview.active_users} accounts can sign in`"
          accent="#1769e0"
        />
        <AdminStatCard
          icon="person_add"
          label="New registrations"
          :value="overview.new_users_last_30_days"
          :hint="`${overview.new_users_last_7_days} joined in the last 7 days`"
          accent="#635bdf"
          badge="30 days"
        />
        <AdminStatCard
          icon="block"
          label="Blocked users"
          :value="overview.blocked_users"
          hint="Accounts without sign-in access"
          accent="#c94b55"
        />
        <AdminStatCard
          icon="how_to_reg"
          label="Registered today"
          :value="overview.registrations_today"
          hint="New accounts created today"
          accent="#249267"
        />
      </div>

      <section class="analytics-section">
        <div class="analytics-heading">
          <div>
            <h2>Registration analysis</h2>
            <p>New user registrations grouped by assigned role</p>
          </div>
          <span><q-icon name="group_work" /> Role comparison</span>
        </div>
        <div class="analytics-grid">
          <RegistrationRoleChart
            title="Daily registrations"
            subtitle="Last 7 days"
            period-kind="day"
            :points="overview.registrations_by_day"
          />
          <RegistrationRoleChart
            title="Monthly registrations"
            subtitle="Last 6 months"
            period-kind="month"
            :points="overview.registrations_by_month"
          />
          <RegistrationRoleChart
            title="Yearly registrations"
            subtitle="Last 5 years"
            period-kind="year"
            :points="overview.registrations_by_year"
          />
        </div>
      </section>

      <div class="overview-grid">
        <section class="panel-card recent-panel">
          <div class="panel-header">
            <div>
              <h2>Recent registrations</h2>
              <p>Newest user accounts created on CareerVault</p>
            </div>
            <router-link :to="{ name: 'system-admin-users' }">
              View all <q-icon name="arrow_forward" />
            </router-link>
          </div>
          <q-list v-if="overview.recent_users.length" class="recent-list">
            <q-item v-for="user in overview.recent_users" :key="user.id">
              <q-item-section avatar>
                <UserInitialsAvatar :name="user.full_name" />
              </q-item-section>
              <q-item-section>
                <q-item-label class="user-name">{{
                  user.full_name
                }}</q-item-label>
                <q-item-label caption>{{ user.email }}</q-item-label>
                <span class="role-label">{{ roleLabel(user.role) }}</span>
              </q-item-section>
              <q-item-section side>
                <span
                  class="status-chip"
                  :class="
                    user.is_active
                      ? 'status-chip--active'
                      : 'status-chip--blocked'
                  "
                >
                  {{ user.is_active ? "Active" : "Blocked" }}
                </span>
                <span class="joined-date">{{
                  formatLongDate(user.created_at)
                }}</span>
              </q-item-section>
            </q-item>
          </q-list>
          <div v-else class="empty-state">
            <q-icon name="group_add" />
            <span>No user accounts yet</span>
          </div>
        </section>

        <aside class="overview-side">
          <section class="panel-card account-health">
            <div class="panel-header">
              <div>
                <h2>Account access</h2>
                <p>Current sign-in status</p>
              </div>
            </div>
            <div
              class="health-ring"
              :style="{ '--active-share': `${activeShare * 3.6}deg` }"
            >
              <div>
                <strong>{{ activeShare }}</strong>
                <span>% active</span>
              </div>
            </div>
            <div class="health-legend">
              <span>
                <i class="active-dot"></i>Active
                <strong>{{ overview.active_users }}</strong>
              </span>
              <span>
                <i class="blocked-dot"></i>Blocked
                <strong>{{ overview.blocked_users }}</strong>
              </span>
            </div>
          </section>

          <section class="panel-card roles-card">
            <div class="panel-header">
              <div>
                <h2>Roles</h2>
                <p>Assigned account roles</p>
              </div>
            </div>
            <div
              v-for="roleCount in overview.role_counts"
              :key="roleCount.role"
              class="role-count"
            >
              <span class="role-icon">
                <q-icon
                  :name="
                    roleCount.role === 'system_admin'
                      ? 'admin_panel_settings'
                      : 'person'
                  "
                />
              </span>
              <div>
                <strong>{{ roleLabel(roleCount.role) }}</strong>
                <span>Single assigned role</span>
              </div>
              <b>{{ roleCount.count }}</b>
            </div>
          </section>
        </aside>
      </div>
    </template>
  </q-page>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";
import type { UserRole } from "@/api/auth";
import AdminStatCard from "./components/AdminStatCard.vue";
import RegistrationRoleChart from "./components/RegistrationRoleChart.vue";
import UserInitialsAvatar from "./components/UserInitialsAvatar.vue";
import { useAdminDashboard } from "./composables/useAdminDashboard";

defineOptions({ name: "AdminDashboardPage" });

const { overview, loading, load } = useAdminDashboard();
const todayLabel = new Intl.DateTimeFormat("en", {
  weekday: "long",
  month: "long",
  day: "numeric"
}).format(new Date());
const activeShare = computed(() =>
  overview.value.total_users
    ? Math.round(
        (overview.value.active_users / overview.value.total_users) * 100
      )
    : 0
);
const roleLabel = (role: UserRole) =>
  role === "system_admin" ? "System Admin" : "Job Applicant";
const formatLongDate = (value: string) =>
  new Intl.DateTimeFormat("en", {
    month: "short",
    day: "numeric",
    year: "numeric"
  }).format(new Date(value));
onMounted(load);
</script>

<style lang="scss" scoped>
.admin-page {
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
  color: #8b95a5;
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.55px;
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
  max-width: 720px;
  margin: 4px 0 0;
  color: #748094;
  font-size: 13px;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
}
.skeleton-card,
.panel-card {
  border-radius: 12px;
}
.panel-card {
  border: 1px solid #dfe4ea;
  background: #fff;
  box-shadow: 0 1px 2px rgba(30, 42, 56, 0.04);
}
.analytics-section {
  margin-top: 22px;
}
.analytics-heading {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 11px;
}
.analytics-heading h2 {
  margin: 0;
  color: #263449;
  font-size: 15px;
  font-weight: 770;
}
.analytics-heading p {
  margin: 3px 0 0;
  color: #8d98a8;
  font-size: 10.5px;
}
.analytics-heading > span {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: #66748a;
  font-size: 9.5px;
  font-weight: 650;
}
.analytics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 14px;
}
.panel-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 13px;
}
.panel-header h2 {
  margin: 0;
  color: #263449;
  font-size: 14px;
  font-weight: 750;
}
.panel-header p {
  margin: 3px 0 0;
  color: #929cab;
  font-size: 10.5px;
}
.panel-header a {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #1769e0;
  font-size: 11px;
  font-weight: 700;
  text-decoration: none;
}
.overview-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.65fr) minmax(270px, 0.75fr);
  align-items: start;
  gap: 14px;
  margin-top: 18px;
}
.overview-side {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.recent-panel,
.account-health,
.roles-card {
  padding: 18px;
}
.recent-list :deep(.q-item) {
  min-height: 68px;
  padding: 8px 4px;
  border-top: 1px solid #edf0f3;
}
.recent-list :deep(.q-item__section--avatar) {
  min-width: 48px;
}
.user-name {
  color: #354154;
  font-size: 12.5px;
  font-weight: 700;
}
.recent-list :deep(.q-item__label--caption) {
  margin-top: 2px;
  color: #8a95a5;
  font-size: 10.5px;
}
.role-label {
  display: inline-block;
  margin-top: 3px;
  color: #657389;
  font-size: 9.5px;
  font-weight: 650;
}
.status-chip {
  padding: 3px 7px;
  border-radius: 999px;
  font-size: 9.5px;
  font-weight: 700;
}
.status-chip--active {
  color: #287a56;
  background: #edf8f3;
}
.status-chip--blocked {
  color: #a33f48;
  background: #fff0f1;
}
.joined-date {
  margin-top: 5px;
  color: #9aa3b0;
  font-size: 9.5px;
}
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 230px;
  color: #99a3b1;
  font-size: 12px;
}
.empty-state .q-icon {
  font-size: 24px;
}
.health-ring {
  position: relative;
  display: grid;
  place-items: center;
  width: 132px;
  height: 132px;
  margin: 21px auto;
  border-radius: 50%;
  background: conic-gradient(#1769e0 var(--active-share), #e9edf2 0);
}
.health-ring::before {
  content: "";
  position: absolute;
  width: 102px;
  height: 102px;
  border-radius: 50%;
  background: #fff;
}
.health-ring > div {
  position: relative;
  z-index: 1;
  text-align: center;
}
.health-ring strong,
.health-ring span {
  display: block;
}
.health-ring strong {
  color: #172033;
  font-size: 25px;
  font-weight: 800;
  line-height: 1;
}
.health-ring span {
  margin-top: 4px;
  color: #8a95a5;
  font-size: 9.5px;
}
.health-legend {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}
.health-legend span {
  display: grid;
  grid-template-columns: 8px 1fr auto;
  align-items: center;
  gap: 6px;
  padding: 8px;
  border-radius: 8px;
  color: #687487;
  background: #f7f9fb;
  font-size: 10px;
}
.health-legend i {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}
.active-dot {
  background: #1769e0;
}
.blocked-dot {
  background: #d35d66;
}
.health-legend strong {
  color: #354154;
}
.role-count {
  display: grid;
  grid-template-columns: 38px 1fr auto;
  align-items: center;
  gap: 10px;
  padding: 11px 0;
  border-top: 1px solid #edf0f3;
}
.role-icon {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  border-radius: 9px;
  color: #635bdf;
  background: #f0edff;
  font-size: 18px;
}
.role-count strong,
.role-count span {
  display: block;
}
.role-count strong {
  color: #3d495c;
  font-size: 11px;
}
.role-count span {
  margin-top: 2px;
  color: #99a2b0;
  font-size: 9px;
}
.role-count b {
  color: #172033;
  font-size: 17px;
}

@media (max-width: 1100px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 760px) {
  .admin-page {
    padding: 20px 16px 34px;
  }
  .overview-grid {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 520px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .page-header {
    align-items: flex-start;
  }
  .analytics-heading {
    align-items: flex-start;
    flex-direction: column;
  }
  .analytics-grid {
    grid-template-columns: minmax(0, 1fr);
  }
  .recent-list :deep(.q-item__section--side) {
    display: none;
  }
}
</style>
