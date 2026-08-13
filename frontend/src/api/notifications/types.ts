export type NotificationType = "opportunity" | "email_follow_up";

export interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  message: string;
  entity_id: string;
  action_path: string;
  is_seen: boolean;
  seen_at: string | null;
  created_at: string;
}

export interface NotificationCount {
  unseen_count: number;
}
