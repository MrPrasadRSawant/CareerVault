import type { NotificationType } from "@/api/notifications";

export const notificationTypeDetails: Record<
  NotificationType,
  { label: string; icon: string; color: string; background: string }
> = {
  opportunity: {
    label: "Opportunity",
    icon: "work_outline",
    color: "#1f6f8b",
    background: "#e7f3f8"
  },
  email_follow_up: {
    label: "Recruiter email",
    icon: "mark_email_read",
    color: "#b7791f",
    background: "#fff4d6"
  }
};

export function formatNotificationDate(value: string): string {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short"
  }).format(new Date(value));
}
