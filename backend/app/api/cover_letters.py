import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.repositories.cover_letter_repository import CoverLetterRepository
from app.schemas import (
    CoverLetterCreate,
    CoverLetterRead,
    CoverLetterUpdate,
    Message,
)

router = APIRouter(prefix="/cover-letters", tags=["cover letters"])


@router.get("", response_model=list[CoverLetterRead])
def list_cover_letters(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list:
    return CoverLetterRepository(db).list_owned(
        current_user.id, limit=limit, offset=offset
    )


@router.post("", response_model=CoverLetterRead, status_code=201)
def create_cover_letter(
    payload: CoverLetterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return CoverLetterRepository(db).create(
        user_id=current_user.id, **payload.model_dump()
    )


@router.get("/{cover_letter_id}", response_model=CoverLetterRead)
def get_cover_letter(
    cover_letter_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return CoverLetterRepository(db).get_owned(current_user.id, cover_letter_id)


@router.patch("/{cover_letter_id}", response_model=CoverLetterRead)
def update_cover_letter(
    cover_letter_id: uuid.UUID,
    payload: CoverLetterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = CoverLetterRepository(db)
    cover_letter = repo.get_owned(current_user.id, cover_letter_id)
    return repo.update(cover_letter, **payload.model_dump(exclude_unset=True))


@router.delete("/{cover_letter_id}", response_model=Message)
def delete_cover_letter(
    cover_letter_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Message:
    repo = CoverLetterRepository(db)
    repo.delete(repo.get_owned(current_user.id, cover_letter_id))
    return Message(detail="Cover letter deleted")
