import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.repositories.application_repository import ApplicationRepository
from app.repositories.interview_repository import InterviewRepository
from app.schemas import InterviewCreate, InterviewRead, InterviewUpdate, Message

router = APIRouter(prefix="/interviews", tags=["interviews"])


def _owned_interview(db: Session, user_id: uuid.UUID, interview_id: uuid.UUID):
    interview = InterviewRepository(db).get(interview_id)
    if interview is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found"
        )
    ApplicationRepository(db).get_owned(user_id, interview.application_id)
    return interview


@router.get("", response_model=list[InterviewRead])
def list_interviews(
    application_id: uuid.UUID | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = InterviewRepository(db)
    if application_id is None:
        return repo.list_all(limit=limit, offset=offset)
    ApplicationRepository(db).get_owned(current_user.id, application_id)
    return repo.list_owned(application_id, limit=limit, offset=offset)


@router.post("", response_model=InterviewRead, status_code=201)
def create_interview(
    payload: InterviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ApplicationRepository(db).get_owned(current_user.id, payload.application_id)
    return InterviewRepository(db).create(**payload.model_dump())


@router.get("/{interview_id}", response_model=InterviewRead)
def get_interview(
    interview_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _owned_interview(db, current_user.id, interview_id)


@router.patch("/{interview_id}", response_model=InterviewRead)
def update_interview(
    interview_id: uuid.UUID,
    payload: InterviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = InterviewRepository(db)
    interview = _owned_interview(db, current_user.id, interview_id)
    return repo.update(interview, **payload.model_dump(exclude_unset=True))


@router.delete("/{interview_id}", response_model=Message)
def delete_interview(
    interview_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Message:
    repo = InterviewRepository(db)
    repo.delete(_owned_interview(db, current_user.id, interview_id))
    return Message(detail="Interview deleted")
