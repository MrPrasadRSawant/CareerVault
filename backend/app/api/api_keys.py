import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.api_key import ApiKey
from app.models.user import User
from app.repositories.api_key_repository import ApiKeyRepository
from app.schemas import ApiKeyCreate, ApiKeyCreated, ApiKeyRead, ApiKeyUpdate, Message

router = APIRouter(prefix="/settings/api-keys", tags=["settings - API keys"])


@router.get("", response_model=list[ApiKeyRead])
def list_api_keys(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[ApiKey]:
    return list(db.scalars(select(ApiKey).where(ApiKey.user_id == current_user.id).order_by(ApiKey.created_on_utc.desc())))


@router.post("", response_model=ApiKeyCreated, status_code=status.HTTP_201_CREATED)
def create_api_key(payload: ApiKeyCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    api_key, raw_key = ApiKeyRepository(db).create_for_user(current_user.id, name=payload.name, expires_on_utc=payload.expires_on_utc)
    return {"id": api_key.id, "name": api_key.name, "key_prefix": api_key.key_prefix, "created_on_utc": api_key.created_on_utc, "last_used_on_utc": api_key.last_used_on_utc, "expires_on_utc": api_key.expires_on_utc, "is_revoked": api_key.is_revoked, "key": raw_key}


@router.delete("/{api_key_id}", response_model=Message)
def revoke_api_key(api_key_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Message:
    key = db.scalar(select(ApiKey).where(ApiKey.id == api_key_id, ApiKey.user_id == current_user.id))
    if key is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="API key not found")
    key.is_revoked = True
    db.commit()
    return Message(detail="API key revoked")


@router.patch("/{api_key_id}", response_model=ApiKeyRead)
def update_api_key(api_key_id: uuid.UUID, payload: ApiKeyUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> ApiKey:
    key = db.scalar(select(ApiKey).where(ApiKey.id == api_key_id, ApiKey.user_id == current_user.id, ApiKey.is_revoked.is_(False)))
    if key is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Active API key not found")
    key.name = payload.name.strip()
    key.expires_on_utc = payload.expires_on_utc
    db.commit()
    db.refresh(key)
    return key
