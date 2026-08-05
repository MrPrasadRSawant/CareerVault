import uuid
from datetime import datetime

from pydantic import Field

from app.schemas.common import ORMModel


class CompanyCreate(ORMModel):
    name: str = Field(min_length=1, max_length=255)
    website: str | None = Field(default=None, max_length=500)
    location: str | None = Field(default=None, max_length=255)
    industry: str | None = Field(default=None, max_length=255)
    notes: str | None = None


class CompanyUpdate(ORMModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    website: str | None = Field(default=None, max_length=500)
    location: str | None = Field(default=None, max_length=255)
    industry: str | None = Field(default=None, max_length=255)
    notes: str | None = None


class CompanyRead(ORMModel):
    id: uuid.UUID
    name: str
    website: str | None
    location: str | None
    industry: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
