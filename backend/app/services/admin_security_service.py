from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.auth_session import AuthSession
from app.models.enums import AuthOutcome, UserRole
from app.models.login_audit_log import LoginAuditLog
from app.models.user import User
from app.repositories.auth_audit_repository import AuthAuditRepository
from app.schemas.admin_security import (
    AdminAuthSessionPage,
    AdminAuthSessionRead,
    AdminLoginEventPage,
    AdminLoginEventRead,
    AdminSecurityOverviewRead,
)


class AdminSecurityService:
    def __init__(self, db: Session) -> None:
        self.repository = AuthAuditRepository(db)

    @staticmethod
    def _utc(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @staticmethod
    def _login_event(
        event: LoginAuditLog, user: User | None
    ) -> AdminLoginEventRead:
        return AdminLoginEventRead(
            id=event.id,
            user_id=user.id if user else None,
            user_name=user.full_name if user else None,
            user_email=user.email if user else None,
            role=event.role,
            account_known=user is not None,
            unknown_account_reference=(
                None if user else event.identifier_hash[:12]
            ),
            event_type=event.event_type,
            outcome=event.outcome,
            failure_reason=event.failure_reason,
            occurred_at=event.occurred_at,
            ip_address=event.ip_address,
            user_agent=event.user_agent,
            http_status=event.http_status,
        )

    def _auth_session(
        self, auth_session: AuthSession, user: User
    ) -> AdminAuthSessionRead:
        now = datetime.now(timezone.utc)
        started_at = self._utc(auth_session.started_at)
        last_seen_at = self._utc(auth_session.last_seen_at)
        expires_at = self._utc(auth_session.expires_at)
        ended_at = (
            self._utc(auth_session.ended_at)
            if auth_session.ended_at is not None
            else None
        )
        if ended_at is not None:
            session_status = "ended"
            duration_end = ended_at
            duration_basis = "exact"
        elif expires_at <= now:
            session_status = "expired"
            duration_end = last_seen_at
            duration_basis = "estimated_last_activity"
        else:
            session_status = "active"
            duration_end = now
            duration_basis = "ongoing"
        return AdminAuthSessionRead(
            user_id=user.id,
            user_name=user.full_name,
            user_email=user.email,
            role=user.role,
            auth_method=auth_session.auth_method,
            started_at=started_at,
            last_seen_at=last_seen_at,
            ended_at=ended_at,
            expires_at=expires_at,
            status=session_status,
            duration_seconds=max(
                0, int((duration_end - started_at).total_seconds())
            ),
            duration_basis=duration_basis,
            end_reason=auth_session.end_reason,
            ip_address=auth_session.ip_address,
            user_agent=auth_session.user_agent,
        )

    def overview(self) -> AdminSecurityOverviewRead:
        now = datetime.now(timezone.utc)
        last_24_hours = now - timedelta(hours=24)
        return AdminSecurityOverviewRead(
            successful_logins_last_24_hours=self.repository.count_login_events(
                outcome=AuthOutcome.SUCCESS,
                occurred_since=last_24_hours,
            ),
            failed_logins_last_24_hours=self.repository.count_login_events(
                outcome=AuthOutcome.FAILURE,
                occurred_since=last_24_hours,
            ),
            active_sessions=self.repository.count_active_sessions(now),
            retention_days=settings.AUTH_AUDIT_RETENTION_DAYS,
        )

    def login_events(
        self,
        *,
        search: str | None,
        outcome: AuthOutcome | None,
        role: UserRole | None,
        limit: int,
        offset: int,
    ) -> AdminLoginEventPage:
        rows, total = self.repository.list_login_events(
            search=search,
            outcome=outcome,
            role=role,
            limit=limit,
            offset=offset,
        )
        return AdminLoginEventPage(
            items=[self._login_event(event, user) for event, user in rows],
            total=total,
            limit=limit,
            offset=offset,
        )

    def sessions(
        self,
        *,
        search: str | None,
        role: UserRole | None,
        limit: int,
        offset: int,
    ) -> AdminAuthSessionPage:
        rows, total = self.repository.list_sessions(
            search=search,
            role=role,
            limit=limit,
            offset=offset,
        )
        return AdminAuthSessionPage(
            items=[
                self._auth_session(auth_session, user)
                for auth_session, user in rows
            ],
            total=total,
            limit=limit,
            offset=offset,
        )
