<template>
  <section class="registration-card">
    <div class="chart-header">
      <div>
        <h3>{{ title }}</h3>
        <p>{{ subtitle }}</p>
      </div>
      <span class="total-badge">{{ total }} total</span>
    </div>

    <div class="chart-legend" aria-hidden="true">
      <span><i class="applicant-dot"></i>Job Applicant</span>
      <span><i class="admin-dot"></i>System Admin</span>
    </div>

    <div
      class="chart-groups"
      role="img"
      :aria-label="`${title}, registrations grouped by user role`"
      :style="{
        gridTemplateColumns: `repeat(${points.length}, minmax(0, 1fr))`
      }"
    >
      <div v-for="point in points" :key="point.period" class="chart-group">
        <div class="bar-pair">
          <div
            class="bar-track"
            :title="`${periodTitle(point.period)} — Job Applicant: ${countFor(point, 'job_applicant')}`"
          >
            <div
              class="role-bar applicant-bar"
              :class="{
                'role-bar--empty': countFor(point, 'job_applicant') === 0
              }"
              :style="{
                height: `${heightFor(countFor(point, 'job_applicant'))}%`
              }"
            >
              <span v-if="countFor(point, 'job_applicant')">{{
                countFor(point, "job_applicant")
              }}</span>
            </div>
          </div>
          <div
            class="bar-track"
            :title="`${periodTitle(point.period)} — System Admin: ${countFor(point, 'system_admin')}`"
          >
            <div
              class="role-bar admin-bar"
              :class="{
                'role-bar--empty': countFor(point, 'system_admin') === 0
              }"
              :style="{
                height: `${heightFor(countFor(point, 'system_admin'))}%`
              }"
            >
              <span v-if="countFor(point, 'system_admin')">{{
                countFor(point, "system_admin")
              }}</span>
            </div>
          </div>
        </div>
        <span class="period-label">{{ periodLabel(point.period) }}</span>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { AdminRegistrationPeriod } from "@/api/admin";
import type { UserRole } from "@/api/auth";

defineOptions({ name: "RegistrationRoleChart" });

const props = defineProps<{
  title: string;
  subtitle: string;
  periodKind: "day" | "month" | "year";
  points: AdminRegistrationPeriod[];
}>();

const total = computed(() =>
  props.points.reduce(
    (sum, point) =>
      sum +
      point.role_counts.reduce((roleSum, item) => roleSum + item.count, 0),
    0
  )
);
const maxCount = computed(() =>
  Math.max(
    ...props.points.flatMap(point => point.role_counts.map(item => item.count)),
    1
  )
);

function countFor(point: AdminRegistrationPeriod, role: UserRole) {
  return point.role_counts.find(item => item.role === role)?.count ?? 0;
}

function heightFor(count: number) {
  return count === 0 ? 2 : Math.max(12, (count / maxCount.value) * 100);
}

function periodDate(period: string) {
  const normalized =
    props.periodKind === "day"
      ? `${period}T00:00:00Z`
      : `${period}-01T00:00:00Z`;
  return new Date(normalized);
}

function periodLabel(period: string) {
  if (props.periodKind === "year") return period;
  if (props.periodKind === "month") {
    return new Intl.DateTimeFormat("en", {
      month: "short",
      year: "2-digit",
      timeZone: "UTC"
    }).format(periodDate(period));
  }
  return new Intl.DateTimeFormat("en", {
    weekday: "short",
    day: "numeric",
    timeZone: "UTC"
  }).format(periodDate(period));
}

function periodTitle(period: string) {
  if (props.periodKind === "year") return period;
  return new Intl.DateTimeFormat("en", {
    month: "long",
    day: props.periodKind === "day" ? "numeric" : undefined,
    year: "numeric",
    timeZone: "UTC"
  }).format(periodDate(period));
}
</script>

<style lang="scss" scoped>
.registration-card {
  min-width: 0;
  padding: 17px;
  border: 1px solid #dfe4ea;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 1px 2px rgba(30, 42, 56, 0.04);
}
.chart-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
}
.chart-header h3 {
  margin: 0;
  color: #263449;
  font-size: 13px;
  font-weight: 750;
}
.chart-header p {
  margin: 3px 0 0;
  color: #929cab;
  font-size: 9.5px;
}
.total-badge {
  flex: 0 0 auto;
  padding: 4px 7px;
  border-radius: 999px;
  color: #526279;
  background: #f2f5f8;
  font-size: 9px;
  font-weight: 700;
}
.chart-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 13px;
  margin-top: 15px;
  color: #6e7a8c;
  font-size: 9px;
}
.chart-legend span {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}
.chart-legend i {
  width: 7px;
  height: 7px;
  border-radius: 2px;
}
.applicant-dot {
  background: #1769e0;
}
.admin-dot {
  background: #7168df;
}
.chart-groups {
  display: grid;
  gap: clamp(5px, 1vw, 13px);
  min-width: 0;
  margin-top: 13px;
}
.chart-group {
  min-width: 0;
  text-align: center;
}
.bar-pair {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: clamp(2px, 0.5vw, 5px);
  height: 146px;
  padding: 17px 2px 0;
  border-bottom: 1px solid #e3e8ee;
}
.bar-track {
  display: flex;
  align-items: flex-end;
  width: min(26px, 42%);
  height: 100%;
}
.role-bar {
  position: relative;
  width: 100%;
  min-height: 3px;
  border-radius: 4px 4px 1px 1px;
  transition: height 180ms ease;
}
.role-bar span {
  position: absolute;
  top: -15px;
  left: 50%;
  color: #59667a;
  font-size: 8px;
  font-weight: 750;
  transform: translateX(-50%);
}
.applicant-bar {
  background: linear-gradient(180deg, #4d92ed, #1769e0);
}
.admin-bar {
  background: linear-gradient(180deg, #9189ee, #665ddb);
}
.role-bar--empty {
  background: #e9edf2;
}
.period-label {
  display: block;
  overflow: hidden;
  margin-top: 7px;
  color: #8792a3;
  font-size: 8.5px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@media (max-width: 520px) {
  .registration-card {
    padding: 14px 12px;
  }
  .chart-groups {
    gap: 3px;
  }
  .bar-pair {
    gap: 2px;
  }
  .role-bar span {
    display: none;
  }
}
</style>
