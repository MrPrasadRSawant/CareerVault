import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class AdminExceptionLogRead(BaseModel):
    id: uuid.UUID
    request_id: str
    user_id: uuid.UUID | None
    user_name: str | None
    user_email: str | None
    occurred_at: datetime
    method: str
    route_template: str
    query_parameter_names: list[str] = Field(default_factory=list)
    status_code: int
    exception_type: str
    message: str
    fingerprint: str
    ip_address: str | None
    user_agent: str | None
    app_environment: str
    is_handled: bool


class AdminExceptionLogDetail(AdminExceptionLogRead):
    traceback: str


class AdminExceptionLogPage(BaseModel):
    items: list[AdminExceptionLogRead]
    total: int
    limit: int
    offset: int


class AdminExceptionOverviewRead(BaseModel):
    exceptions_last_24_hours: int
    exceptions_last_7_days: int
    unique_fingerprints_last_24_hours: int
    retention_days: int
