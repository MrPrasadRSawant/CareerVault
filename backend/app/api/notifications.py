import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.notification import Notification
from app.models.user import User
from app.repositories.notification_repository import NotificationRepository
from app.schemas import (
    Message,
    NotificationCountRead,
    NotificationRead,
    NotificationSeenUpdate,
)

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=list[NotificationRead])
def list_notifications(
    is_seen: bool | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Notification]:
    return NotificationRepository(db).list_owned(
        current_user.id, is_seen=is_seen, limit=limit, offset=offset
    )


@router.get("/unseen-count", response_model=NotificationCountRead)
def get_unseen_notification_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> NotificationCountRead:
    return NotificationCountRead(
        unseen_count=NotificationRepository(db).unseen_count(current_user.id)
    )


@router.patch("/mark-all-seen", response_model=Message)
def mark_all_notifications_seen(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Message:
    updated = NotificationRepository(db).mark_all_seen(current_user.id)
    return Message(detail=f"Marked {updated} notifications as seen")


@router.patch("/{notification_id}/seen", response_model=NotificationRead)
def set_notification_seen(
    notification_id: uuid.UUID,
    payload: NotificationSeenUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Notification:
    repository = NotificationRepository(db)
    notification = repository.get_owned(current_user.id, notification_id)
    return repository.set_seen(notification, payload.is_seen)
