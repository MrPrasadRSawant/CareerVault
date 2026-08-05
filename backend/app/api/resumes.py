import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.repositories.resume_repository import ResumeRepository
from app.schemas import Message, ResumeCreate, ResumeRead, ResumeUpdate
from app.services.upload_service import save_upload

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.get("", response_model=list[ResumeRead])
def list_resumes(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list:
    return ResumeRepository(db).list_owned(current_user.id, limit=limit, offset=offset)


@router.post("", response_model=ResumeRead, status_code=201)
def create_resume(
    payload: ResumeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ResumeRepository(db).create(user_id=current_user.id, **payload.model_dump())


@router.post("/upload", response_model=ResumeRead, status_code=201)
async def upload_resume(
    file: UploadFile = File(...),
    name: str | None = Form(default=None),
    version: str | None = Form(default=None),
    is_active: bool = Form(default=False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = ResumeRepository(db)
    file_name, file_path, file_size = save_upload(file, current_user.id)
    if is_active:
        for resume in repo.list_owned(current_user.id):
            repo.update(resume, is_active=False)
    return repo.create(
        user_id=current_user.id,
        name=name or file_name,
        version=version,
        file_name=file_name,
        file_path=file_path,
        content_type=file.content_type,
        file_size=file_size,
        is_active=is_active,
    )


@router.get("/{resume_id}", response_model=ResumeRead)
def get_resume(
    resume_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ResumeRepository(db).get_owned(current_user.id, resume_id)


@router.get("/{resume_id}/download")
def download_resume(
    resume_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume = ResumeRepository(db).get_owned(current_user.id, resume_id)
    path = Path(resume.file_path)
    if not path.is_file():
        raise FileNotFoundError(resume.file_path)
    return FileResponse(path, filename=resume.file_name, media_type="application/octet-stream")


@router.patch("/{resume_id}", response_model=ResumeRead)
def update_resume(
    resume_id: uuid.UUID,
    payload: ResumeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = ResumeRepository(db)
    resume = repo.get_owned(current_user.id, resume_id)
    values = payload.model_dump(exclude_unset=True)
    if values.get("is_active"):
        for other in repo.list_owned(current_user.id):
            if other.id != resume.id:
                repo.update(other, is_active=False)
    return repo.update(resume, **values)


@router.delete("/{resume_id}", response_model=Message)
def delete_resume(
    resume_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Message:
    repo = ResumeRepository(db)
    resume = repo.get_owned(current_user.id, resume_id)
    Path(resume.file_path).unlink(missing_ok=True)
    repo.delete(resume)
    return Message(detail="Resume deleted")
