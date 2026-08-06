<template>
  <q-page class="dashboard-page">
    <div class="page-header">
      <div>
        <div class="page-title">Dashboard</div>
        <div class="page-subtitle">
          Welcome back, {{ auth.user?.full_name }} — here's an overview of your
          job search.
        </div>
      </div>
      <q-btn
        unelevated
        no-caps
        outline
        color="primary"
        icon="refresh"
        label="Refresh"
        :loading="loading"
        @click="load"
      />
    </div>

    <q-banner v-if="error" rounded class="q-mb-md" color="negative">
      <template #avatar>
        <q-icon name="error_outline" />
      </template>
      {{ error }}
      <template #action>
        <q-btn flat dense label="Try again" text-color="white" @click="load" />
      </template>
    </q-banner>

    <template v-if="loading">
      <div class="row q-col-gutter-md">
        <div v-for="i in 4" :key="'kpi' + i" class="col-12 col-sm-6 col-md-3">
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
          <q-tab name="applications" icon="assignment" label="Applications" />
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

      <div v-if="activeReport === 'applications'" class="row q-col-gutter-md">
        <div class="col-12 col-sm-6 col-md-3">
          <StatCard
            icon="assignment"
            label="Applications"
            :value="totalApplications"
            :hint="`${waitingForResponseCount} awaiting response`"
            accent="#219EBC"
            :to="{ name: 'applications' }"
          />
        </div>
        <div class="col-12 col-sm-6 col-md-3">
          <StatCard
            icon="route"
            label="Active pipeline"
            :value="activePipelineCount"
            :hint="`${interviewStageCount} at interview stage`"
            accent="#2B6CB0"
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
            accent="#D99A2B"
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
          <div class="col-3 col-sm-3">
            <StatCard
              icon="work_outline"
              label="Total opportunities"
              :value="totalOpportunities"
              hint="Matching the current filters"
              accent="#219EBC"
              :to="{ name: 'opportunities' }"
            />
          </div>
          <div class="col-3 col-sm-3">
            <StatCard
              icon="track_changes"
              label="Active opportunities"
              :value="activeOpportunities"
              :hint="`${totalOpportunities - activeOpportunities} closed or archived`"
              accent="#2B6CB0"
              :to="{ name: 'opportunities' }"
            />
          </div>
          <div class="col-3 col-sm-3">
            <StatCard
              icon="add_chart"
              label="Added in 30 days"
              :value="opportunitiesAddedLast30Days"
              hint="Newly captured opportunities"
              accent="#D99A2B"
              :to="{ name: 'opportunities' }"
            />
          </div>
          <div class="col-3 col-sm-3">
            <StatCard
              icon="conversion_path"
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
                      totalOpportunities === 1 ? "opportunity" : "opportunities"
                    }}
                    across your pipeline
                  </div>
                </div>
                <router-link class="panel-link" :to="{ name: 'opportunities' }">
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
                <router-link class="panel-link" :to="{ name: 'opportunities' }">
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
              >Conversion, momentum, interviews, and follow-up execution</div
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
                <div class="panel-note">{{ overdueFollowUpCount }} overdue</div>
              </div>
              <FollowUpsCard :items="pendingFollowUps" />
            </div>
          </div>
        </div>
      </template>
    </template>
  </q-page>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
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
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #023047;
  letter-spacing: -0.3px;
}

.page-subtitle {
  margin-top: 4px;
  font-size: 14px;
  color: #64748b;
}

.skeleton-card {
  border-radius: 14px;
}

.report-tabs-card {
  margin-bottom: 14px;
  border-bottom: 1px solid #dce6eb;
}

.report-filters {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 18px;
  padding: 14px;
  border: 1px solid #e1e9ee;
  border-radius: 12px;
  background: #fff;
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
  border: 1px solid #e6edf1;
  border-radius: 14px;
  padding: 20px;
  height: 100%;
  box-shadow: 0 1px 3px rgba(2, 48, 71, 0.06);
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
  color: #023047;
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
  color: #219ebc;
  text-decoration: none;

  &:hover {
    text-decoration: underline;
  }
}
</style>
