from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas import LoginRequest, TokenWithUser, UserCreate, UserRead
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenWithUser, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> TokenWithUser:
    service = AuthService(db)
    user = service.register(
        email=payload.email, full_name=payload.full_name, password=payload.password
    )
    return TokenWithUser(access_token=service.issue_token(user), user=user)


@router.post("/login", response_model=TokenWithUser)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenWithUser:
    service = AuthService(db)
    user = service.authenticate(email=payload.email, password=payload.password)
    return TokenWithUser(access_token=service.issue_token(user), user=user)


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
