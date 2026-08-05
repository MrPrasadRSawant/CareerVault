import uuid
from datetime import datetime

from pydantic import Field

from app.schemas.common import ORMModel


class ResumeCreate(ORMModel):
    name: str = Field(min_length=1, max_length=255)
    version: str | None = Field(default=None, max_length=50)
    is_active: bool = False


class ResumeUpdate(ORMModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    version: str | None = Field(default=None, max_length=50)
    is_active: bool | None = None


class ResumeRead(ORMModel):
    id: uuid.UUID
    name: str
    version: str | None
    file_name: str | None
    content_type: str | None
    file_size: int | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
