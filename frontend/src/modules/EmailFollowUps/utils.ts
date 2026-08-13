import type { EmailFollowUpOutcome } from "@/api/emailFollowUps";

export const emailOutcomeOptions: {
  label: string;
  value: EmailFollowUpOutcome;
  color: string;
  icon: string;
}[] = [
  { label: "Pending", value: "pending", color: "warning", icon: "schedule" },
  { label: "Won", value: "won", color: "positive", icon: "check_circle" },
  { label: "Lost", value: "lost", color: "negative", icon: "cancel" }
];

export function outcomeLabel(outcome: EmailFollowUpOutcome): string {
  return (
    emailOutcomeOptions.find(option => option.value === outcome)?.label ??
    outcome
  );
}

export function outcomeColor(outcome: EmailFollowUpOutcome): string {
  return (
    emailOutcomeOptions.find(option => option.value === outcome)?.color ??
    "grey"
  );
}

export function formatEmailDate(value: string): string {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short"
  }).format(new Date(value));
}
