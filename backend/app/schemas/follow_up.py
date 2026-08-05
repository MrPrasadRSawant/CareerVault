import uuid
from datetime import datetime

from pydantic import Field

from app.models.enums import FollowUpStatus
from app.schemas.common import ORMModel


class FollowUpCreate(ORMModel):
    application_id: uuid.UUID
    scheduled_at: datetime
    subject: str | None = Field(default=None, max_length=255)
    message: str | None = None
    status: FollowUpStatus = FollowUpStatus.PENDING


class FollowUpUpdate(ORMModel):
    scheduled_at: datetime | None = None
    subject: str | None = Field(default=None, max_length=255)
    message: str | None = None
    status: FollowUpStatus | None = None
    completed_at: datetime | None = None


class FollowUpRead(ORMModel):
    id: uuid.UUID
    application_id: uuid.UUID
    scheduled_at: datetime
    subject: str | None
    message: str | None
    status: FollowUpStatus
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime
