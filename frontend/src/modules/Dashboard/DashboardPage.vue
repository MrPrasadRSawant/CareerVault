<template>
  <q-page class="dashboard-page">
    <div class="dashboard-grid">
      <aside
        class="dashboard-rail dashboard-rail--left"
        aria-label="Career profile"
      >
        <div class="rail-card profile-card">
          <div class="profile-cover">
            <span class="profile-cover-shape profile-cover-shape--one"></span>
            <span class="profile-cover-shape profile-cover-shape--two"></span>
          </div>
          <div class="profile-body">
            <div class="profile-avatar-wrap">
              <q-avatar size="64px" class="profile-initials">
                {{ profileInitials }}
              </q-avatar>
            </div>
            <div class="profile-name">{{ auth.user?.full_name }}</div>
            <div class="profile-role">Your private career workspace</div>
            <div class="profile-location"
              ><q-icon name="lock" size="13px" /> Only visible to you</div
            >
          </div>
          <q-separator />
          <router-link :to="{ name: 'resumes' }" class="profile-link">
            <span>Resume library</span><strong>View</strong>
          </router-link>
          <router-link :to="{ name: 'cover-letters' }" class="profile-link">
            <span>Cover letters</span><strong>Manage</strong>
          </router-link>
        </div>

        <div class="rail-card search-status-card">
          <div class="rail-card-title">Job search status</div>
          <div class="status-line"
            ><span class="status-pulse"></span
            ><span>Actively tracking</span></div
          >
          <div class="mini-metrics">
            <div
              ><strong>{{ activeOpportunities }}</strong
              ><span>Active roles</span></div
            >
            <div
              ><strong>{{ activePipelineCount }}</strong
              ><span>In pipeline</span></div
            >
          </div>
          <q-btn
            outline
            no-caps
            color="primary"
            label="View applications"
            class="full-width"
            :to="{ name: 'applications' }"
          />
        </div>
      </aside>

      <main class="dashboard-main">
        <div class="page-header">
          <div>
            <div class="page-kicker">{{ todayLabel }}</div>
            <div class="page-title">{{ greeting }}, {{ firstName }}</div>
            <div class="page-subtitle">
              Here is what is happening in your job search.
            </div>
          </div>
          <div class="page-actions">
            <q-btn
              flat
              round
              dense
              icon="refresh"
              color="grey-7"
              aria-label="Refresh dashboard"
              :loading="loading"
              @click="load"
            >
              <q-tooltip>Refresh dashboard</q-tooltip>
            </q-btn>
            <q-btn
              unelevated
              no-caps
              color="primary"
              icon="add"
              label="Add opportunity"
              :to="{ name: 'opportunities' }"
              class="primary-action"
            />
          </div>
        </div>

        <q-banner v-if="error" rounded class="q-mb-md" color="negative">
          <template #avatar>
            <q-icon name="error_outline" />
          </template>
          {{ error }}
          <template #action>
            <q-btn
              flat
              dense
              label="Try again"
              text-color="white"
              @click="load"
            />
          </template>
        </q-banner>

        <template v-if="loading">
          <div class="row q-col-gutter-md">
            <div
              v-for="i in 4"
              :key="'kpi' + i"
              class="col-12 col-sm-6 col-md-3"
            >
              <q-skeleton height="128px" class="skeleton-card" />
            </div>
          </div>
          <div class="row q-col-gutter-md q-mt-md">
            <div class="col-12 col-md-6">
              <q-skeleton height="320px" class="skeleton-card" />
            </div>
            <div class="col-12 col-md-6">
              <q-skeleton height="320px" class="skeleton-card" />
            </div>
          </div>
        </template>

        <template v-else>
          <div class="report-tabs-card">
            <q-tabs
              v-model="activeReport"
              dense
              no-caps
              align="left"
              active-color="primary"
              indicator-color="primary"
            >
              <q-tab
                name="opportunities"
                icon="work_outline"
                label="Opportunities"
              />
              <q-tab
                name="applications"
                icon="assignment"
                label="Applications"
              />
            </q-tabs>
          </div>

          <div v-if="activeReport === 'opportunities'" class="report-filters">
            <q-select
              v-model="opportunityFilters.statuses"
              outlined
              dense
              multiple
              use-chips
              emit-value
              map-options
              options-dense
              label="Statuses"
              :options="opportunityStatusOptions"
              class="filter-control status-control"
            />
            <q-select
              v-model="opportunityFilters.company"
              outlined
              dense
              clearable
              label="Company"
              :options="opportunityCompanyOptions"
              class="filter-control"
            />
            <ProfessionalDateRangeField
              :from="opportunityFilters.dateFrom"
              :to="opportunityFilters.dateTo"
              label="Created date range"
              class="filter-control date-control"
              @update:from="opportunityFilters.dateFrom = $event"
              @update:to="opportunityFilters.dateTo = $event"
            />
            <q-btn
              flat
              no-caps
              icon="restart_alt"
              label="Clear filters"
              @click="clearOpportunityFilters"
            />
            <div class="report-result-count">
              {{ totalOpportunities }}
              {{ totalOpportunities === 1 ? "record" : "records" }}
            </div>
          </div>

          <div v-else class="report-filters">
            <q-select
              v-model="applicationFilters.statuses"
              outlined
              dense
              multiple
              use-chips
              emit-value
              map-options
              options-dense
              label="Statuses"
              :options="applicationStatusOptions"
              class="filter-control status-control"
            />
            <ProfessionalDateRangeField
              :from="applicationFilters.dateFrom"
              :to="applicationFilters.dateTo"
              label="Applied date range"
              class="filter-control date-control"
              @update:from="applicationFilters.dateFrom = $event"
              @update:to="applicationFilters.dateTo = $event"
            />
            <q-btn
              flat
              no-caps
              icon="restart_alt"
              label="Clear filters"
              @click="clearApplicationFilters"
            />
            <div class="report-result-count">
              {{ totalApplications }}
              {{ totalApplications === 1 ? "record" : "records" }}
            </div>
          </div>

          <div
            v-if="activeReport === 'applications'"
            class="row q-col-gutter-md"
          >
            <div class="col-12 col-sm-6 col-md-3">
              <StatCard
                icon="assignment"
                label="Applications"
                :value="totalApplications"
                :hint="`${waitingForResponseCount} awaiting response`"
                accent="#1769E0"
                :to="{ name: 'applications' }"
              />
            </div>
            <div class="col-12 col-sm-6 col-md-3">
              <StatCard
                icon="route"
                label="Active pipeline"
                :value="activePipelineCount"
                :hint="`${interviewStageCount} at interview stage`"
                accent="#635BDF"
                :to="{ name: 'applications' }"
              />
            </div>
            <div class="col-12 col-sm-6 col-md-3">
              <StatCard
                icon="mark_email_read"
                label="Response rate"
                :value="responseRate"
                value-suffix="%"
                :hint="`${respondedApplications} responses received`"
                accent="#E8A11A"
                :to="{ name: 'applications' }"
              />
            </div>
            <div class="col-12 col-sm-6 col-md-3">
              <StatCard
                icon="event_available"
                label="Interview conversion"
                :value="interviewConversionRate"
                value-suffix="%"
                :hint="`${offersCount} offers so far`"
                accent="#2F855A"
                :to="{ name: 'applications' }"
              />
            </div>
          </div>

          <template v-if="activeReport === 'opportunities'">
            <div class="row q-col-gutter-md opportunity-kpi-row">
              <div class="col-12 col-sm-6 col-lg-3">
                <StatCard
                  icon="work_outline"
                  label="Total opportunities"
                  :value="totalOpportunities"
                  hint="Matching the current filters"
                  accent="#1769E0"
                  :to="{ name: 'opportunities' }"
                />
              </div>
              <div class="col-12 col-sm-6 col-lg-3">
                <StatCard
                  icon="track_changes"
                  label="Active opportunities"
                  :value="activeOpportunities"
                  :hint="`${totalOpportunities - activeOpportunities} closed or archived`"
                  accent="#635BDF"
                  :to="{ name: 'opportunities' }"
                />
              </div>
              <div class="col-12 col-sm-6 col-lg-3">
                <StatCard
                  icon="add_chart"
                  label="Added in 30 days"
                  :value="opportunitiesAddedLast30Days"
                  hint="Newly captured opportunities"
                  accent="#E8A11A"
                  :to="{ name: 'opportunities' }"
                />
              </div>
              <div class="col-12 col-sm-6 col-lg-3">
                <StatCard
                  icon="trending_up"
                  label="Application conversion"
                  :value="opportunityConversionRate"
                  value-suffix="%"
                  :hint="`${opportunityApplicationCount} converted opportunities`"
                  accent="#2F855A"
                  :to="{ name: 'applications' }"
                />
              </div>
            </div>

            <div class="section-heading q-mt-lg">
              <div>
                <div class="section-title">Opportunities</div>
                <div class="section-subtitle">
                  Pipeline distribution and your most recently added roles
                </div>
              </div>
              <router-link class="panel-link" :to="{ name: 'opportunities' }">
                View all opportunities
              </router-link>
            </div>

            <div class="row q-col-gutter-md opportunity-section">
              <div class="col-12 opportunity-chart-column">
                <div class="panel-card">
                  <div class="panel-header">
                    <div>
                      <div class="panel-title">Opportunities by status</div>
                      <div class="panel-subtitle">
                        {{ totalOpportunities }}
                        {{
                          totalOpportunities === 1
                            ? "opportunity"
                            : "opportunities"
                        }}
                        across your pipeline
                      </div>
                    </div>
                    <router-link
                      class="panel-link"
                      :to="{ name: 'opportunities' }"
                    >
                      View all
                    </router-link>
                  </div>
                  <StatusDonut
                    :data="opportunityByStatus"
                    :total="totalOpportunities"
                  />
                </div>
              </div>
              <div class="col-12 opportunity-list-column">
                <div class="panel-card">
                  <div class="panel-header">
                    <div class="panel-title">Recently added opportunities</div>
                    <router-link
                      class="panel-link"
                      :to="{ name: 'opportunities' }"
                    >
                      View all
                    </router-link>
                  </div>
                  <RecentOpportunities :items="recentOpportunities" />
                </div>
              </div>
            </div>
          </template>

          <template v-if="activeReport === 'applications'">
            <div class="section-heading q-mt-lg">
              <div>
                <div class="section-title">Application performance</div>
                <div class="section-subtitle"
                  >Conversion, momentum, interviews, and follow-up
                  execution</div
                >
              </div>
            </div>

            <div class="row q-col-gutter-md">
              <div class="col-12 col-md-7">
                <div class="panel-card">
                  <div class="panel-header">
                    <div>
                      <div class="panel-title">Application funnel</div>
                      <div class="panel-subtitle">
                        Where applications are progressing or dropping off
                      </div>
                    </div>
                  </div>
                  <ApplicationFunnel :stages="applicationFunnel" />
                </div>
              </div>
              <div class="col-12 col-md-5">
                <div class="panel-card">
                  <div class="panel-header">
                    <div>
                      <div class="panel-title">Current pipeline</div>
                      <div class="panel-subtitle">
                        {{ waitingForResponseCount }} waiting for a response
                      </div>
                    </div>
                  </div>
                  <StatusBars :data="applicationByStatus" />
                </div>
              </div>
            </div>

            <div class="row q-col-gutter-md q-mt-md">
              <div class="col-12 col-md-6">
                <div class="panel-card">
                  <div class="panel-header">
                    <div class="panel-title">Application activity</div>
                    <div class="panel-note">Last 8 weeks</div>
                  </div>
                  <TrendChart :points="applicationsPerWeek" />
                </div>
              </div>
              <div class="col-12 col-md-6">
                <div class="panel-card">
                  <div class="panel-header">
                    <div class="panel-title">Upcoming interviews</div>
                  </div>
                  <UpcomingInterviews :items="upcomingInterviews" />
                </div>
              </div>
            </div>

            <div class="row q-col-gutter-md q-mt-md">
              <div class="col-12">
                <div class="panel-card">
                  <div class="panel-header">
                    <div class="panel-title">Pending follow-ups</div>
                    <div class="panel-note"
                      >{{ overdueFollowUpCount }} overdue</div
                    >
                  </div>
                  <FollowUpsCard :items="pendingFollowUps" />
                </div>
              </div>
            </div>
          </template>
        </template>
      </main>

      <aside
        class="dashboard-rail dashboard-rail--right"
        aria-label="Job search shortcuts"
      >
        <div class="rail-card quick-actions-card">
          <div class="rail-card-heading">
            <div>
              <div class="rail-card-title">Quick actions</div>
              <div class="rail-card-subtitle">Keep your search moving</div>
            </div>
            <q-icon name="bolt" size="20px" />
          </div>
          <q-list class="quick-action-list">
            <q-item clickable v-ripple :to="{ name: 'opportunities' }">
              <q-item-section avatar
                ><span class="quick-icon quick-icon--blue"
                  ><q-icon name="add_business" /></span
              ></q-item-section>
              <q-item-section
                ><q-item-label>Add an opportunity</q-item-label
                ><q-item-label caption
                  >Save a role you found</q-item-label
                ></q-item-section
              >
              <q-item-section side
                ><q-icon name="chevron_right"
              /></q-item-section>
            </q-item>
            <q-item clickable v-ripple :to="{ name: 'resumes' }">
              <q-item-section avatar
                ><span class="quick-icon quick-icon--violet"
                  ><q-icon name="upload_file" /></span
              ></q-item-section>
              <q-item-section
                ><q-item-label>Upload a resume</q-item-label
                ><q-item-label caption
                  >Keep versions organized</q-item-label
                ></q-item-section
              >
              <q-item-section side
                ><q-icon name="chevron_right"
              /></q-item-section>
            </q-item>
            <q-item clickable v-ripple :to="{ name: 'email-follow-ups' }">
              <q-item-section avatar
                ><span class="quick-icon quick-icon--amber"
                  ><q-icon name="schedule_send" /></span
              ></q-item-section>
              <q-item-section
                ><q-item-label>Plan a follow-up</q-item-label
                ><q-item-label caption
                  >Reconnect at the right time</q-item-label
                ></q-item-section
              >
              <q-item-section side
                ><q-icon name="chevron_right"
              /></q-item-section>
            </q-item>
          </q-list>
        </div>

        <div class="rail-card progress-card">
          <div class="rail-card-title">Application progress</div>
          <div class="progress-number">{{ responseRate }}<span>%</span></div>
          <div class="progress-label">Response rate</div>
          <q-linear-progress
            rounded
            size="7px"
            :value="responseRate / 100"
            color="primary"
            track-color="blue-grey-1"
            class="q-mt-md"
          />
          <div class="progress-row"
            ><span>Awaiting response</span
            ><strong>{{ waitingForResponseCount }}</strong></div
          >
          <div class="progress-row"
            ><span>Interview stage</span
            ><strong>{{ interviewStageCount }}</strong></div
          >
          <div class="progress-row"
            ><span>Offers</span><strong>{{ offersCount }}</strong></div
          >
        </div>

        <div class="rail-card momentum-card">
          <div class="momentum-icon"
            ><q-icon name="insights" size="22px"
          /></div>
          <div class="rail-card-title">Build your momentum</div>
          <p
            >Track every application and follow up consistently to spot what is
            working.</p
          >
          <router-link :to="{ name: 'applications' }"
            >Review your pipeline <q-icon name="arrow_forward"
          /></router-link>
        </div>
      </aside>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import ProfessionalDateRangeField from "@/components/ProfessionalDateRangeField.vue";
import {
  APPLICATION_STATUS_LABELS,
  APPLICATION_STATUS_ORDER,
  OPPORTUNITY_STATUS_LABELS,
  OPPORTUNITY_STATUS_ORDER
} from "@/modules/shared/statusColors";
import { useDashboard } from "./composables/useDashboard";
import StatCard from "./components/StatCard.vue";
import StatusDonut from "./components/StatusDonut.vue";
import StatusBars from "./components/StatusBars.vue";
import ApplicationFunnel from "./components/ApplicationFunnel.vue";
import TrendChart from "./components/TrendChart.vue";
import UpcomingInterviews from "./components/UpcomingInterviews.vue";
import RecentOpportunities from "./components/RecentOpportunities.vue";
import FollowUpsCard from "./components/FollowUpsCard.vue";

const auth = useAuthStore();
const activeReport = ref<"opportunities" | "applications">("opportunities");
const firstName = computed(
  () => auth.user?.full_name?.trim().split(/\s+/)[0] || "there"
);
const profileInitials = computed(
  () =>
    auth.user?.full_name
      ?.split(/\s+/)
      .filter(Boolean)
      .slice(0, 2)
      .map(part => part[0])
      .join("")
      .toUpperCase() || "CV"
);
const greeting = computed(() => {
  const hour = new Date().getHours();
  if (hour < 12) return "Good morning";
  if (hour < 18) return "Good afternoon";
  return "Good evening";
});
const todayLabel = new Intl.DateTimeFormat("en", {
  weekday: "long",
  month: "long",
  day: "numeric"
}).format(new Date());

const opportunityStatusOptions = OPPORTUNITY_STATUS_ORDER.map(value => ({
  label: OPPORTUNITY_STATUS_LABELS[value],
  value
}));
const applicationStatusOptions = APPLICATION_STATUS_ORDER.map(value => ({
  label: APPLICATION_STATUS_LABELS[value],
  value
}));

const {
  loading,
  error,
  load,
  opportunityFilters,
  applicationFilters,
  opportunityCompanyOptions,
  clearOpportunityFilters,
  clearApplicationFilters,
  totalOpportunities,
  activeOpportunities,
  opportunitiesAddedLast30Days,
  opportunityApplicationCount,
  opportunityConversionRate,
  totalApplications,
  offersCount,
  respondedApplications,
  activePipelineCount,
  waitingForResponseCount,
  interviewStageCount,
  responseRate,
  interviewConversionRate,
  opportunityByStatus,
  applicationByStatus,
  applicationFunnel,
  applicationsPerWeek,
  recentOpportunities,
  upcomingInterviews,
  pendingFollowUps,
  overdueFollowUpCount
} = useDashboard();

onMounted(load);
</script>

<style lang="scss" scoped>
.dashboard-page {
  padding: 20px 18px 40px;
  max-width: 1450px;
  margin: 0 auto;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 220px minmax(0, 1fr) 270px;
  align-items: start;
  gap: 18px;
}

.dashboard-main {
  min-width: 0;
}

.dashboard-rail {
  position: sticky;
  top: 86px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.rail-card {
  overflow: hidden;
  border: 1px solid #dfe4ea;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 1px 2px rgba(30, 42, 56, 0.04);
}

.profile-cover {
  position: relative;
  height: 66px;
  overflow: hidden;
  background: linear-gradient(135deg, #163d7a 0%, #1769e0 62%, #4b8df0 100%);
}

.profile-cover-shape {
  position: absolute;
  border: 1px solid rgba(255, 255, 255, 0.22);
  border-radius: 50%;
}
.profile-cover-shape--one {
  width: 110px;
  height: 110px;
  top: -60px;
  right: -18px;
}
.profile-cover-shape--two {
  width: 70px;
  height: 70px;
  top: 18px;
  right: 40px;
}

.profile-body {
  position: relative;
  padding: 0 16px 16px;
  text-align: center;
}
.profile-avatar-wrap {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 64px;
  margin-top: -32px;
  margin-bottom: 9px;
}
.profile-initials {
  display: inline-flex !important;
  align-items: center;
  justify-content: center;
  border: 3px solid #fff;
  color: #fff;
  background: linear-gradient(135deg, #1769e0, #625ad8);
  box-shadow: 0 3px 12px rgba(36, 63, 100, 0.2);
  font-size: 18px;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -0.25px;
}
.profile-name {
  color: #172033;
  font-size: 16px;
  font-weight: 750;
}
.profile-role {
  margin-top: 3px;
  color: #657184;
  font-size: 12px;
  line-height: 1.4;
}
.profile-location {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  margin-top: 8px;
  color: #98a2b1;
  font-size: 10.5px;
}
.profile-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 11px 14px;
  border-bottom: 1px solid #edf0f3;
  color: #4f5b6c;
  font-size: 12px;
  text-decoration: none;
}
.profile-link:last-child {
  border-bottom: 0;
}
.profile-link:hover {
  background: #f8fafc;
}
.profile-link strong {
  color: #1769e0;
  font-size: 11px;
}

.search-status-card,
.progress-card,
.momentum-card {
  padding: 16px;
}
.rail-card-title {
  color: #1c2638;
  font-size: 14px;
  font-weight: 750;
}
.rail-card-subtitle {
  margin-top: 2px;
  color: #8a95a5;
  font-size: 11px;
}
.status-line {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 13px;
  color: #4b596b;
  font-size: 12px;
}
.status-pulse {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #22a06b;
  box-shadow: 0 0 0 4px rgba(34, 160, 107, 0.12);
}
.mini-metrics {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  margin: 14px 0;
}
.mini-metrics div {
  display: flex;
  flex-direction: column;
  padding: 10px;
  border-radius: 8px;
  background: #f6f8fb;
}
.mini-metrics strong {
  color: #172033;
  font-size: 20px;
  line-height: 1;
}
.mini-metrics span {
  margin-top: 5px;
  color: #8a95a5;
  font-size: 10px;
}
.search-status-card :deep(.q-btn) {
  min-height: 36px;
  border-radius: 18px;
  font-size: 12px;
}

.rail-card-heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 15px 15px 8px;
}
.rail-card-heading > .q-icon {
  color: #f0a11a;
}
.quick-action-list {
  padding: 0 7px 8px;
}
.quick-action-list :deep(.q-item) {
  min-height: 62px;
  padding: 7px 8px;
  border-radius: 8px;
}
.quick-action-list :deep(.q-item:hover) {
  background: #f6f8fb;
}
.quick-action-list :deep(.q-item__section--avatar) {
  min-width: 45px;
}
.quick-action-list :deep(.q-item__label) {
  color: #354154;
  font-size: 12px;
  font-weight: 650;
}
.quick-action-list :deep(.q-item__label--caption) {
  margin-top: 2px;
  color: #939dac;
  font-size: 10.5px;
  font-weight: 400;
}
.quick-action-list :deep(.q-item__section--side) {
  padding-left: 4px;
  color: #b6bec9;
}
.quick-icon {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border-radius: 9px;
  font-size: 18px;
}
.quick-icon--blue {
  color: #1769e0;
  background: #eaf2ff;
}
.quick-icon--violet {
  color: #6558d3;
  background: #f0edff;
}
.quick-icon--amber {
  color: #b87808;
  background: #fff4dc;
}

.progress-number {
  margin-top: 15px;
  color: #1769e0;
  font-size: 32px;
  font-weight: 800;
  letter-spacing: -1px;
  line-height: 1;
}
.progress-number span {
  font-size: 17px;
}
.progress-label {
  margin-top: 3px;
  color: #8a95a5;
  font-size: 11px;
}
.progress-row {
  display: flex;
  justify-content: space-between;
  margin-top: 12px;
  color: #647084;
  font-size: 11.5px;
}
.progress-row strong {
  color: #263449;
}

.momentum-card {
  background: linear-gradient(145deg, #f0f5ff, #fff);
}
.momentum-icon {
  display: grid;
  place-items: center;
  width: 40px;
  height: 40px;
  margin-bottom: 12px;
  border-radius: 10px;
  color: #1769e0;
  background: #fff;
  box-shadow: 0 4px 14px rgba(23, 105, 224, 0.12);
}
.momentum-card p {
  margin: 7px 0 12px;
  color: #657184;
  font-size: 11.5px;
  line-height: 1.5;
}
.momentum-card a {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: #1769e0;
  font-size: 11.5px;
  font-weight: 700;
  text-decoration: none;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
  flex-wrap: wrap;
}

.page-kicker {
  margin-bottom: 3px;
  color: #8b95a5;
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.55px;
  text-transform: uppercase;
}
.page-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}
.primary-action {
  border-radius: 19px;
  padding: 0 15px;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #172033;
  letter-spacing: -0.3px;
}

.page-subtitle {
  margin-top: 4px;
  font-size: 14px;
  color: #758094;
}

.skeleton-card {
  border-radius: 14px;
}

.report-tabs-card {
  margin-bottom: 14px;
  padding: 4px;
  border: 1px solid #dfe4ea;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 1px 2px rgba(30, 42, 56, 0.04);
}

.report-tabs-card :deep(.q-tab) {
  min-height: 42px;
  border-radius: 9px;
  color: #697587;
  font-size: 12px;
}
.report-tabs-card :deep(.q-tab--active) {
  background: #edf4ff;
}
.report-tabs-card :deep(.q-tab__indicator) {
  display: none;
}

.report-filters {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 18px;
  padding: 14px;
  border: 1px solid #dfe4ea;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 1px 2px rgba(30, 42, 56, 0.04);
}

.filter-control {
  width: 220px;
}

.status-control {
  width: 260px;
}

.date-control {
  width: 280px;
}

.report-result-count {
  margin-left: auto;
  color: #829ab1;
  font-size: 13px;
}

.panel-card {
  background: #fff;
  border: 1px solid #dfe4ea;
  border-radius: 12px;
  padding: 18px;
  height: 100%;
  box-shadow: 0 1px 2px rgba(30, 42, 56, 0.04);
}

.opportunity-kpi-row :deep(.stat-card) {
  padding: 14px 16px;
}

.opportunity-kpi-row :deep(.stat-icon) {
  width: 36px;
  height: 36px;
  margin-bottom: 9px;
  border-radius: 9px;
}

.opportunity-kpi-row :deep(.stat-value) {
  font-size: 24px;
}

.opportunity-kpi-row :deep(.stat-value-suffix) {
  font-size: 15px;
}

.opportunity-kpi-row :deep(.stat-label) {
  font-size: 13px;
}

.section-heading {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 12px;
}

.opportunity-chart-column {
  flex: 0 0 40%;
  max-width: 40%;
}

.opportunity-list-column {
  flex: 0 0 60%;
  max-width: 60%;
}

@media (max-width: 1023px) {
  .dashboard-grid {
    grid-template-columns: minmax(0, 1fr);
  }
  .dashboard-rail--right {
    display: none;
  }

  .opportunity-chart-column,
  .opportunity-list-column {
    flex-basis: 100%;
    max-width: 100%;
  }

  .filter-control,
  .status-control,
  .date-control {
    width: 100%;
  }

  .report-result-count {
    width: 100%;
    margin-left: 0;
  }
}

.section-title {
  color: #102a43;
  font-size: 18px;
  font-weight: 750;
  letter-spacing: -0.25px;
}

.section-subtitle {
  margin-top: 3px;
  color: #829ab1;
  font-size: 12px;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.panel-title {
  font-size: 15px;
  font-weight: 600;
  color: #172033;
}

.panel-subtitle {
  margin-top: 3px;
  color: #829ab1;
  font-size: 12px;
}

.panel-note {
  font-size: 12px;
  color: #94a3b8;
}

.panel-link {
  font-size: 13px;
  font-weight: 500;
  color: #1769e0;
  text-decoration: none;

  &:hover {
    text-decoration: underline;
  }
}

@media (max-width: 1280px) {
  .dashboard-grid {
    grid-template-columns: minmax(0, 1fr) 260px;
  }
  .dashboard-rail--left {
    display: none;
  }
}

@media (max-width: 1023px) {
  .dashboard-grid {
    grid-template-columns: minmax(0, 1fr);
  }
  .dashboard-rail--right {
    display: none;
  }
}

@media (max-width: 700px) {
  .dashboard-page {
    padding: 14px 12px 28px;
  }
  .page-header {
    align-items: flex-start;
  }
  .page-title {
    font-size: 21px;
  }
  .page-actions {
    width: 100%;
    justify-content: space-between;
  }
  .primary-action {
    flex: 1;
  }
  .report-filters {
    padding: 10px;
  }
  .panel-card {
    padding: 14px;
  }
}
</style>
