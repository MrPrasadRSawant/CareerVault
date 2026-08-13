<template>
  <q-table
    v-model:expanded="expanded"
    flat
    bordered
    row-key="application_id"
    :rows="groups"
    :columns="columns"
    :loading="loading"
    :pagination="{ rowsPerPage: 10 }"
    class="group-table"
    no-data-label="No recruiter email follow-ups have been recorded yet"
  >
    <template #body="props">
      <q-tr :props="props" class="application-row">
        <q-td auto-width>
          <q-btn
            flat
            round
            dense
            size="sm"
            :icon="props.expand ? 'expand_less' : 'expand_more'"
            :aria-label="
              props.expand ? 'Collapse email chain' : 'Expand email chain'
            "
            @click="props.expand = !props.expand"
          />
        </q-td>
        <q-td key="application" :props="props">
          <button
            class="application-title"
            @click="props.expand = !props.expand"
          >
            {{ props.row.opportunity_title }}
          </button>
          <div class="company-name">
            {{ props.row.company_name || "Company not specified" }}
          </div>
        </q-td>
        <q-td key="status" :props="props">
          <q-badge
            rounded
            :style="applicationStatusStyle(props.row.application_status)"
          >
            {{ applicationStatusLabel(props.row.application_status) }}
          </q-badge>
        </q-td>
        <q-td key="latest" :props="props">
          {{ formatEmailDate(props.row.latest_received_at) }}
        </q-td>
        <q-td key="outcome" :props="props">
          <q-chip
            dense
            square
            text-color="white"
            :color="outcomeColor(props.row.latest_outcome)"
          >
            {{ outcomeLabel(props.row.latest_outcome) }}
          </q-chip>
        </q-td>
        <q-td key="count" :props="props">
          <q-badge color="blue-grey-2" text-color="blue-grey-9">
            {{ props.row.email_count }}
          </q-badge>
        </q-td>
      </q-tr>
      <q-tr v-show="props.expand" :props="props" class="email-chain-row">
        <q-td colspan="100%">
          <div class="chain-wrap">
            <div class="chain-heading">
              <q-icon name="forum" color="primary" />
              Email chain · newest first
            </div>
            <q-markup-table flat separator="horizontal" class="email-subtable">
              <thead>
                <tr>
                  <th class="text-left">Received</th>
                  <th class="text-left">From</th>
                  <th class="text-left">Subject</th>
                  <th class="text-left">Outcome</th>
                  <th class="text-left">Reason category</th>
                  <th class="text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="email in props.row.emails" :key="email.id">
                  <td class="nowrap">{{
                    formatEmailDate(email.received_at)
                  }}</td>
                  <td>
                    <div class="sender-name">{{
                      email.sender_name || email.sender_email
                    }}</div>
                    <div v-if="email.sender_name" class="sender-email">{{
                      email.sender_email
                    }}</div>
                  </td>
                  <td>
                    <button
                      class="subject-button"
                      @click="$emit('view', email)"
                    >
                      {{ email.subject }}
                    </button>
                  </td>
                  <td>
                    <q-badge :color="outcomeColor(email.outcome)">
                      {{ outcomeLabel(email.outcome) }}
                    </q-badge>
                  </td>
                  <td>{{ email.reason_category || "—" }}</td>
                  <td class="text-right nowrap">
                    <q-btn
                      flat
                      round
                      dense
                      icon="visibility"
                      color="primary"
                      @click="$emit('view', email)"
                    />
                    <q-btn
                      flat
                      round
                      dense
                      icon="edit"
                      color="primary"
                      @click="$emit('edit', email)"
                    />
                    <q-btn
                      flat
                      round
                      dense
                      icon="delete"
                      color="negative"
                      @click="$emit('delete', email)"
                    />
                  </td>
                </tr>
              </tbody>
            </q-markup-table>
          </div>
        </q-td>
      </q-tr>
    </template>
  </q-table>
</template>

<script setup lang="ts">
import { ref } from "vue";
import type { QTableProps } from "quasar";
import type { EmailFollowUp, EmailFollowUpGroup } from "@/api/emailFollowUps";
import type { ApplicationStatus } from "@/api/applications";
import {
  APPLICATION_STATUS_COLORS,
  APPLICATION_STATUS_LABELS
} from "@/modules/shared/statusColors";
import { formatEmailDate, outcomeColor, outcomeLabel } from "../utils";

defineProps<{ groups: EmailFollowUpGroup[]; loading: boolean }>();
defineEmits<{
  (event: "view", email: EmailFollowUp): void;
  (event: "edit", email: EmailFollowUp): void;
  (event: "delete", email: EmailFollowUp): void;
}>();

const expanded = ref<string[]>([]);
const columns: QTableProps["columns"] = [
  { name: "expand", label: "", field: "application_id", align: "left" },
  {
    name: "application",
    label: "Application",
    field: "opportunity_title",
    align: "left",
    sortable: true
  },
  {
    name: "status",
    label: "Application status",
    field: "application_status",
    align: "left",
    sortable: true
  },
  {
    name: "latest",
    label: "Latest email",
    field: "latest_received_at",
    align: "left",
    sortable: true
  },
  {
    name: "outcome",
    label: "Latest outcome",
    field: "latest_outcome",
    align: "left",
    sortable: true
  },
  {
    name: "count",
    label: "Emails",
    field: "email_count",
    align: "left",
    sortable: true
  }
];

function applicationStatusLabel(status: ApplicationStatus): string {
  return APPLICATION_STATUS_LABELS[status];
}

function applicationStatusStyle(status: ApplicationStatus) {
  return {
    background: APPLICATION_STATUS_COLORS[status],
    color: "var(--cv-white)",
    fontWeight: "700",
    padding: "5px 9px"
  };
}
</script>

<style lang="scss" scoped>
.group-table {
  overflow: hidden;
  border-color: var(--cv-border);
  border-radius: 14px;
  box-shadow: var(--cv-shadow-card);
}
.application-row {
  background: var(--cv-surface);
}
.application-title,
.subject-button {
  border: 0;
  padding: 0;
  background: transparent;
  color: var(--cv-primary-dark);
  font-weight: 750;
  text-align: left;
  cursor: pointer;
}
.application-title:hover,
.subject-button:hover {
  text-decoration: underline;
}
.company-name,
.sender-email {
  margin-top: 2px;
  color: var(--cv-muted-light);
  font-size: 11px;
}
.sender-name {
  color: var(--cv-text-strong);
  font-weight: 600;
}
.email-chain-row td {
  background: var(--cv-surface-soft);
}
.chain-wrap {
  margin: 4px 18px 14px 42px;
  overflow: auto;
  border: 1px solid var(--cv-border-light);
  border-radius: 10px;
  background: var(--cv-surface);
}
.chain-heading {
  display: flex;
  align-items: center;
  gap: 7px;
  border-bottom: 1px solid var(--cv-border-light);
  padding: 11px 14px;
  color: var(--cv-navy);
  font-size: 12px;
  font-weight: 750;
}
.email-subtable {
  min-width: 920px;
}
.nowrap {
  white-space: nowrap;
}
@media (max-width: 700px) {
  .chain-wrap {
    margin-left: 0;
  }
}
</style>
