<template>
  <q-dialog v-model="dialogOpen">
    <q-card v-if="props.opportunity" class="opportunity-dialog">
      <q-card-section class="dialog-header">
        <div
          ><div class="dialog-title">{{ props.opportunity.title }}</div
          ><div class="dialog-subtitle">{{
            props.opportunity.company_name || "Company not specified"
          }}</div></div
        >
        <q-btn flat round dense icon="close" v-close-popup />
      </q-card-section>
      <q-card-section class="view-body">
        <div class="view-status-row">
          <span
            class="status-chip"
            :style="statusStyle(props.opportunity.status)"
            >{{ statusLabel(props.opportunity.status) }}</span
          >
          <span v-if="props.opportunity.job_location"
            ><q-icon name="place" /> {{ props.opportunity.job_location }}</span
          >
        </div>
        <div class="view-links">
          <q-btn
            v-if="props.opportunity.post_url"
            flat
            no-caps
            color="primary"
            icon="open_in_new"
            label="Open job post"
            tag="a"
            :href="props.opportunity.post_url"
            target="_blank"
            rel="noopener noreferrer"
          />
          <q-btn
            v-if="props.opportunity.company_career_page"
            flat
            no-caps
            color="primary"
            icon="business"
            label="Career page"
            tag="a"
            :href="props.opportunity.company_career_page"
            target="_blank"
            rel="noopener noreferrer"
          />
          <q-btn
            v-if="props.opportunity.company_url"
            flat
            no-caps
            color="primary"
            icon="language"
            label="Company website"
            tag="a"
            :href="props.opportunity.company_url"
            target="_blank"
            rel="noopener noreferrer"
          />
        </div>
        <div class="view-grid">
          <div
            ><span>Posted</span
            ><strong>{{
              formatOpportunityDate(props.opportunity.posted_on_utc)
            }}</strong></div
          >
          <div
            ><span>Experience</span
            ><strong>{{
              props.opportunity.experience_level || "Not specified"
            }}</strong></div
          >
          <div
            ><span>Created</span
            ><strong>{{
              formatOpportunityDate(props.opportunity.created_on_utc)
            }}</strong></div
          >
          <div
            ><span>Updated</span
            ><strong>{{
              formatOpportunityDate(props.opportunity.updated_on_utc)
            }}</strong></div
          >
        </div>
        <div v-if="props.opportunity.required_skills?.length" class="view-block"
          ><span class="view-label">Skills requested</span
          ><div class="skill-list"
            ><q-chip
              v-for="skill in props.opportunity.required_skills"
              :key="skill"
              dense
              outline
              color="primary"
              >{{ skill }}</q-chip
            ></div
          ></div
        >
        <div v-if="props.opportunity.description" class="view-block"
          ><span class="view-label">Job description</span
          ><p class="view-text">{{ props.opportunity.description }}</p></div
        >
      </q-card-section>
      <q-card-actions align="right"
        ><q-btn
          flat
          no-caps
          label="Edit"
          color="primary"
          @click="editOpportunity"
      /></q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { Opportunity, OpportunityStatus } from "@/api/opportunities";
import {
  OPPORTUNITY_STATUS_COLORS,
  OPPORTUNITY_STATUS_LABELS
} from "@/modules/shared/statusColors";
import { formatOpportunityDate } from "../utils";

const props = defineProps<{
  modelValue: boolean;
  opportunity: Opportunity | null;
}>();
const emit = defineEmits<{
  (event: "update:modelValue", value: boolean): void;
  (event: "edit", opportunity: Opportunity): void;
}>();
const dialogOpen = computed({
  get: () => props.modelValue,
  set: (value: boolean) => emit("update:modelValue", value)
});
function editOpportunity() {
  if (props.opportunity) emit("edit", props.opportunity);
}
function statusLabel(status: OpportunityStatus) {
  return OPPORTUNITY_STATUS_LABELS[status];
}
function statusStyle(status: OpportunityStatus) {
  return { background: OPPORTUNITY_STATUS_COLORS[status], color: "#fff" };
}
</script>

<style lang="scss" scoped>
.opportunity-dialog {
  width: min(760px, 94vw);
  max-width: 760px;
}
.dialog-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  border-bottom: 1px solid #edf2f5;
}
.dialog-title {
  color: #102a43;
  font-size: 20px;
  font-weight: 750;
}
.dialog-subtitle {
  margin-top: 4px;
  color: #829ab1;
  font-size: 12px;
}
.view-body {
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.view-status-row,
.view-links {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  color: #627d98;
  font-size: 13px;
}
.status-chip {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
}
.view-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  padding: 14px;
  border: 1px solid #e7eef2;
  border-radius: 10px;
  background: #f8fafb;
}
.view-grid div {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.view-grid span,
.view-label {
  color: #829ab1;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.4px;
  text-transform: uppercase;
}
.view-grid strong {
  color: #243b53;
  font-size: 13px;
}
.view-block {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.skill-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
.view-text {
  margin: 0;
  color: #334e68;
  font-size: 13px;
  line-height: 1.6;
  white-space: pre-wrap;
}
@media (max-width: 700px) {
  .opportunity-dialog {
    width: 100%;
    max-width: none;
  }
  .view-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
