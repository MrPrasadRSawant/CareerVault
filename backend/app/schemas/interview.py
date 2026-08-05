import uuid
from datetime import datetime

from pydantic import Field

from app.models.enums import InterviewStatus, InterviewType
from app.schemas.common import ORMModel


class InterviewCreate(ORMModel):
    application_id: uuid.UUID
    scheduled_at: datetime
    type: InterviewType = InterviewType.VIDEO
    location_or_link: str | None = Field(default=None, max_length=500)
    status: InterviewStatus = InterviewStatus.SCHEDULED
    notes: str | None = None


class InterviewUpdate(ORMModel):
    scheduled_at: datetime | None = None
    type: InterviewType | None = None
    location_or_link: str | None = Field(default=None, max_length=500)
    status: InterviewStatus | None = None
    notes: str | None = None


class InterviewRead(ORMModel):
    id: uuid.UUID
    application_id: uuid.UUID
    scheduled_at: datetime
    type: InterviewType
    location_or_link: str | None
    status: InterviewStatus
    notes: str | None
    created_at: datetime
    updated_at: datetime
