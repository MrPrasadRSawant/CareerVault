import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.enums import OpportunityStatus
from app.models.job_opportunity import JobOpportunity
from app.models.user import User
from app.repositories.opportunity_repository import OpportunityRepository
from app.schemas import (
    Message,
    OpportunityCreate,
    OpportunityRead,
    OpportunityUpdate,
)

router = APIRouter(prefix="/opportunities", tags=["opportunities"])


@router.get("", response_model=list[OpportunityRead])
def list_opportunities(
    status: OpportunityStatus | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list:
    repo = OpportunityRepository(db)
    if status is None:
        return repo.list_owned(current_user.id, limit=limit, offset=offset)
    stmt = (
        select(JobOpportunity)
        .where(
            JobOpportunity.created_by == current_user.id,
            JobOpportunity.status == status,
            JobOpportunity.is_deleted.is_(False),
        )
        .order_by(JobOpportunity.created_on_utc.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(stmt))


@router.post("", response_model=OpportunityRead, status_code=201)
def create_opportunity(
    payload: OpportunityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    now = datetime.now(timezone.utc)
    return OpportunityRepository(db).create(
        created_by=current_user.id,
        created_on_utc=now,
        updated_by=current_user.id,
        updated_on_utc=now,
        **payload.model_dump()
    )


@router.get("/{opportunity_id}", response_model=OpportunityRead)
def get_opportunity(
    opportunity_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return OpportunityRepository(db).get_owned(current_user.id, opportunity_id)


@router.patch("/{opportunity_id}", response_model=OpportunityRead)
def update_opportunity(
    opportunity_id: uuid.UUID,
    payload: OpportunityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = OpportunityRepository(db)
    opportunity = repo.get_owned(current_user.id, opportunity_id)
    return repo.update(
        opportunity,
        updated_by=current_user.id,
        updated_on_utc=datetime.now(timezone.utc),
        **payload.model_dump(exclude_unset=True),
    )


@router.delete("/{opportunity_id}", response_model=Message)
def delete_opportunity(
    opportunity_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Message:
    repo = OpportunityRepository(db)
    repo.update(
        repo.get_owned(current_user.id, opportunity_id),
        updated_by=current_user.id,
        updated_on_utc=datetime.now(timezone.utc),
        is_deleted=True,
    )
    return Message(detail="Opportunity deleted")
