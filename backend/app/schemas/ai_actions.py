import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import OpportunityStatus
from app.schemas.opportunity import OpportunityCreate, OpportunityRead, OpportunityUpdate


class AiOpportunityCreate(OpportunityCreate):
    status: OpportunityStatus = OpportunityStatus.DRAFT


class AiOpportunityBatchCreate(BaseModel):
    opportunities: list[AiOpportunityCreate] = Field(min_length=1, max_length=100)


class AiOpportunityFilter(BaseModel):
    query: str | None = None
    company_name: str | None = None
    job_location: str | None = None
    status: OpportunityStatus | None = None
    posted_after_utc: datetime | None = None
    posted_before_utc: datetime | None = None
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class AiOpportunityUpdate(OpportunityUpdate):
    pass
