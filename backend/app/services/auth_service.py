import hashlib
import hmac
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.request_context import AuthClientContext
from app.core.security import create_access_token, hash_password, verify_password
from app.models.enums import (
    AuthEventType,
    AuthFailureReason,
    AuthSessionEndReason,
    UserRole,
)
from app.models.user import User
from app.repositories.auth_audit_repository import AuthAuditRepository
from app.repositories.system_setting_repository import (
    SystemSettingRepository,
)
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, db: Session) -> None:
        self.user_repo = UserRepository(db)
        self.audit_repo = AuthAuditRepository(db)
        self.settings_repo = SystemSettingRepository(db)

    @staticmethod
    def _identifier_hash(email: str) -> str:
        return hmac.new(
            settings.SECRET_KEY.encode("utf-8"),
            email.strip().lower().encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    @staticmethod
    def _context(
        client_context: AuthClientContext | None,
    ) -> AuthClientContext:
        return client_context or AuthClientContext(None, None)

    @staticmethod
    def _as_utc(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @staticmethod
    def _temporary_lock_response(locked_until: datetime) -> HTTPException:
        now = datetime.now(timezone.utc)
        retry_after = max(
            1,
            int((AuthService._as_utc(locked_until) - now).total_seconds()),
        )
        remaining_minutes = max(1, (retry_after + 59) // 60)
        return HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail=(
                "This account is temporarily locked after consecutive failed "
                f"login attempts. Please try again in {remaining_minutes} "
                "minutes."
            ),
            headers={"Retry-After": str(retry_after)},
        )

    def register(self, email: str, full_name: str, password: str) -> User:
        minimum, maximum = self.settings_repo.get_password_length_policy()
        if not minimum <= len(password) <= maximum:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=(
                    f"Password must contain between {minimum} and {maximum} "
                    "characters"
                ),
            )
        if self.user_repo.get_by_email(email) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists",
            )
        daily_limit = self.settings_repo.get_daily_registration_limit()
        user = self.user_repo.create_with_daily_registration_quota(
            email=email,
            full_name=full_name,
            hashed_password=hash_password(password),
            registration_date=datetime.now(timezone.utc).date(),
            daily_limit=daily_limit,
        )
        if user is None:
            now = datetime.now(timezone.utc)
            tomorrow = datetime.combine(
                now.date(), datetime.min.time(), tzinfo=timezone.utc
            ) + timedelta(days=1)
            retry_after = max(1, int((tomorrow - now).total_seconds()))
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=(
                    "Today's account registration limit has been reached. "
                    "Please try again after 00:00 UTC."
                ),
                headers={"Retry-After": str(retry_after)},
            )
        return user

    def authenticate(
        self,
        email: str,
        password: str,
        required_role: UserRole | None = None,
        client_context: AuthClientContext | None = None,
    ) -> User:
        context = self._context(client_context)
        identifier_hash = self._identifier_hash(email)
        user = self.user_repo.get_by_email(email)
        now = datetime.now(timezone.utc)
        if (
            user is not None
            and user.locked_until is not None
            and self._as_utc(user.locked_until) > now
        ):
            self.audit_repo.record_failure(
                user=user,
                identifier_hash=identifier_hash,
                reason=AuthFailureReason.TEMPORARILY_LOCKED,
                http_status=status.HTTP_423_LOCKED,
                ip_address=context.ip_address,
                user_agent=context.user_agent,
            )
            raise self._temporary_lock_response(user.locked_until)

        minimum, maximum = self.settings_repo.get_password_length_policy()
        password_length_allowed = minimum <= len(password) <= maximum
        if (
            user is None
            or not password_length_allowed
            or not verify_password(password, user.hashed_password)
        ):
            newly_locked_until = None
            failure_reason = AuthFailureReason.INVALID_CREDENTIALS
            http_status = status.HTTP_401_UNAUTHORIZED
            if user is not None:
                newly_locked_until = self.user_repo.record_failed_login_attempt(
                    user.id,
                    attempt_limit=(
                        self.settings_repo.get_failed_login_attempt_limit()
                    ),
                    lock_minutes=(
                        self.settings_repo.get_login_lockout_duration_minutes()
                    ),
                    now=now,
                )
                if (
                    newly_locked_until is not None
                    and self._as_utc(newly_locked_until) > now
                ):
                    failure_reason = AuthFailureReason.TEMPORARILY_LOCKED
                    http_status = status.HTTP_423_LOCKED
            self.audit_repo.record_failure(
                user=user,
                identifier_hash=identifier_hash,
                reason=failure_reason,
                http_status=http_status,
                ip_address=context.ip_address,
                user_agent=context.user_agent,
            )
            if newly_locked_until is not None:
                raise self._temporary_lock_response(newly_locked_until)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if required_role is not None and user.role != required_role:
            self.audit_repo.record_failure(
                user=user,
                identifier_hash=identifier_hash,
                reason=AuthFailureReason.ROLE_NOT_ALLOWED,
                http_status=status.HTTP_401_UNAUTHORIZED,
                ip_address=context.ip_address,
                user_agent=context.user_agent,
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            self.audit_repo.record_failure(
                user=user,
                identifier_hash=identifier_hash,
                reason=AuthFailureReason.ACCOUNT_BLOCKED,
                http_status=status.HTTP_403_FORBIDDEN,
                ip_address=context.ip_address,
                user_agent=context.user_agent,
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This account has been deactivated",
            )
        self.user_repo.reset_failed_login_attempts(user.id)
        return user

    def issue_token(
        self,
        user: User,
        *,
        email: str | None = None,
        client_context: AuthClientContext | None = None,
        auth_method: AuthEventType = AuthEventType.LOGIN,
    ) -> str:
        context = self._context(client_context)
        auth_session = self.audit_repo.start_session(
            user=user,
            identifier_hash=self._identifier_hash(email or user.email),
            auth_method=auth_method,
            ip_address=context.ip_address,
            user_agent=context.user_agent,
        )
        return create_access_token(
            subject=user.id,
            additional_claims={"sid": str(auth_session.id)},
        )

    def logout(self, session_id: uuid.UUID, user_id: uuid.UUID) -> None:
        self.audit_repo.close_session(
            session_id,
            user_id,
            AuthSessionEndReason.LOGOUT,
        )
