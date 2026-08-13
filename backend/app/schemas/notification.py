import uuid
from datetime import datetime

from app.models.enums import NotificationType
from app.schemas.common import ORMModel


class NotificationRead(ORMModel):
    id: uuid.UUID
    type: NotificationType
    title: str
    message: str
    entity_id: uuid.UUID
    action_path: str
    is_seen: bool
    seen_at: datetime | None
    created_at: datetime


class NotificationSeenUpdate(ORMModel):
    is_seen: bool


class NotificationCountRead(ORMModel):
    unseen_count: int
