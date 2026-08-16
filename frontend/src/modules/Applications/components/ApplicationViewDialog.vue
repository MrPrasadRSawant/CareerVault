<template>
  <q-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <q-card v-if="application" class="view-card">
      <q-card-section class="row items-start"
        ><div
          ><div class="view-kicker">APPLICATION DETAILS</div
          ><div class="view-title">{{
            application.opportunity?.title ?? "Unknown opportunity"
          }}</div
          ><div class="view-company">{{
            application.opportunity?.company_name || "Company not specified"
          }}</div></div
        ><q-space /><q-btn flat round dense icon="close" v-close-popup
      /></q-card-section>
      <q-card-section class="view-body">
        <div class="row items-center q-gutter-sm q-mb-md"
          ><q-badge rounded :style="statusStyle(application.status)">{{
            statusLabel(application.status)
          }}</q-badge
          ><span class="muted"
            >Applied {{ application.applied_date || "date not recorded" }}</span
          ></div
        >
        <div class="detail-grid"
          ><div
            ><span>Location</span
            ><strong>{{
              application.opportunity?.job_location || "Not specified"
            }}</strong></div
          ><div
            ><span>Resume</span
            ><strong>{{ application.resume?.name || "Not attached" }}</strong
            ><small v-if="application.resume?.version">{{
              application.resume.version
            }}</small></div
          ><div
            ><span>Cover letter</span
            ><strong>{{
              application.cover_letter_id ? "Attached" : "Not attached"
            }}</strong></div
          ><div
            ><span>Created</span
            ><strong>{{ formatDate(application.created_at) }}</strong></div
          ></div
        >
        <div v-if="application.notes" class="notes-block"
          ><div class="detail-label">Notes</div
          ><div>{{ application.notes }}</div></div
        >
        <div class="row q-gutter-sm q-mt-md"
          ><q-btn
            v-if="application.opportunity?.post_url"
            outline
            color="primary"
            icon="open_in_new"
            label="Job post"
            :href="application.opportunity.post_url"
            target="_blank" /><q-btn
            v-if="application.opportunity?.company_career_page"
            outline
            color="primary"
            icon="work_outline"
            label="Career page"
            :href="application.opportunity.company_career_page"
            target="_blank"
        /></div>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import type { ApplicationStatus } from "@/api/applications";
import {
  APPLICATION_STATUS_COLORS,
  APPLICATION_STATUS_LABELS
} from "@/modules/shared/statusColors";
import type { ApplicationRow } from "../types";
defineProps<{ modelValue: boolean; application: ApplicationRow | null }>();
defineEmits<{ (event: "update:modelValue", value: boolean): void }>();
function statusLabel(status: ApplicationStatus) {
  return APPLICATION_STATUS_LABELS[status];
}
function statusStyle(status: ApplicationStatus) {
  return {
    background: APPLICATION_STATUS_COLORS[status],
    color: "var(--cv-white)",
    fontWeight: "700",
    padding: "5px 10px"
  };
}
function formatDate(value: string) {
  return value ? new Date(value).toLocaleDateString() : "—";
}
</script>

<style lang="scss" scoped>
.view-card {
  width: min(600px, 94vw);
  border-radius: 14px;
}
.view-kicker {
  color: var(--cv-muted-light);
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.08em;
}
.view-title {
  margin-top: 6px;
  color: var(--cv-navy);
  font-size: 22px;
  font-weight: 800;
}
.view-company {
  margin-top: 4px;
  color: var(--cv-muted);
}
.view-body {
  padding-top: 0;
}
.muted {
  color: var(--cv-muted-light);
  font-size: 12px;
}
.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  border-top: 1px solid var(--cv-border-light);
  border-bottom: 1px solid var(--cv-border-light);
  padding: 16px 0;
}
.detail-grid span,
.detail-label {
  display: block;
  color: var(--cv-muted-light);
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
}
.detail-grid strong {
  display: block;
  margin-top: 3px;
  color: var(--cv-text-strong);
  font-size: 13px;
}
.detail-grid small {
  display: block;
  margin-top: 2px;
  color: var(--cv-muted);
  font-size: 11px;
}
.notes-block {
  margin-top: 16px;
  color: var(--cv-muted);
  line-height: 1.5;
  white-space: pre-wrap;
}
</style>
