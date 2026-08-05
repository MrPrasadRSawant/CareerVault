import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.repositories.application_repository import ApplicationRepository
from app.repositories.follow_up_repository import FollowUpRepository
from app.schemas import FollowUpCreate, FollowUpRead, FollowUpUpdate, Message

router = APIRouter(prefix="/follow-ups", tags=["follow-ups"])


def _owned_follow_up(db: Session, user_id: uuid.UUID, follow_up_id: uuid.UUID):
    follow_up = FollowUpRepository(db).get(follow_up_id)
    if follow_up is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Follow-up not found"
        )
    ApplicationRepository(db).get_owned(user_id, follow_up.application_id)
    return follow_up


@router.get("", response_model=list[FollowUpRead])
def list_follow_ups(
    application_id: uuid.UUID | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = FollowUpRepository(db)
    if application_id is None:
        return repo.list_all(limit=limit, offset=offset)
    ApplicationRepository(db).get_owned(current_user.id, application_id)
    return repo.list_owned(application_id, limit=limit, offset=offset)


@router.post("", response_model=FollowUpRead, status_code=201)
def create_follow_up(
    payload: FollowUpCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ApplicationRepository(db).get_owned(current_user.id, payload.application_id)
    return FollowUpRepository(db).create(**payload.model_dump())


@router.get("/{follow_up_id}", response_model=FollowUpRead)
def get_follow_up(
    follow_up_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _owned_follow_up(db, current_user.id, follow_up_id)


@router.patch("/{follow_up_id}", response_model=FollowUpRead)
def update_follow_up(
    follow_up_id: uuid.UUID,
    payload: FollowUpUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = FollowUpRepository(db)
    follow_up = _owned_follow_up(db, current_user.id, follow_up_id)
    return repo.update(follow_up, **payload.model_dump(exclude_unset=True))


@router.delete("/{follow_up_id}", response_model=Message)
def delete_follow_up(
    follow_up_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Message:
    repo = FollowUpRepository(db)
    repo.delete(_owned_follow_up(db, current_user.id, follow_up_id))
    return Message(detail="Follow-up deleted")
