<template>
  <q-dialog
    :model-value="modelValue"
    persistent
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <q-card class="email-dialog">
      <q-card-section class="dialog-header">
        <div class="header-mark">
          <q-icon name="mark_email_read" size="22px" />
        </div>
        <div class="header-copy">
          <div class="dialog-title">
            {{ editingEmail ? "Edit email follow-up" : "New email follow-up" }}
          </div>
          <div class="dialog-subtitle">
            {{
              editingEmail
                ? "Review the message details and refine its classification."
                : "Connect a recruiter response to an application and capture its outcome."
            }}
          </div>
        </div>
        <q-space />
        <q-btn
          flat
          round
          dense
          icon="close"
          aria-label="Close dialog"
          v-close-popup
        />
      </q-card-section>

      <q-card-section class="dialog-body">
        <q-form ref="formRef" @submit.prevent="submit">
          <q-stepper
            v-model="wizardStep"
            flat
            animated
            color="primary"
            class="email-stepper"
          >
            <q-step
              :name="1"
              title="Context"
              caption="Application and sender"
              icon="link"
              :done="wizardStep > 1"
            >
              <div class="wizard-intro">
                Start by linking the response to the application it belongs to.
                This keeps the full conversation grouped in one place.
              </div>

              <div class="form-section-title">Application</div>
              <q-select
                v-model="form.applicationId"
                outlined
                emit-value
                map-options
                use-input
                input-debounce="0"
                label="Related application *"
                hint="Search by role or company"
                :options="visibleApplications"
                :rules="[required('Choose an application')]"
                @filter="filterApplications"
              >
                <template #prepend>
                  <q-icon name="assignment" color="primary" />
                </template>
                <template #no-option>
                  <q-item>
                    <q-item-section class="text-grey-7">
                      No matching applications
                    </q-item-section>
                  </q-item>
                </template>
              </q-select>

              <div class="form-section-title section-gap"
                >Sender and timing</div
              >
              <div class="row q-col-gutter-md">
                <div class="col-12 col-md-7">
                  <q-input
                    v-model="form.senderEmail"
                    outlined
                    type="email"
                    label="Recruiter email *"
                    placeholder="recruiter@company.com"
                    :rules="[required('Enter the sender email'), validEmail]"
                  >
                    <template #prepend>
                      <q-icon name="alternate_email" color="primary" />
                    </template>
                  </q-input>
                </div>
                <div class="col-12 col-md-5">
                  <q-input
                    v-model="form.senderName"
                    outlined
                    label="Recruiter name"
                    placeholder="Optional"
                  >
                    <template #prepend>
                      <q-icon name="person_outline" color="primary" />
                    </template>
                  </q-input>
                </div>
                <div class="col-12 col-md-7">
                  <ProfessionalDateTimeField
                    v-model="form.receivedAt"
                    label="Received date and time *"
                    :dense="false"
                  />
                  <div
                    v-if="stepOneAttempted && !form.receivedAt"
                    class="field-error"
                  >
                    Choose when the email was received
                  </div>
                </div>
              </div>
            </q-step>

            <q-step
              :name="2"
              title="Message"
              caption="Subject and content"
              icon="mail_outline"
              :done="wizardStep > 2"
            >
              <div class="wizard-intro">
                Preserve the useful parts of the recruiter’s message so the
                response can be understood without reopening the inbox.
              </div>

              <div class="form-section-title">Email details</div>
              <div class="row q-col-gutter-md">
                <div class="col-12">
                  <q-input
                    v-model="form.subject"
                    outlined
                    label="Subject *"
                    placeholder="Paste the original email subject"
                    :rules="[required('Enter the email subject')]"
                  >
                    <template #prepend>
                      <q-icon name="subject" color="primary" />
                    </template>
                  </q-input>
                </div>
                <div class="col-12">
                  <q-input
                    v-model="form.recipientEmails"
                    outlined
                    label="Recipients"
                    hint="Separate multiple addresses with commas"
                    :rules="[validRecipientList]"
                  >
                    <template #prepend>
                      <q-icon name="group_outlined" color="primary" />
                    </template>
                  </q-input>
                </div>
                <div class="col-12">
                  <q-input
                    v-model="form.bodyText"
                    outlined
                    type="textarea"
                    rows="7"
                    label="Email body"
                    placeholder="Paste the recruiter’s message here…"
                    class="message-field"
                  />
                </div>
              </div>

              <q-expansion-item
                icon="fingerprint"
                label="Provider identifiers"
                caption="Optional IDs used by n8n to prevent duplicates"
                header-class="identifier-header"
                class="identifier-panel"
              >
                <div class="row q-col-gutter-md q-pa-md">
                  <div class="col-12 col-md-6">
                    <q-input
                      v-model="form.externalMessageId"
                      outlined
                      dense
                      label="External message ID"
                    />
                  </div>
                  <div class="col-12 col-md-6">
                    <q-input
                      v-model="form.threadId"
                      outlined
                      dense
                      label="Thread ID"
                    />
                  </div>
                </div>
              </q-expansion-item>
            </q-step>

            <q-step
              :name="3"
              title="Classify"
              caption="Outcome and reason"
              icon="fact_check"
            >
              <div class="wizard-intro">
                Classify what this reply means. You can leave it pending when
                the hiring process is still active.
              </div>

              <div class="form-section-title">Application outcome</div>
              <div
                class="outcome-grid"
                role="radiogroup"
                aria-label="Email outcome"
              >
                <button
                  v-for="option in emailOutcomeOptions"
                  :key="option.value"
                  type="button"
                  class="outcome-option"
                  :class="[
                    `outcome-option--${option.value}`,
                    {
                      'outcome-option--selected': form.outcome === option.value
                    }
                  ]"
                  :aria-checked="form.outcome === option.value"
                  role="radio"
                  @click="form.outcome = option.value"
                >
                  <span class="outcome-icon">
                    <q-icon :name="option.icon" size="20px" />
                  </span>
                  <span>
                    <strong>{{ option.label }}</strong>
                    <small>{{ outcomeDescription(option.value) }}</small>
                  </span>
                  <q-icon
                    v-if="form.outcome === option.value"
                    name="check_circle"
                    class="selected-check"
                  />
                </button>
              </div>

              <div class="form-section-title section-gap"
                >Classification details</div
              >
              <div class="row q-col-gutter-md">
                <div class="col-12 col-md-7">
                  <q-select
                    v-model="form.reasonCategory"
                    outlined
                    clearable
                    use-input
                    fill-input
                    hide-selected
                    new-value-mode="add-unique"
                    label="Reason category"
                    hint="Choose a category or enter your own"
                    :options="reasonCategoryOptions"
                    @filter="filterReasonCategories"
                  >
                    <template #prepend>
                      <q-icon name="category" color="primary" />
                    </template>
                  </q-select>
                </div>
                <div class="col-12 col-md-5">
                  <div class="confidence-field">
                    <div class="confidence-heading">
                      <span>AI confidence</span>
                      <strong>{{ confidenceDisplay }}</strong>
                    </div>
                    <q-slider
                      v-model="confidencePercent"
                      :min="0"
                      :max="100"
                      :step="1"
                      color="primary"
                      label
                      label-always
                    />
                    <div class="confidence-hint">
                      Optional · use when classified by AI
                    </div>
                  </div>
                </div>
                <div class="col-12">
                  <q-input
                    v-model="form.reason"
                    outlined
                    type="textarea"
                    autogrow
                    label="Outcome reason"
                    placeholder="Summarize why this response was classified this way…"
                  />
                </div>
              </div>

              <div class="review-strip">
                <q-icon name="verified" color="primary" size="20px" />
                <div>
                  <strong>Ready to save</strong>
                  <span>
                    This email will be added to the selected application’s
                    conversation history.
                  </span>
                </div>
              </div>
            </q-step>
          </q-stepper>

          <div class="dialog-actions">
            <q-btn flat no-caps label="Cancel" v-close-popup />
            <q-btn
              v-if="wizardStep > 1"
              flat
              no-caps
              color="primary"
              label="Back"
              icon="arrow_back"
              @click="wizardStep -= 1"
            />
            <q-btn
              v-if="wizardStep < 3"
              unelevated
              no-caps
              color="primary"
              label="Continue"
              icon-right="arrow_forward"
              @click="nextStep"
            />
            <q-btn
              v-if="wizardStep === 3"
              unelevated
              no-caps
              color="primary"
              type="submit"
              :loading="saving"
              :label="editingEmail ? 'Save changes' : 'Save email follow-up'"
            />
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from "vue";
import type { QForm } from "quasar";
import type {
  EmailFollowUp,
  EmailFollowUpOutcome,
  EmailFollowUpPayload
} from "@/api/emailFollowUps";
import ProfessionalDateTimeField from "@/components/ProfessionalDateTimeField.vue";
import type { ApplicationChoice } from "../types";
import { emailOutcomeOptions } from "../utils";

interface EmailFollowUpForm {
  applicationId: string;
  senderEmail: string;
  senderName: string;
  subject: string;
  receivedAt: string;
  recipientEmails: string;
  outcome: EmailFollowUpOutcome;
  reasonCategory: string | null;
  reason: string;
  bodyText: string;
  externalMessageId: string;
  threadId: string;
  aiConfidence: number | null;
}

const props = defineProps<{
  modelValue: boolean;
  editingEmail: EmailFollowUp | null;
  applications: ApplicationChoice[];
  saving: boolean;
}>();
const emit = defineEmits<{
  (event: "update:modelValue", value: boolean): void;
  (event: "save", payload: EmailFollowUpPayload): void;
}>();

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const defaultReasonCategories = [
  "Application received",
  "Screening",
  "Interview invitation",
  "Interview feedback",
  "Additional information",
  "Offer",
  "Qualifications",
  "Position filled",
  "Hiring paused",
  "Rejection",
  "Other"
];
const wizardStep = ref(1);
const stepOneAttempted = ref(false);
const formRef = ref<QForm | null>(null);
const visibleApplications = ref<{ label: string; value: string }[]>([]);
const reasonCategoryOptions = ref<string[]>(defaultReasonCategories);
const form = reactive<EmailFollowUpForm>(emptyForm());

const confidencePercent = computed({
  get: () => Math.round((form.aiConfidence ?? 0) * 100),
  set: value => {
    form.aiConfidence = value === 0 ? null : value / 100;
  }
});
const confidenceDisplay = computed(() =>
  form.aiConfidence === null
    ? "Not set"
    : `${Math.round(form.aiConfidence * 100)}%`
);

watch([() => props.modelValue, () => props.editingEmail], ([open]) => {
  if (!open) return;
  wizardStep.value = 1;
  stepOneAttempted.value = false;
  visibleApplications.value = applicationOptions();
  reasonCategoryOptions.value = [...defaultReasonCategories];
  const email = props.editingEmail;
  Object.assign(
    form,
    email
      ? {
          applicationId: email.application_id,
          senderEmail: email.sender_email,
          senderName: email.sender_name ?? "",
          subject: email.subject,
          receivedAt: localDateTimeValue(email.received_at),
          recipientEmails: email.recipient_emails?.join(", ") ?? "",
          outcome: email.outcome,
          reasonCategory: email.reason_category ?? "",
          reason: email.reason ?? "",
          bodyText: email.body_text ?? "",
          externalMessageId: email.external_message_id ?? "",
          threadId: email.thread_id ?? "",
          aiConfidence: email.ai_confidence
        }
      : emptyForm()
  );
});

function emptyForm(): EmailFollowUpForm {
  return {
    applicationId: "",
    senderEmail: "",
    senderName: "",
    subject: "",
    receivedAt: localDateTimeValue(new Date().toISOString()),
    recipientEmails: "",
    outcome: "pending",
    reasonCategory: "",
    reason: "",
    bodyText: "",
    externalMessageId: "",
    threadId: "",
    aiConfidence: null
  };
}

function applicationOptions() {
  return props.applications.map(application => ({
    label: application.label,
    value: application.applicationId
  }));
}

function filterApplications(
  value: string,
  update: (callback: () => void) => void
) {
  update(() => {
    const query = value.trim().toLowerCase();
    visibleApplications.value = query
      ? applicationOptions().filter(option =>
          option.label.toLowerCase().includes(query)
        )
      : applicationOptions();
  });
}

function filterReasonCategories(
  value: string,
  update: (callback: () => void) => void
) {
  update(() => {
    const query = value.trim().toLowerCase();
    reasonCategoryOptions.value = query
      ? defaultReasonCategories.filter(option =>
          option.toLowerCase().includes(query)
        )
      : [...defaultReasonCategories];
  });
}

function localDateTimeValue(value: string): string {
  const date = new Date(value);
  const offset = date.getTimezoneOffset() * 60_000;
  return new Date(date.getTime() - offset).toISOString().slice(0, 16);
}

function required(message: string) {
  return (value: string | null) => Boolean(value?.trim()) || message;
}

function validEmail(value: string) {
  return (
    !value || emailPattern.test(value.trim()) || "Enter a valid email address"
  );
}

function validRecipientList(value: string) {
  const invalid = value
    .split(",")
    .map(email => email.trim())
    .filter(Boolean)
    .find(email => !emailPattern.test(email));
  return !invalid || `“${invalid}” is not a valid email address`;
}

function outcomeDescription(outcome: EmailFollowUpOutcome): string {
  return {
    pending: "Process is still active",
    won: "Positive result or offer",
    lost: "Application was closed"
  }[outcome];
}

async function nextStep() {
  if (wizardStep.value === 1) {
    stepOneAttempted.value = true;
    if (
      !form.applicationId ||
      !form.senderEmail.trim() ||
      !emailPattern.test(form.senderEmail.trim()) ||
      !form.receivedAt
    ) {
      await formRef.value?.validate();
      return;
    }
  }
  if (wizardStep.value === 2) {
    if (
      !form.subject.trim() ||
      validRecipientList(form.recipientEmails) !== true
    ) {
      await formRef.value?.validate();
      return;
    }
  }
  wizardStep.value = Math.min(3, wizardStep.value + 1);
}

async function submit() {
  if (
    !(await formRef.value?.validate()) ||
    !form.applicationId ||
    !form.receivedAt
  )
    return;
  const recipients = form.recipientEmails
    .split(",")
    .map(value => value.trim())
    .filter(Boolean);
  emit("save", {
    application_id: form.applicationId,
    sender_email: form.senderEmail.trim(),
    sender_name: form.senderName.trim() || null,
    subject: form.subject.trim(),
    received_at: new Date(form.receivedAt).toISOString(),
    recipient_emails: recipients.length ? recipients : null,
    outcome: form.outcome,
    reason_category: form.reasonCategory?.trim() || null,
    reason: form.reason.trim() || null,
    body_text: form.bodyText.trim() || null,
    external_message_id: form.externalMessageId.trim() || null,
    thread_id: form.threadId.trim() || null,
    ai_confidence: form.aiConfidence
  });
}
</script>

<style lang="scss" scoped>
.email-dialog {
  width: min(820px, 94vw);
  max-width: 820px;
  border-radius: 14px;
}
.dialog-header {
  display: flex;
  align-items: flex-start;
  gap: 13px;
  border-bottom: 1px solid var(--cv-border-light);
  padding: 18px 20px;
}
.header-mark {
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
.dialog-title {
  color: var(--cv-navy);
  font-size: 20px;
  font-weight: 750;
  line-height: 1.3;
}
.dialog-subtitle {
  margin-top: 3px;
  color: var(--cv-muted-light);
  font-size: 12px;
  line-height: 1.45;
}
.dialog-body {
  max-height: 76vh;
  overflow-y: auto;
  padding: 18px 20px 20px;
}
.email-stepper {
  background: transparent;
}
.email-stepper :deep(.q-stepper__header) {
  border: 1px solid #e7eef2;
  border-radius: 10px;
  background: #f8fafb;
  box-shadow: none;
}
.email-stepper :deep(.q-stepper__tab) {
  min-height: 68px;
  padding: 12px 16px;
}
.email-stepper :deep(.q-stepper__title) {
  font-weight: 700;
}
.email-stepper :deep(.q-stepper__caption) {
  color: var(--cv-muted-light);
}
.email-stepper :deep(.q-stepper__step-inner) {
  padding: 20px 2px 4px;
}
.wizard-intro {
  max-width: 680px;
  margin-bottom: 18px;
  color: var(--cv-muted);
  font-size: 13px;
  line-height: 1.55;
}
.form-section-title {
  margin: 8px 0 12px;
  color: var(--cv-primary);
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}
.section-gap {
  margin-top: 18px;
}
.field-error {
  margin: -16px 12px 8px;
  color: var(--q-negative);
  font-size: 11px;
}
.message-field :deep(textarea) {
  line-height: 1.55;
  resize: vertical;
}
.identifier-panel {
  margin-top: 14px;
  overflow: hidden;
  border: 1px solid var(--cv-border-light);
  border-radius: 10px;
  background: var(--cv-surface-soft);
}
.identifier-panel :deep(.identifier-header) {
  min-height: 58px;
  color: var(--cv-text-strong);
}
.outcome-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}
.outcome-option {
  position: relative;
  display: flex;
  align-items: center;
  gap: 11px;
  min-height: 74px;
  border: 1px solid var(--cv-border);
  padding: 12px;
  border-radius: 11px;
  background: var(--cv-surface);
  color: var(--cv-text);
  text-align: left;
  cursor: pointer;
  transition:
    border-color 0.18s ease,
    background 0.18s ease,
    box-shadow 0.18s ease;
}
.outcome-option:hover {
  border-color: var(--cv-secondary);
  background: var(--cv-surface-soft);
}
.outcome-option--selected {
  border-color: var(--cv-primary);
  background: var(--cv-primary-soft);
  box-shadow: 0 0 0 1px var(--cv-primary);
}
.outcome-option--won.outcome-option--selected {
  border-color: var(--q-positive);
  background: #f0faf5;
  box-shadow: 0 0 0 1px var(--q-positive);
}
.outcome-option--lost.outcome-option--selected {
  border-color: var(--q-negative);
  background: #fff5f5;
  box-shadow: 0 0 0 1px var(--q-negative);
}
.outcome-icon {
  display: grid;
  width: 38px;
  height: 38px;
  flex: 0 0 auto;
  place-items: center;
  border-radius: 10px;
  background: var(--cv-empty-soft);
  color: var(--cv-muted);
}
.outcome-option--pending.outcome-option--selected .outcome-icon {
  background: #fff4d6;
  color: var(--q-warning);
}
.outcome-option--won.outcome-option--selected .outcome-icon {
  background: #dff5e9;
  color: var(--q-positive);
}
.outcome-option--lost.outcome-option--selected .outcome-icon {
  background: #fde7e7;
  color: var(--q-negative);
}
.outcome-option strong,
.outcome-option small {
  display: block;
}
.outcome-option strong {
  color: var(--cv-navy);
  font-size: 13px;
}
.outcome-option small {
  margin-top: 2px;
  color: var(--cv-muted-light);
  font-size: 10px;
}
.selected-check {
  position: absolute;
  top: 7px;
  right: 7px;
  color: var(--cv-primary);
}
.outcome-option--won .selected-check {
  color: var(--q-positive);
}
.outcome-option--lost .selected-check {
  color: var(--q-negative);
}
.confidence-field {
  min-height: 56px;
  border: 1px solid var(--cv-border);
  padding: 8px 14px 5px;
  border-radius: 4px;
}
.confidence-heading {
  display: flex;
  justify-content: space-between;
  color: var(--cv-muted);
  font-size: 12px;
}
.confidence-heading strong {
  color: var(--cv-primary-dark);
}
.confidence-field :deep(.q-slider) {
  margin: 8px 0 2px;
}
.confidence-hint {
  color: var(--cv-muted-light);
  font-size: 10px;
}
.review-strip {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-top: 20px;
  border: 1px solid #cfe6ef;
  padding: 12px 14px;
  border-radius: 10px;
  background: #f1f8fb;
}
.review-strip strong,
.review-strip span {
  display: block;
}
.review-strip strong {
  color: var(--cv-navy);
  font-size: 12px;
}
.review-strip span {
  margin-top: 2px;
  color: var(--cv-muted);
  font-size: 11px;
}
.dialog-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  padding-top: 20px;
}
@media (max-width: 700px) {
  .email-dialog {
    width: 100%;
    max-width: none;
    border-radius: 0;
  }
  .dialog-header {
    padding: 16px;
  }
  .header-mark {
    display: none;
  }
  .dialog-body {
    max-height: calc(100vh - 82px);
    padding: 14px 16px 16px;
  }
  .email-stepper :deep(.q-stepper__tab) {
    padding: 10px 7px;
  }
  .email-stepper :deep(.q-stepper__label) {
    display: none;
  }
  .outcome-grid {
    grid-template-columns: 1fr;
  }
  .dialog-actions {
    position: sticky;
    z-index: 2;
    bottom: -16px;
    margin: 10px -16px -16px;
    border-top: 1px solid var(--cv-border-light);
    padding: 12px 16px;
    background: var(--cv-surface);
  }
}
</style>
