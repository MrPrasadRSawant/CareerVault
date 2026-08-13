import uuid
from datetime import date, datetime
from typing import Any

from pydantic import EmailStr, Field, field_validator

from app.models.enums import ApplicationStatus, EmailFollowUpOutcome
from app.schemas.common import ORMModel


class EmailFollowUpCreate(ORMModel):
    application_id: uuid.UUID
    external_message_id: str | None = Field(default=None, max_length=500)
    thread_id: str | None = Field(default=None, max_length=500)
    subject: str = Field(min_length=1, max_length=500)
    sender_email: EmailStr
    sender_name: str | None = Field(default=None, max_length=255)
    recipient_emails: list[EmailStr] | None = None
    received_at: datetime
    body_text: str | None = None
    outcome: EmailFollowUpOutcome = EmailFollowUpOutcome.PENDING
    reason: str | None = None
    reason_category: str | None = Field(default=None, max_length=100)
    ai_confidence: float | None = Field(default=None, ge=0, le=1)
    raw_metadata: dict[str, Any] | None = None

    @field_validator("external_message_id", "thread_id", "sender_name", "reason_category")
    @classmethod
    def empty_string_to_none(cls, value: str | None) -> str | None:
        return value.strip() or None if value is not None else None


class EmailFollowUpUpdate(ORMModel):
    application_id: uuid.UUID | None = None
    external_message_id: str | None = Field(default=None, max_length=500)
    thread_id: str | None = Field(default=None, max_length=500)
    subject: str | None = Field(default=None, min_length=1, max_length=500)
    sender_email: EmailStr | None = None
    sender_name: str | None = Field(default=None, max_length=255)
    recipient_emails: list[EmailStr] | None = None
    received_at: datetime | None = None
    body_text: str | None = None
    outcome: EmailFollowUpOutcome | None = None
    reason: str | None = None
    reason_category: str | None = Field(default=None, max_length=100)
    ai_confidence: float | None = Field(default=None, ge=0, le=1)
    raw_metadata: dict[str, Any] | None = None


class EmailFollowUpRead(ORMModel):
    id: uuid.UUID
    application_id: uuid.UUID
    external_message_id: str | None
    thread_id: str | None
    subject: str
    sender_email: str
    sender_name: str | None
    recipient_emails: list[str] | None
    received_at: datetime
    body_text: str | None
    outcome: EmailFollowUpOutcome
    reason: str | None
    reason_category: str | None
    ai_confidence: float | None
    raw_metadata: dict[str, Any] | None
    created_at: datetime
    updated_at: datetime


class EmailFollowUpGroup(ORMModel):
    application_id: uuid.UUID
    opportunity_title: str
    company_name: str | None
    application_status: ApplicationStatus
    applied_date: date | None
    latest_received_at: datetime
    latest_outcome: EmailFollowUpOutcome
    email_count: int
    emails: list[EmailFollowUpRead]


class EmailAgentApplication(ORMModel):
    application_id: uuid.UUID
    opportunity_id: uuid.UUID
    opportunity_title: str
    company_name: str | None
    job_location: str | None
    application_status: ApplicationStatus
    applied_date: date | None
