import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_user_from_api_key
from app.core.database import get_db
from app.models.application import Application
from app.models.email_follow_up import EmailFollowUp
from app.models.job_opportunity import JobOpportunity
from app.models.user import User
from app.repositories.application_repository import ApplicationRepository
from app.repositories.email_follow_up_repository import EmailFollowUpRepository
from app.schemas import (
    EmailAgentApplication,
    EmailFollowUpCreate,
    EmailFollowUpRead,
    EmailFollowUpUpdate,
)
from app.services.email_follow_up_service import (
    email_follow_up_create_values,
    email_follow_up_update_values,
)

router = APIRouter(prefix="/email-agent", tags=["email agent"])


@router.get(
    "/applications",
    response_model=list[EmailAgentApplication],
    summary="Find applications that may match a recruiter email",
)
def search_applications(
    query: str | None = Query(default=None, max_length=200),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_api_key),
) -> list[EmailAgentApplication]:
    statement = (
        select(Application)
        .join(Application.opportunity)
        .where(Application.user_id == current_user.id)
        .options(joinedload(Application.opportunity))
        .order_by(Application.applied_date.desc(), Application.created_at.desc())
        .limit(limit)
    )
    if query and query.strip():
        term = f"%{query.strip()}%"
        statement = statement.where(
            or_(
                JobOpportunity.title.ilike(term),
                JobOpportunity.company_name.ilike(term),
                JobOpportunity.job_location.ilike(term),
                Application.notes.ilike(term),
            )
        )
    applications = list(db.scalars(statement))
    return [
        EmailAgentApplication(
            application_id=application.id,
            opportunity_id=application.opportunity_id,
            opportunity_title=application.opportunity.title,
            company_name=application.opportunity.company_name,
            job_location=application.opportunity.job_location,
            application_status=application.status,
            applied_date=application.applied_date,
        )
        for application in applications
    ]


@router.post(
    "/follow-ups",
    response_model=EmailFollowUpRead,
    status_code=status.HTTP_201_CREATED,
    summary="Record a classified recruiter email",
)
def record_email_follow_up(
    payload: EmailFollowUpCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_api_key),
) -> EmailFollowUp:
    ApplicationRepository(db).get_owned(current_user.id, payload.application_id)
    repo = EmailFollowUpRepository(db)
    if payload.external_message_id:
        existing = repo.find_by_external_message(
            current_user.id, payload.application_id, payload.external_message_id
        )
        if existing is not None:
            return existing
    return repo.create(**email_follow_up_create_values(payload))


@router.patch("/follow-ups/{email_follow_up_id}", response_model=EmailFollowUpRead)
def revise_email_follow_up_classification(
    email_follow_up_id: uuid.UUID,
    payload: EmailFollowUpUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_api_key),
) -> EmailFollowUp:
    repo = EmailFollowUpRepository(db)
    follow_up = repo.get_owned(current_user.id, email_follow_up_id)
    if payload.application_id is not None:
        ApplicationRepository(db).get_owned(current_user.id, payload.application_id)
    return repo.update(follow_up, **email_follow_up_update_values(payload))
