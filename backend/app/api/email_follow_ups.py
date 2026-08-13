import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.email_follow_up import EmailFollowUp
from app.models.enums import EmailFollowUpOutcome
from app.models.user import User
from app.repositories.application_repository import ApplicationRepository
from app.repositories.email_follow_up_repository import EmailFollowUpRepository
from app.schemas import (
    EmailFollowUpCreate,
    EmailFollowUpGroup,
    EmailFollowUpRead,
    EmailFollowUpUpdate,
    Message,
)
from app.services.email_follow_up_service import (
    email_follow_up_create_values,
    email_follow_up_update_values,
)

router = APIRouter(prefix="/email-follow-ups", tags=["email follow-ups"])


def _groups(
    db: Session,
    user_id: uuid.UUID,
    application_id: uuid.UUID | None,
    outcome: EmailFollowUpOutcome | None,
    search: str | None,
) -> list[EmailFollowUpGroup]:
    applications = EmailFollowUpRepository(db).list_grouped_source(
        user_id, application_id
    )
    query = search.strip().lower() if search else None
    result: list[EmailFollowUpGroup] = []
    for application in applications:
        emails = sorted(
            application.email_follow_ups,
            key=lambda email: email.received_at,
            reverse=True,
        )
        if outcome is not None and not any(email.outcome == outcome for email in emails):
            continue
        if query:
            searchable = " ".join(
                filter(
                    None,
                    [
                        application.opportunity.title,
                        application.opportunity.company_name,
                        *[
                            " ".join(
                                filter(
                                    None,
                                    [
                                        email.subject,
                                        email.sender_email,
                                        email.sender_name,
                                        email.reason,
                                        email.reason_category,
                                    ],
                                )
                            )
                            for email in emails
                        ],
                    ],
                )
            ).lower()
            if query not in searchable:
                continue
        latest = emails[0]
        result.append(
            EmailFollowUpGroup(
                application_id=application.id,
                opportunity_title=application.opportunity.title,
                company_name=application.opportunity.company_name,
                application_status=application.status,
                applied_date=application.applied_date,
                latest_received_at=latest.received_at,
                latest_outcome=latest.outcome,
                email_count=len(emails),
                emails=emails,
            )
        )
    return sorted(result, key=lambda group: group.latest_received_at, reverse=True)


@router.get("", response_model=list[EmailFollowUpGroup])
def list_email_follow_up_groups(
    application_id: uuid.UUID | None = None,
    outcome: EmailFollowUpOutcome | None = None,
    search: str | None = Query(default=None, max_length=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[EmailFollowUpGroup]:
    if application_id is not None:
        ApplicationRepository(db).get_owned(current_user.id, application_id)
    return _groups(db, current_user.id, application_id, outcome, search)


@router.post("", response_model=EmailFollowUpRead, status_code=status.HTTP_201_CREATED)
def create_email_follow_up(
    payload: EmailFollowUpCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> EmailFollowUp:
    ApplicationRepository(db).get_owned(current_user.id, payload.application_id)
    return EmailFollowUpRepository(db).create(
        **email_follow_up_create_values(payload)
    )


@router.get("/{email_follow_up_id}", response_model=EmailFollowUpRead)
def get_email_follow_up(
    email_follow_up_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> EmailFollowUp:
    return EmailFollowUpRepository(db).get_owned(current_user.id, email_follow_up_id)


@router.patch("/{email_follow_up_id}", response_model=EmailFollowUpRead)
def update_email_follow_up(
    email_follow_up_id: uuid.UUID,
    payload: EmailFollowUpUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> EmailFollowUp:
    repo = EmailFollowUpRepository(db)
    follow_up = repo.get_owned(current_user.id, email_follow_up_id)
    if payload.application_id is not None:
        ApplicationRepository(db).get_owned(current_user.id, payload.application_id)
    return repo.update(follow_up, **email_follow_up_update_values(payload))


@router.delete("/{email_follow_up_id}", response_model=Message)
def delete_email_follow_up(
    email_follow_up_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Message:
    repo = EmailFollowUpRepository(db)
    repo.delete(repo.get_owned(current_user.id, email_follow_up_id))
    return Message(detail="Email follow-up deleted")
