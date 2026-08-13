import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import func, select, update

from app.models.notification import Notification
from app.repositories.base import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    model = Notification

    def get_owned(self, user_id: uuid.UUID, id: uuid.UUID) -> Notification:
        notification = self.db.scalar(
            select(Notification).where(
                Notification.id == id, Notification.user_id == user_id
            )
        )
        if notification is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found",
            )
        return notification

    def list_owned(
        self,
        user_id: uuid.UUID,
        *,
        is_seen: bool | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Notification]:
        statement = select(Notification).where(Notification.user_id == user_id)
        if is_seen is not None:
            statement = statement.where(Notification.is_seen == is_seen)
        statement = (
            statement.order_by(Notification.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.scalars(statement))

    def unseen_count(self, user_id: uuid.UUID) -> int:
        return (
            self.db.scalar(
                select(func.count())
                .select_from(Notification)
                .where(
                    Notification.user_id == user_id,
                    Notification.is_seen.is_(False),
                )
            )
            or 0
        )

    def set_seen(self, notification: Notification, is_seen: bool) -> Notification:
        notification.is_seen = is_seen
        notification.seen_at = datetime.now(timezone.utc) if is_seen else None
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def mark_all_seen(self, user_id: uuid.UUID) -> int:
        result = self.db.execute(
            update(Notification)
            .where(
                Notification.user_id == user_id,
                Notification.is_seen.is_(False),
            )
            .values(is_seen=True, seen_at=datetime.now(timezone.utc))
        )
        self.db.commit()
        return result.rowcount or 0
