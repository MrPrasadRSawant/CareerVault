import uuid
from datetime import datetime

from pydantic import Field

from app.models.enums import OpportunityStatus
from app.schemas.common import ORMModel


class OpportunityCreate(ORMModel):
    title: str = Field(min_length=1, max_length=255)
    company_name: str | None = Field(default=None, max_length=255)
    post_url: str | None = Field(default=None, max_length=500)
    company_career_page: str | None = Field(default=None, max_length=500)
    company_url: str | None = Field(default=None, max_length=500)
    posted_on_utc: datetime | None = None
    job_location: str | None = Field(default=None, max_length=255)
    description: str | None = None
    required_skills: list[str] | None = None
    experience_level: str | None = Field(default=None, max_length=100)
    status: OpportunityStatus = OpportunityStatus.SAVED


class OpportunityUpdate(ORMModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    company_name: str | None = Field(default=None, max_length=255)
    post_url: str | None = Field(default=None, max_length=500)
    company_career_page: str | None = Field(default=None, max_length=500)
    company_url: str | None = Field(default=None, max_length=500)
    posted_on_utc: datetime | None = None
    job_location: str | None = Field(default=None, max_length=255)
    description: str | None = None
    required_skills: list[str] | None = None
    experience_level: str | None = Field(default=None, max_length=100)
    status: OpportunityStatus | None = None


class OpportunityRead(ORMModel):
    id: uuid.UUID
    title: str
    company_name: str | None
    post_url: str | None
    company_career_page: str | None
    company_url: str | None
    posted_on_utc: datetime | None
    job_location: str | None
    description: str | None
    required_skills: list[str] | None
    experience_level: str | None
    status: OpportunityStatus
    created_by: uuid.UUID
    created_on_utc: datetime
    updated_by: uuid.UUID
    updated_on_utc: datetime
    is_deleted: bool
