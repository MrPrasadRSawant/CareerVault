import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.repositories.company_repository import CompanyRepository
from app.schemas import CompanyCreate, CompanyRead, CompanyUpdate, Message

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("", response_model=list[CompanyRead])
def list_companies(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list:
    return CompanyRepository(db).list_owned(current_user.id, limit=limit, offset=offset)


@router.post("", response_model=CompanyRead, status_code=201)
def create_company(
    payload: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return CompanyRepository(db).create(user_id=current_user.id, **payload.model_dump())


@router.get("/{company_id}", response_model=CompanyRead)
def get_company(
    company_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return CompanyRepository(db).get_owned(current_user.id, company_id)


@router.patch("/{company_id}", response_model=CompanyRead)
def update_company(
    company_id: uuid.UUID,
    payload: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = CompanyRepository(db)
    company = repo.get_owned(current_user.id, company_id)
    return repo.update(company, **payload.model_dump(exclude_unset=True))


@router.delete("/{company_id}", response_model=Message)
def delete_company(
    company_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Message:
    repo = CompanyRepository(db)
    repo.delete(repo.get_owned(current_user.id, company_id))
    return Message(detail="Company deleted")
