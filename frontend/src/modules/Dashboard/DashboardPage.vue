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
      <div class="row q-col-gutter-md">
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

      <div class="row q-col-gutter-md q-mt-md">
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
        <div class="col-12 col-md-6">
          <div class="panel-card">
            <div class="panel-header">
              <div class="panel-title">Recent opportunities</div>
              <router-link class="panel-link" :to="{ name: 'opportunities' }">
                View all
              </router-link>
            </div>
            <RecentOpportunities :items="recentOpportunities" />
          </div>
        </div>
        <div class="col-12 col-md-6">
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
  </q-page>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useDashboard } from "./composables/useDashboard";
import StatCard from "./components/StatCard.vue";
import StatusBars from "./components/StatusBars.vue";
import ApplicationFunnel from "./components/ApplicationFunnel.vue";
import TrendChart from "./components/TrendChart.vue";
import UpcomingInterviews from "./components/UpcomingInterviews.vue";
import RecentOpportunities from "./components/RecentOpportunities.vue";
import FollowUpsCard from "./components/FollowUpsCard.vue";

const auth = useAuthStore();

const {
  loading,
  error,
  load,
  totalApplications,
  offersCount,
  respondedApplications,
  activePipelineCount,
  waitingForResponseCount,
  interviewStageCount,
  responseRate,
  interviewConversionRate,
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

.panel-card {
  background: #fff;
  border: 1px solid #e6edf1;
  border-radius: 14px;
  padding: 20px;
  height: 100%;
  box-shadow: 0 1px 3px rgba(2, 48, 71, 0.06);
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
