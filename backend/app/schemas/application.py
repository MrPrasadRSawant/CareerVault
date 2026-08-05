import uuid
from datetime import date, datetime

from pydantic import Field

from app.models.enums import ApplicationStatus
from app.schemas.common import ORMModel


class ApplicationCreate(ORMModel):
    opportunity_id: uuid.UUID
    resume_id: uuid.UUID | None = None
    cover_letter_id: uuid.UUID | None = None
    status: ApplicationStatus = ApplicationStatus.APPLIED
    applied_date: date | None = None
    notes: str | None = None


class ApplicationUpdate(ORMModel):
    resume_id: uuid.UUID | None = None
    cover_letter_id: uuid.UUID | None = None
    applied_date: date | None = None
    notes: str | None = None


class ApplicationStatusUpdate(ORMModel):
    status: ApplicationStatus
    note: str | None = None


class ApplicationStatusHistoryRead(ORMModel):
    id: uuid.UUID
    application_id: uuid.UUID
    status: ApplicationStatus
    changed_at: datetime
    note: str | None


class ApplicationRead(ORMModel):
    id: uuid.UUID
    opportunity_id: uuid.UUID
    resume_id: uuid.UUID | None
    cover_letter_id: uuid.UUID | None
    status: ApplicationStatus
    applied_date: date | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
