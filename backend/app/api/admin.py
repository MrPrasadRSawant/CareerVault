import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_system_admin
from app.core.database import get_db
from app.models.enums import AuthOutcome, UserRole
from app.models.user import User
from app.schemas.admin import (
    AdminOverviewRead,
    AdminUserPage,
    AdminUserRead,
    AdminUserStatusUpdate,
)
from app.schemas.user import UserRead
from app.schemas.admin_security import (
    AdminAuthSessionPage,
    AdminLoginEventPage,
    AdminSecurityOverviewRead,
)
from app.services.admin_security_service import AdminSecurityService
from app.services.admin_service import AdminService
from app.schemas.system_setting import (
    LoginSecuritySettingsRead,
    LoginSecuritySettingsUpdate,
    RegistrationSettingsRead,
    RegistrationSettingsUpdate,
)
from app.services.system_setting_service import SystemSettingService

router = APIRouter(prefix="/admin", tags=["system-admin"])


@router.get("/auth/me", response_model=UserRead)
def admin_me(current_admin: User = Depends(get_current_system_admin)) -> User:
    return current_admin


@router.get("/overview", response_model=AdminOverviewRead)
def overview(
    db: Session = Depends(get_db),
    _current_admin: User = Depends(get_current_system_admin),
) -> AdminOverviewRead:
    return AdminService(db).overview()


@router.get(
    "/settings/registration",
    response_model=RegistrationSettingsRead,
)
def registration_settings(
    db: Session = Depends(get_db),
    _current_admin: User = Depends(get_current_system_admin),
) -> RegistrationSettingsRead:
    return SystemSettingService(db).registration_settings()


@router.patch(
    "/settings/registration",
    response_model=RegistrationSettingsRead,
)
def update_registration_settings(
    payload: RegistrationSettingsUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_system_admin),
) -> RegistrationSettingsRead:
    return SystemSettingService(db).update_daily_registration_limit(
        payload.daily_registration_limit,
        current_admin.id,
    )


@router.get(
    "/settings/login-security",
    response_model=LoginSecuritySettingsRead,
)
def login_security_settings(
    db: Session = Depends(get_db),
    _current_admin: User = Depends(get_current_system_admin),
) -> LoginSecuritySettingsRead:
    return SystemSettingService(db).login_security_settings()


@router.patch(
    "/settings/login-security",
    response_model=LoginSecuritySettingsRead,
)
def update_login_security_settings(
    payload: LoginSecuritySettingsUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_system_admin),
) -> LoginSecuritySettingsRead:
    return SystemSettingService(db).update_login_security_settings(
        payload.failed_login_attempt_limit,
        payload.lockout_duration_minutes,
        current_admin.id,
    )


@router.get("/security/overview", response_model=AdminSecurityOverviewRead)
def security_overview(
    db: Session = Depends(get_db),
    _current_admin: User = Depends(get_current_system_admin),
) -> AdminSecurityOverviewRead:
    return AdminSecurityService(db).overview()


@router.get("/security/login-events", response_model=AdminLoginEventPage)
def login_events(
    search: str | None = Query(default=None, max_length=255),
    outcome: AuthOutcome | None = None,
    role: UserRole | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    _current_admin: User = Depends(get_current_system_admin),
) -> AdminLoginEventPage:
    return AdminSecurityService(db).login_events(
        search=search,
        outcome=outcome,
        role=role,
        limit=limit,
        offset=offset,
    )


@router.get("/security/sessions", response_model=AdminAuthSessionPage)
def auth_sessions(
    search: str | None = Query(default=None, max_length=255),
    role: UserRole | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    _current_admin: User = Depends(get_current_system_admin),
) -> AdminAuthSessionPage:
    return AdminSecurityService(db).sessions(
        search=search,
        role=role,
        limit=limit,
        offset=offset,
    )


@router.get("/users", response_model=AdminUserPage)
def list_users(
    search: str | None = Query(default=None, max_length=255),
    is_active: bool | None = None,
    role: UserRole | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    _current_admin: User = Depends(get_current_system_admin),
) -> AdminUserPage:
    return AdminService(db).list_users(
        search=search,
        is_active=is_active,
        role=role,
        limit=limit,
        offset=offset,
    )


@router.get("/users/{user_id}", response_model=AdminUserRead)
def read_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    _current_admin: User = Depends(get_current_system_admin),
) -> AdminUserRead:
    return AdminService(db).get_user(user_id)


@router.patch("/users/{user_id}/status", response_model=AdminUserRead)
def update_user_status(
    user_id: uuid.UUID,
    payload: AdminUserStatusUpdate,
    db: Session = Depends(get_db),
    _current_admin: User = Depends(get_current_system_admin),
) -> AdminUserRead:
    return AdminService(db).set_user_active(user_id, is_active=payload.is_active)
