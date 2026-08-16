import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field

from app.models.enums import (
    AuthEventType,
    AuthFailureReason,
    AuthOutcome,
    AuthSessionEndReason,
    UserRole,
)


class AdminSecurityOverviewRead(BaseModel):
    successful_logins_last_24_hours: int
    failed_logins_last_24_hours: int
    active_sessions: int
    retention_days: int


class AdminLoginEventRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID | None
    user_name: str | None
    user_email: EmailStr | None
    role: UserRole | None
    account_known: bool
    unknown_account_reference: str | None
    event_type: AuthEventType
    outcome: AuthOutcome
    failure_reason: AuthFailureReason | None
    occurred_at: datetime
    ip_address: str | None
    user_agent: str | None
    http_status: int


class AdminLoginEventPage(BaseModel):
    items: list[AdminLoginEventRead] = Field(default_factory=list)
    total: int
    limit: int
    offset: int


class AdminAuthSessionRead(BaseModel):
    user_id: uuid.UUID
    user_name: str
    user_email: EmailStr
    role: UserRole
    auth_method: AuthEventType
    started_at: datetime
    last_seen_at: datetime
    ended_at: datetime | None
    expires_at: datetime
    status: Literal["active", "ended", "expired"]
    duration_seconds: int
    duration_basis: Literal["ongoing", "exact", "estimated_last_activity"]
    end_reason: AuthSessionEndReason | None
    ip_address: str | None
    user_agent: str | None


class AdminAuthSessionPage(BaseModel):
    items: list[AdminAuthSessionRead] = Field(default_factory=list)
    total: int
    limit: int
    offset: int
