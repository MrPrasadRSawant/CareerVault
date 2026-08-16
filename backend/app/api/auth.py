import uuid

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.security import HTTPAuthorizationCredentials
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.api.deps import bearer_scheme, get_authenticated_user, get_current_user
from app.core.database import get_db
from app.core.request_context import auth_client_context
from app.core.security import decode_access_token
from app.models.enums import AuthEventType
from app.models.user import User
from app.schemas import LoginRequest, TokenWithUser, UserCreate, UserRead
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenWithUser, status_code=201)
def register(
    payload: UserCreate,
    request: Request,
    db: Session = Depends(get_db),
) -> TokenWithUser:
    service = AuthService(db)
    user = service.register(
        email=payload.email, full_name=payload.full_name, password=payload.password
    )
    return TokenWithUser(
        access_token=service.issue_token(
            user,
            email=payload.email,
            client_context=auth_client_context(request),
            auth_method=AuthEventType.REGISTRATION,
        ),
        user=user,
    )


@router.post("/login", response_model=TokenWithUser)
def login(
    payload: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> TokenWithUser:
    service = AuthService(db)
    context = auth_client_context(request)
    user = service.authenticate(
        email=payload.email,
        password=payload.password,
        client_context=context,
    )
    return TokenWithUser(
        access_token=service.issue_token(
            user,
            email=payload.email,
            client_context=context,
        ),
        user=user,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    current_user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
) -> None:
    if credentials is None:
        return
    try:
        payload = decode_access_token(credentials.credentials)
        session_id = uuid.UUID(str(payload.get("sid")))
    except (InvalidTokenError, TypeError, ValueError):
        return
    AuthService(db).logout(session_id, current_user.id)
    response.status_code = status.HTTP_204_NO_CONTENT


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
