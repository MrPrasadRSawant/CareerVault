<template>
  <q-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <q-card v-if="email" class="detail-card">
      <q-card-section class="detail-header">
        <div class="email-icon"><q-icon name="mail" size="22px" /></div>
        <div class="header-copy">
          <div class="detail-kicker">{{ applicationLabel }}</div>
          <div class="detail-title">{{ email.subject }}</div>
          <div class="detail-sender">
            From {{ email.sender_name ? `${email.sender_name} · ` : ""
            }}{{ email.sender_email }}
          </div>
        </div>
        <q-space />
        <q-btn flat round dense icon="close" v-close-popup />
      </q-card-section>
      <q-separator />
      <q-card-section>
        <div class="summary-grid">
          <div
            ><span>Received</span
            ><strong>{{ formatEmailDate(email.received_at) }}</strong></div
          >
          <div>
            <span>Outcome</span>
            <q-badge :color="outcomeColor(email.outcome)">{{
              outcomeLabel(email.outcome)
            }}</q-badge>
          </div>
          <div
            ><span>Reason category</span
            ><strong>{{
              email.reason_category || "Not classified"
            }}</strong></div
          >
          <div
            ><span>AI confidence</span
            ><strong>{{ confidenceLabel }}</strong></div
          >
        </div>
        <div v-if="email.recipient_emails?.length" class="detail-block">
          <div class="block-label">Recipients</div>
          <div>{{ email.recipient_emails.join(", ") }}</div>
        </div>
        <div v-if="email.reason" class="detail-block reason-block">
          <div class="block-label">Classification reason</div>
          <div>{{ email.reason }}</div>
        </div>
        <div class="detail-block">
          <div class="block-label">Email body</div>
          <div class="email-body">{{
            email.body_text || "No email body was stored."
          }}</div>
        </div>
        <q-expansion-item
          v-if="
            email.external_message_id || email.thread_id || email.raw_metadata
          "
          dense
          icon="data_object"
          label="Technical details"
          class="technical-details"
        >
          <div v-if="email.external_message_id" class="technical-line"
            ><span>Message ID</span>{{ email.external_message_id }}</div
          >
          <div v-if="email.thread_id" class="technical-line"
            ><span>Thread ID</span>{{ email.thread_id }}</div
          >
          <pre v-if="email.raw_metadata">{{
            JSON.stringify(email.raw_metadata, null, 2)
          }}</pre>
        </q-expansion-item>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat no-caps label="Close" color="primary" v-close-popup />
        <q-btn
          no-caps
          label="Edit"
          icon="edit"
          color="primary"
          @click="$emit('edit', email)"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { EmailFollowUp } from "@/api/emailFollowUps";
import { formatEmailDate, outcomeColor, outcomeLabel } from "../utils";

const props = defineProps<{
  modelValue: boolean;
  email: EmailFollowUp | null;
  applicationLabel: string;
}>();
defineEmits<{
  (event: "update:modelValue", value: boolean): void;
  (event: "edit", email: EmailFollowUp): void;
}>();

const confidenceLabel = computed(() =>
  props.email?.ai_confidence == null
    ? "Not recorded"
    : `${Math.round(props.email.ai_confidence * 100)}%`
);
</script>

<style lang="scss" scoped>
.detail-card {
  width: min(720px, 96vw);
  max-height: 92vh;
  overflow: auto;
  border-radius: 14px;
}
.detail-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}
.email-icon {
  display: grid;
  width: 42px;
  height: 42px;
  flex: 0 0 auto;
  place-items: center;
  border-radius: 12px;
  background: var(--cv-primary-soft);
  color: var(--cv-primary);
}
.header-copy {
  min-width: 0;
}
.detail-kicker,
.block-label,
.summary-grid span {
  color: var(--cv-muted-light);
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
.detail-title {
  margin-top: 4px;
  color: var(--cv-navy);
  font-size: 20px;
  font-weight: 800;
}
.detail-sender {
  margin-top: 4px;
  color: var(--cv-muted);
  font-size: 12px;
}
.summary-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.summary-grid strong,
.summary-grid .q-badge {
  display: block;
  width: fit-content;
  margin-top: 4px;
}
.detail-block {
  margin-top: 18px;
  color: var(--cv-text);
  line-height: 1.55;
}
.reason-block {
  border-left: 3px solid var(--cv-amber);
  padding: 10px 12px;
  background: #fffbeb;
}
.email-body {
  margin-top: 7px;
  border: 1px solid var(--cv-border-light);
  padding: 14px;
  white-space: pre-wrap;
  border-radius: 9px;
  background: var(--cv-surface-soft);
}
.technical-details {
  margin-top: 12px;
}
.technical-line {
  padding: 4px 16px;
  overflow-wrap: anywhere;
  font-size: 12px;
}
.technical-line span {
  margin-right: 8px;
  color: var(--cv-muted-light);
  font-weight: 700;
}
pre {
  overflow: auto;
  margin: 8px 16px;
  padding: 10px;
  background: var(--cv-surface-soft);
  font-size: 11px;
}
@media (max-width: 550px) {
  .summary-grid {
    grid-template-columns: 1fr;
  }
}
</style>
