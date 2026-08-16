import uuid
from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.api_key_repository import ApiKeyRepository
from app.repositories.auth_audit_repository import AuthAuditRepository
from app.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer(auto_error=False)
api_key_scheme = APIKeyHeader(name="X-CareerVault-Key", auto_error=False)


def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise credentials_exception
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = uuid.UUID(str(payload.get("sub")))
        session_claim = payload.get("sid")
        session_id = (
            uuid.UUID(str(session_claim)) if session_claim is not None else None
        )
    except (InvalidTokenError, TypeError, ValueError):
        raise credentials_exception

    user = UserRepository(db).get(user_id)
    if user is None or not user.is_active:
        raise credentials_exception
    if session_id is not None and not AuthAuditRepository(
        db
    ).validate_and_touch_session(session_id, user.id):
        raise credentials_exception
    return user


def require_role(user: User, role: UserRole) -> User:
    if user.role != role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this area",
        )
    return user


def get_current_user(
    user: User = Depends(get_authenticated_user),
) -> User:
    """Return the current job applicant for all candidate-facing APIs."""
    return require_role(user, UserRole.JOB_APPLICANT)


def get_current_system_admin(
    user: User = Depends(get_authenticated_user),
) -> User:
    return require_role(user, UserRole.SYSTEM_ADMIN)


def get_current_user_from_api_key(
    api_key: str | None = Depends(api_key_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="A valid X-CareerVault-Key is required",
        headers={"WWW-Authenticate": "ApiKey"},
    )
    if not api_key:
        raise credentials_exception
    key = ApiKeyRepository(db).authenticate(api_key)
    if key is None:
        raise credentials_exception
    user = UserRepository(db).get(key.user_id)
    if user is None or not user.is_active:
        raise credentials_exception
    return require_role(user, UserRole.JOB_APPLICANT)
