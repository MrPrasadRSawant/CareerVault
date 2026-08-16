import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.models.enums import UserRole
from app.schemas.common import ORMModel


class AdminUserRead(ORMModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime


class AdminUserPage(BaseModel):
    items: list[AdminUserRead]
    total: int
    limit: int
    offset: int


class AdminUserStatusUpdate(BaseModel):
    is_active: bool


class AdminRoleCountRead(BaseModel):
    role: UserRole
    count: int


class AdminRegistrationPeriodRead(BaseModel):
    period: str
    role_counts: list[AdminRoleCountRead] = Field(default_factory=list)


class AdminOverviewRead(BaseModel):
    total_users: int
    active_users: int
    blocked_users: int
    registrations_today: int
    new_users_last_7_days: int
    new_users_last_30_days: int
    role_counts: list[AdminRoleCountRead] = Field(default_factory=list)
    registrations_by_day: list[AdminRegistrationPeriodRead] = Field(
        default_factory=list
    )
    registrations_by_month: list[AdminRegistrationPeriodRead] = Field(
        default_factory=list
    )
    registrations_by_year: list[AdminRegistrationPeriodRead] = Field(
        default_factory=list
    )
    recent_users: list[AdminUserRead] = Field(default_factory=list)
