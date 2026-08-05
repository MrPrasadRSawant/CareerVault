import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ApiKeyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    expires_on_utc: datetime | None = None


class ApiKeyUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    expires_on_utc: datetime | None = None


class ApiKeyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    key_prefix: str
    created_on_utc: datetime
    last_used_on_utc: datetime | None
    expires_on_utc: datetime | None
    is_revoked: bool


class ApiKeyCreated(ApiKeyRead):
    key: str
