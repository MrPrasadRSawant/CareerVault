import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, func, or_, select, update
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.auth_session import AuthSession
from app.models.enums import (
    AuthEventType,
    AuthFailureReason,
    AuthOutcome,
    AuthSessionEndReason,
    UserRole,
)
from app.models.login_audit_log import LoginAuditLog
from app.models.user import User


class AuthAuditRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def purge_expired_records(self, now: datetime) -> None:
        cutoff = now - timedelta(days=settings.AUTH_AUDIT_RETENTION_DAYS)
        self.db.execute(
            delete(LoginAuditLog).where(LoginAuditLog.occurred_at < cutoff)
        )
        self.db.execute(
            delete(AuthSession).where(
                AuthSession.started_at < cutoff,
                or_(
                    AuthSession.ended_at.is_not(None),
                    AuthSession.expires_at < now,
                ),
            )
        )

    def record_failure(
        self,
        *,
        user: User | None,
        identifier_hash: str,
        reason: AuthFailureReason,
        http_status: int,
        ip_address: str | None,
        user_agent: str | None,
    ) -> LoginAuditLog:
        now = datetime.now(timezone.utc)
        self.purge_expired_records(now)
        event = LoginAuditLog(
            user_id=user.id if user else None,
            event_type=AuthEventType.LOGIN,
            outcome=AuthOutcome.FAILURE,
            failure_reason=reason,
            role=user.role if user else None,
            identifier_hash=identifier_hash,
            occurred_at=now,
            ip_address=ip_address,
            user_agent=user_agent,
            http_status=http_status,
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def start_session(
        self,
        *,
        user: User,
        identifier_hash: str,
        auth_method: AuthEventType,
        ip_address: str | None,
        user_agent: str | None,
    ) -> AuthSession:
        now = datetime.now(timezone.utc)
        self.purge_expired_records(now)
        auth_session = AuthSession(
            user_id=user.id,
            auth_method=auth_method,
            started_at=now,
            last_seen_at=now,
            expires_at=now
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.db.add(auth_session)
        self.db.flush()
        self.db.add(
            LoginAuditLog(
                user_id=user.id,
                auth_session_id=auth_session.id,
                event_type=auth_method,
                outcome=AuthOutcome.SUCCESS,
                role=user.role,
                identifier_hash=identifier_hash,
                occurred_at=now,
                ip_address=ip_address,
                user_agent=user_agent,
                http_status=200 if auth_method == AuthEventType.LOGIN else 201,
            )
        )
        self.db.commit()
        self.db.refresh(auth_session)
        return auth_session

    def validate_and_touch_session(
        self, session_id: uuid.UUID, user_id: uuid.UUID
    ) -> bool:
        now = datetime.now(timezone.utc)
        auth_session = self.db.scalar(
            select(AuthSession).where(
                AuthSession.id == session_id,
                AuthSession.user_id == user_id,
                AuthSession.ended_at.is_(None),
                AuthSession.expires_at > now,
            )
        )
        if auth_session is None:
            return False
        update_before = now - timedelta(
            seconds=settings.AUTH_SESSION_ACTIVITY_UPDATE_SECONDS
        )
        self.db.execute(
            update(AuthSession)
            .where(
                AuthSession.id == session_id,
                AuthSession.last_seen_at < update_before,
            )
            .values(last_seen_at=now)
            .execution_options(synchronize_session=False)
        )
        self.db.commit()
        return True

    def close_session(
        self,
        session_id: uuid.UUID,
        user_id: uuid.UUID,
        reason: AuthSessionEndReason,
    ) -> None:
        now = datetime.now(timezone.utc)
        self.db.execute(
            update(AuthSession)
            .where(
                AuthSession.id == session_id,
                AuthSession.user_id == user_id,
                AuthSession.ended_at.is_(None),
            )
            .values(ended_at=now, last_seen_at=now, end_reason=reason)
            .execution_options(synchronize_session=False)
        )
        self.db.commit()

    def close_user_sessions(
        self, user_id: uuid.UUID, reason: AuthSessionEndReason
    ) -> None:
        now = datetime.now(timezone.utc)
        self.db.execute(
            update(AuthSession)
            .where(
                AuthSession.user_id == user_id,
                AuthSession.ended_at.is_(None),
            )
            .values(ended_at=now, last_seen_at=now, end_reason=reason)
            .execution_options(synchronize_session=False)
        )
        self.db.commit()

    def count_login_events(
        self,
        *,
        outcome: AuthOutcome | None = None,
        occurred_since: datetime | None = None,
    ) -> int:
        filters = [LoginAuditLog.event_type == AuthEventType.LOGIN]
        if outcome is not None:
            filters.append(LoginAuditLog.outcome == outcome)
        if occurred_since is not None:
            filters.append(LoginAuditLog.occurred_at >= occurred_since)
        return (
            self.db.scalar(
                select(func.count())
                .select_from(LoginAuditLog)
                .where(*filters)
            )
            or 0
        )

    def count_active_sessions(self, now: datetime) -> int:
        return (
            self.db.scalar(
                select(func.count())
                .select_from(AuthSession)
                .where(
                    AuthSession.ended_at.is_(None),
                    AuthSession.expires_at > now,
                )
            )
            or 0
        )

    def list_login_events(
        self,
        *,
        search: str | None,
        outcome: AuthOutcome | None,
        role: UserRole | None,
        limit: int,
        offset: int,
    ) -> tuple[list[tuple[LoginAuditLog, User | None]], int]:
        filters = []
        if search:
            pattern = f"%{search.strip()}%"
            filters.append(
                or_(User.full_name.ilike(pattern), User.email.ilike(pattern))
            )
        if outcome is not None:
            filters.append(LoginAuditLog.outcome == outcome)
        if role is not None:
            filters.append(LoginAuditLog.role == role)
        base = (
            select(LoginAuditLog, User)
            .outerjoin(User, LoginAuditLog.user_id == User.id)
            .where(*filters)
        )
        total = (
            self.db.scalar(
                select(func.count())
                .select_from(base.order_by(None).subquery())
            )
            or 0
        )
        rows = self.db.execute(
            base.order_by(LoginAuditLog.occurred_at.desc())
            .limit(limit)
            .offset(offset)
        ).all()
        return [(row[0], row[1]) for row in rows], total

    def list_sessions(
        self,
        *,
        search: str | None,
        role: UserRole | None,
        limit: int,
        offset: int,
    ) -> tuple[list[tuple[AuthSession, User]], int]:
        filters = []
        if search:
            pattern = f"%{search.strip()}%"
            filters.append(
                or_(User.full_name.ilike(pattern), User.email.ilike(pattern))
            )
        if role is not None:
            filters.append(User.role == role)
        base = (
            select(AuthSession, User)
            .join(User, AuthSession.user_id == User.id)
            .where(*filters)
        )
        total = (
            self.db.scalar(
                select(func.count())
                .select_from(base.order_by(None).subquery())
            )
            or 0
        )
        rows = self.db.execute(
            base.order_by(AuthSession.started_at.desc())
            .limit(limit)
            .offset(offset)
        ).all()
        return [(row[0], row[1]) for row in rows], total
