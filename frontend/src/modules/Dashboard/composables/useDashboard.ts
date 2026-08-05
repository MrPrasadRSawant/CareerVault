import { computed, ref } from "vue";
import { applicationApi } from "@/api/applications";
import type { Application } from "@/api/applications";
import { followUpApi } from "@/api/followUps";
import type { FollowUp } from "@/api/followUps";
import { interviewApi } from "@/api/interviews";
import type { Interview } from "@/api/interviews";
import { opportunityApi } from "@/api/opportunities";
import type { Opportunity } from "@/api/opportunities";
import { resumeApi } from "@/api/resumes";
import type { Resume } from "@/api/resumes";
import {
  APPLICATION_STATUS_COLORS,
  APPLICATION_STATUS_LABELS,
  APPLICATION_STATUS_ORDER,
  OPPORTUNITY_STATUS_COLORS,
  OPPORTUNITY_STATUS_LABELS,
  OPPORTUNITY_STATUS_ORDER
} from "@/modules/shared/statusColors";

export interface StatusDatum {
  label: string;
  value: number;
  color: string;
  percent: number;
}

export interface UpcomingInterviewRow {
  id: string;
  scheduled_at: string;
  type: string;
  title: string;
}

export interface WeeklyPoint {
  label: string;
  value: number;
}

export interface FunnelDatum {
  label: string;
  value: number;
  percent: number;
  color: string;
}

function startOfWeek(date: Date): Date {
  const d = new Date(date);
  d.setHours(0, 0, 0, 0);
  const day = (d.getDay() + 6) % 7;
  d.setDate(d.getDate() - day);
  return d;
}

export function useDashboard() {
  const loading = ref(false);
  const error = ref<string | null>(null);

  const opportunities = ref<Opportunity[]>([]);
  const applications = ref<Application[]>([]);
  const resumes = ref<Resume[]>([]);
  const interviews = ref<Interview[]>([]);
  const followUps = ref<FollowUp[]>([]);

  async function load() {
    loading.value = true;
    error.value = null;
    try {
      const [opps, apps, res, ints, fus] = await Promise.all([
        opportunityApi.list(),
        applicationApi.list(),
        resumeApi.list(),
        interviewApi.list(),
        followUpApi.list()
      ]);
      opportunities.value = opps;
      applications.value = apps;
      resumes.value = res;
      interviews.value = ints;
      followUps.value = fus;
    } catch {
      error.value = "Could not load dashboard data";
    } finally {
      loading.value = false;
    }
  }

  function buildStatusData<T extends string>(
    items: { status: T }[],
    order: T[],
    labels: Record<T, string>,
    colors: Record<T, string>
  ): StatusDatum[] {
    const total = items.length;
    return order.map(status => {
      const value = items.filter(i => i.status === status).length;
      return {
        label: labels[status],
        value,
        color: colors[status],
        percent: total > 0 ? Math.round((value / total) * 100) : 0
      };
    });
  }

  const totalOpportunities = computed(() => opportunities.value.length);

  const activeOpportunities = computed(
    () =>
      opportunities.value.filter(
        o => o.status !== "rejected" && o.status !== "archived"
      ).length
  );

  const totalApplications = computed(() => applications.value.length);

  const respondedApplications = computed(
    () =>
      applications.value.filter(
        a =>
          a.status !== "applied" &&
          a.status !== "withdrawn"
      ).length
  );

  const activePipelineCount = computed(
    () =>
      applications.value.filter(
        a => a.status !== "rejected" && a.status !== "withdrawn"
      ).length
  );

  const waitingForResponseCount = computed(
    () => applications.value.filter(a => a.status === "applied").length
  );

  const interviewStageCount = computed(
    () =>
      applications.value.filter(
        a =>
          a.status === "interview_scheduled" ||
          a.status === "interview_completed" ||
          a.status === "offer"
      ).length
  );

  const responseRate = computed(() =>
    totalApplications.value
      ? Math.round((respondedApplications.value / totalApplications.value) * 100)
      : 0
  );

  const interviewConversionRate = computed(() =>
    totalApplications.value
      ? Math.round((interviewStageCount.value / totalApplications.value) * 100)
      : 0
  );

  const offersCount = computed(
    () => applications.value.filter(a => a.status === "offer").length
  );

  const upcomingInterviewCount = computed(
    () =>
      interviews.value.filter(
        i => new Date(i.scheduled_at).getTime() >= Date.now() - 24 * 3600 * 1000
      ).length
  );

  const upcomingIn7Days = computed(
    () =>
      interviews.value.filter(i => {
        const t = new Date(i.scheduled_at).getTime();
        return (
          t >= Date.now() - 24 * 3600 * 1000 &&
          t <= Date.now() + 7 * 24 * 3600 * 1000
        );
      }).length
  );

  const totalResumes = computed(() => resumes.value.length);

  const activeResumes = computed(
    () => resumes.value.filter(r => r.is_active).length
  );

  const opportunityByStatus = computed<StatusDatum[]>(() =>
    buildStatusData(
      opportunities.value,
      OPPORTUNITY_STATUS_ORDER,
      OPPORTUNITY_STATUS_LABELS,
      OPPORTUNITY_STATUS_COLORS
    )
  );

  const applicationByStatus = computed<StatusDatum[]>(() =>
    buildStatusData(
      applications.value,
      APPLICATION_STATUS_ORDER,
      APPLICATION_STATUS_LABELS,
      APPLICATION_STATUS_COLORS
    )
  );

  const applicationFunnel = computed<FunnelDatum[]>(() => {
    const total = totalApplications.value;
    const stages = [
      { label: "Applications sent", value: total, color: "#1F6F8B" },
      { label: "Responses received", value: respondedApplications.value, color: "#2B6CB0" },
      { label: "Interview stage", value: interviewStageCount.value, color: "#D99A2B" },
      { label: "Offers", value: offersCount.value, color: "#2F855A" }
    ];
    return stages.map(stage => ({
      ...stage,
      percent: total ? Math.round((stage.value / total) * 100) : 0
    }));
  });

  const applicationsPerWeek = computed<WeeklyPoint[]>(() => {
    const currentWeekStart = startOfWeek(new Date());
    const points: WeeklyPoint[] = [];
    for (let i = 7; i >= 0; i--) {
      const start = new Date(currentWeekStart);
      start.setDate(start.getDate() - i * 7);
      const end = new Date(start);
      end.setDate(end.getDate() + 7);
      const value = applications.value.filter(a => {
        if (a.applied_date === null) return false;
        const t = new Date(a.applied_date).getTime();
        return t >= start.getTime() && t < end.getTime();
      }).length;
      points.push({
        label: start.toLocaleDateString(undefined, {
          month: "short",
          day: "numeric"
        }),
        value
      });
    }
    return points;
  });

  const recentOpportunities = computed(() =>
    [...opportunities.value]
      .sort((a, b) => b.created_on_utc.localeCompare(a.created_on_utc))
      .slice(0, 5)
  );

  const upcomingInterviews = computed<UpcomingInterviewRow[]>(() => {
    const sorted = [...interviews.value]
      .filter(
        i => new Date(i.scheduled_at).getTime() >= Date.now() - 24 * 3600 * 1000
      )
      .sort((a, b) => a.scheduled_at.localeCompare(b.scheduled_at))
      .slice(0, 5);

    return sorted.map(i => {
      const app = applications.value.find(a => a.id === i.application_id);
      const opp = app
        ? opportunities.value.find(o => o.id === app.opportunity_id)
        : undefined;
      return {
        id: i.id,
        scheduled_at: i.scheduled_at,
        type: i.type,
        title: opp?.title ?? `Application #${i.application_id}`
      };
    });
  });

  const pendingFollowUps = computed(() =>
    [...followUps.value]
      .filter(f => f.status !== "completed")
      .sort((a, b) => a.scheduled_at.localeCompare(b.scheduled_at))
      .slice(0, 5)
  );

  const overdueFollowUpCount = computed(
    () =>
      followUps.value.filter(
        followUp =>
          followUp.status !== "completed" &&
          new Date(followUp.scheduled_at).getTime() < Date.now()
      ).length
  );

  return {
    loading,
    error,
    load,
    totalOpportunities,
    activeOpportunities,
    totalApplications,
    respondedApplications,
    activePipelineCount,
    waitingForResponseCount,
    interviewStageCount,
    responseRate,
    interviewConversionRate,
    offersCount,
    upcomingInterviewCount,
    upcomingIn7Days,
    totalResumes,
    activeResumes,
    opportunityByStatus,
    applicationByStatus,
    applicationFunnel,
    applicationsPerWeek,
    recentOpportunities,
    upcomingInterviews,
    pendingFollowUps,
    overdueFollowUpCount
  };
}
