import { api } from "@/api/client";
import type { Notification, NotificationCount } from "./types";

export type {
  Notification,
  NotificationCount,
  NotificationType
} from "./types";

export const notificationApi = {
  list(isSeen?: boolean): Promise<Notification[]> {
    return api
      .get("/notifications", {
        params: isSeen === undefined ? undefined : { is_seen: isSeen }
      })
      .then(response => response.data);
  },

  unseenCount(): Promise<number> {
    return api
      .get<NotificationCount>("/notifications/unseen-count")
      .then(response => response.data.unseen_count);
  },

  setSeen(id: string, isSeen: boolean): Promise<Notification> {
    return api
      .patch(`/notifications/${id}/seen`, { is_seen: isSeen })
      .then(response => response.data);
  },

  markAllSeen(): Promise<void> {
    return api.patch("/notifications/mark-all-seen").then(() => undefined);
  }
};
