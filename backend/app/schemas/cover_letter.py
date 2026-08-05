import uuid
from datetime import datetime

from pydantic import Field

from app.schemas.common import ORMModel


class CoverLetterCreate(ORMModel):
    name: str = Field(min_length=1, max_length=255)
    content: str | None = None


class CoverLetterUpdate(ORMModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = None


class CoverLetterRead(ORMModel):
    id: uuid.UUID
    name: str
    content: str | None
    file_name: str | None
    file_size: int | None
    created_at: datetime
    updated_at: datetime
