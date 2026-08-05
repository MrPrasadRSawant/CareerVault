import uuid
from datetime import date, datetime

from pydantic import Field

from app.models.enums import OpportunityStatus
from app.schemas.common import ORMModel


class OpportunityCreate(ORMModel):
    title: str = Field(min_length=1, max_length=255)
    company_id: uuid.UUID | None = None
    description: str | None = None
    application_link: str | None = Field(default=None, max_length=500)
    salary_range: str | None = Field(default=None, max_length=100)
    required_skills: list[str] | None = None
    experience_level: str | None = Field(default=None, max_length=100)
    status: OpportunityStatus = OpportunityStatus.SAVED
    source: str | None = Field(default=None, max_length=255)
    posted_date: date | None = None
    deadline: date | None = None
    notes: str | None = None


class OpportunityUpdate(ORMModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    company_id: uuid.UUID | None = None
    description: str | None = None
    application_link: str | None = Field(default=None, max_length=500)
    salary_range: str | None = Field(default=None, max_length=100)
    required_skills: list[str] | None = None
    experience_level: str | None = Field(default=None, max_length=100)
    status: OpportunityStatus | None = None
    source: str | None = Field(default=None, max_length=255)
    posted_date: date | None = None
    deadline: date | None = None
    notes: str | None = None


class OpportunityRead(ORMModel):
    id: uuid.UUID
    company_id: uuid.UUID | None
    title: str
    description: str | None
    application_link: str | None
    salary_range: str | None
    required_skills: list[str] | None
    experience_level: str | None
    status: OpportunityStatus
    source: str | None
    posted_date: date | None
    deadline: date | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
