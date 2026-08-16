from datetime import date, datetime

from pydantic import BaseModel, Field


class RegistrationSettingsRead(BaseModel):
    daily_registration_limit: int
    registrations_used_today: int
    registrations_remaining_today: int
    counter_date_utc: date
    updated_at: datetime


class RegistrationSettingsUpdate(BaseModel):
    daily_registration_limit: int = Field(ge=1, le=1_000_000)


class LoginSecuritySettingsRead(BaseModel):
    failed_login_attempt_limit: int
    lockout_duration_minutes: int
    updated_at: datetime


class LoginSecuritySettingsUpdate(BaseModel):
    failed_login_attempt_limit: int = Field(ge=1, le=100)
    lockout_duration_minutes: int = Field(ge=1, le=1_440)
