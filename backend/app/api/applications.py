import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.repositories.application_repository import ApplicationRepository
from app.repositories.opportunity_repository import OpportunityRepository
from app.repositories.resume_repository import ResumeRepository
from app.repositories.status_history_repository import ApplicationStatusHistoryRepository
from app.schemas import (
    ApplicationCreate,
    ApplicationRead,
    ApplicationStatusHistoryRead,
    ApplicationStatusUpdate,
    ApplicationUpdate,
    Message,
)

router = APIRouter(prefix="/applications", tags=["applications"])


@router.get("", response_model=list[ApplicationRead])
def list_applications(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list:
    return ApplicationRepository(db).list_owned(
        current_user.id, limit=limit, offset=offset
    )


@router.post("", response_model=ApplicationRead, status_code=201)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = ApplicationRepository(db)
    OpportunityRepository(db).get_owned(current_user.id, payload.opportunity_id)
    if payload.resume_id is not None:
        ResumeRepository(db).get_owned(current_user.id, payload.resume_id)
    values = payload.model_dump()
    values["applied_date"] = values.get("applied_date") or datetime.now(timezone.utc).date()
    return repo.create(user_id=current_user.id, **values)


@router.get("/{application_id}", response_model=ApplicationRead)
def get_application(
    application_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ApplicationRepository(db).get_owned(current_user.id, application_id)


@router.patch("/{application_id}", response_model=ApplicationRead)
def update_application(
    application_id: uuid.UUID,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = ApplicationRepository(db)
    application = repo.get_owned(current_user.id, application_id)
    if payload.resume_id is not None:
        ResumeRepository(db).get_owned(current_user.id, payload.resume_id)
    return repo.update(application, **payload.model_dump(exclude_unset=True))


@router.delete("/{application_id}", response_model=Message)
def delete_application(
    application_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Message:
    repo = ApplicationRepository(db)
    repo.delete(repo.get_owned(current_user.id, application_id))
    return Message(detail="Application deleted")


@router.post("/{application_id}/status", response_model=ApplicationRead)
def update_application_status(
    application_id: uuid.UUID,
    payload: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = ApplicationRepository(db)
    application = repo.get_owned(current_user.id, application_id)
    repo.update(application, status=payload.status)

    history_repo = ApplicationStatusHistoryRepository(db)
    history_repo.create(
        application_id=application.id,
        status=payload.status,
        changed_at=datetime.now(timezone.utc),
        note=payload.note,
    )
    return application


@router.get(
    "/{application_id}/status-history",
    response_model=list[ApplicationStatusHistoryRead],
)
def list_application_status_history(
    application_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list:
    repo = ApplicationRepository(db)
    application = repo.get_owned(current_user.id, application_id)
    return list(application.status_history)
