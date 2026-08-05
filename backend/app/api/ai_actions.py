import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_from_api_key
from app.core.database import get_db
from app.models.enums import OpportunityStatus
from app.models.job_opportunity import JobOpportunity
from app.models.user import User
from app.repositories.opportunity_repository import OpportunityRepository
from app.schemas import Message, OpportunityRead
from app.schemas.ai_actions import AiOpportunityBatchCreate, AiOpportunityCreate, AiOpportunityUpdate

router = APIRouter(prefix="/ai", tags=["AI Actions"])


@router.get("/opportunities", response_model=list[OpportunityRead], summary="Search this user's opportunities")
def search_opportunities(
    query: str | None = None,
    company_name: str | None = None,
    job_location: str | None = None,
    status_filter: OpportunityStatus | None = Query(default=None, alias="status"),
    posted_after_utc: datetime | None = None,
    posted_before_utc: datetime | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_api_key),
) -> list[JobOpportunity]:
    filters = [JobOpportunity.created_by == current_user.id, JobOpportunity.is_deleted.is_(False)]
    if query:
        term = f"%{query.strip()}%"
        filters.append(or_(JobOpportunity.title.ilike(term), JobOpportunity.company_name.ilike(term), JobOpportunity.description.ilike(term)))
    if company_name:
        filters.append(JobOpportunity.company_name.ilike(f"%{company_name.strip()}%"))
    if job_location:
        filters.append(JobOpportunity.job_location.ilike(f"%{job_location.strip()}%"))
    if status_filter:
        filters.append(JobOpportunity.status == status_filter)
    if posted_after_utc:
        filters.append(JobOpportunity.posted_on_utc >= posted_after_utc)
    if posted_before_utc:
        filters.append(JobOpportunity.posted_on_utc <= posted_before_utc)
    stmt = select(JobOpportunity).where(*filters).order_by(JobOpportunity.created_on_utc.desc()).limit(limit).offset(offset)
    return list(db.scalars(stmt))


@router.post("/opportunities", response_model=OpportunityRead, status_code=status.HTTP_201_CREATED)
def create_opportunity(
    payload: AiOpportunityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_api_key),
) -> JobOpportunity:
    now = datetime.now(timezone.utc)
    values = payload.model_dump()
    values["status"] = OpportunityStatus.DRAFT
    return OpportunityRepository(db).create(created_by=current_user.id, created_on_utc=now, updated_by=current_user.id, updated_on_utc=now, **values)


@router.post("/opportunities/bulk", response_model=list[OpportunityRead], status_code=status.HTTP_201_CREATED)
def create_opportunities_bulk(
    payload: AiOpportunityBatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_api_key),
) -> list[JobOpportunity]:
    repo = OpportunityRepository(db)
    created: list[JobOpportunity] = []
    now = datetime.now(timezone.utc)
    for item in payload.opportunities:
        values = item.model_dump()
        values["status"] = OpportunityStatus.DRAFT
        created.append(repo.model(created_by=current_user.id, created_on_utc=now, updated_by=current_user.id, updated_on_utc=now, **values))
    db.add_all(created)
    db.commit()
    for opportunity in created:
        db.refresh(opportunity)
    return created


@router.patch("/opportunities/{opportunity_id}", response_model=OpportunityRead)
def update_draft_opportunity(
    opportunity_id: uuid.UUID,
    payload: AiOpportunityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_api_key),
) -> JobOpportunity:
    repo = OpportunityRepository(db)
    opportunity = repo.get_owned(current_user.id, opportunity_id)
    if opportunity.status != OpportunityStatus.DRAFT:
        raise HTTPException(status_code=409, detail="Only draft opportunities can be edited through AI Actions")
    values = payload.model_dump(exclude_unset=True)
    values.pop("status", None)
    values.update(status=OpportunityStatus.DRAFT, updated_by=current_user.id, updated_on_utc=datetime.now(timezone.utc))
    return repo.update(opportunity, **values)


@router.delete("/opportunities/{opportunity_id}", response_model=Message)
def delete_draft_opportunity(
    opportunity_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_api_key),
) -> Message:
    repo = OpportunityRepository(db)
    opportunity = repo.get_owned(current_user.id, opportunity_id)
    if opportunity.status != OpportunityStatus.DRAFT:
        raise HTTPException(status_code=409, detail="Only draft opportunities can be deleted through AI Actions")
    repo.update(opportunity, is_deleted=True, updated_by=current_user.id, updated_on_utc=datetime.now(timezone.utc))
    return Message(detail="Draft opportunity deleted")
