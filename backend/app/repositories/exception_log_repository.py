import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, func, or_, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.exception_log import ExceptionLog
from app.models.user import User


class ExceptionLogRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def record(self, **values) -> ExceptionLog:
        cutoff = datetime.now(timezone.utc) - timedelta(
            days=settings.EXCEPTION_LOG_RETENTION_DAYS
        )
        self.db.execute(
            delete(ExceptionLog).where(ExceptionLog.occurred_at < cutoff)
        )
        entry = ExceptionLog(**values)
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def get_with_user(
        self, exception_id: uuid.UUID
    ) -> tuple[ExceptionLog, User | None] | None:
        row = self.db.execute(
            select(ExceptionLog, User)
            .outerjoin(User, ExceptionLog.user_id == User.id)
            .where(ExceptionLog.id == exception_id)
        ).one_or_none()
        return (row[0], row[1]) if row is not None else None

    def list_logs(
        self,
        *,
        search: str | None,
        status_code: int | None,
        limit: int,
        offset: int,
    ) -> tuple[list[tuple[ExceptionLog, User | None]], int]:
        filters = []
        if search:
            pattern = f"%{search.strip()}%"
            filters.append(
                or_(
                    ExceptionLog.request_id.ilike(pattern),
                    ExceptionLog.exception_type.ilike(pattern),
                    ExceptionLog.message.ilike(pattern),
                    ExceptionLog.route_template.ilike(pattern),
                    ExceptionLog.fingerprint.ilike(pattern),
                    User.full_name.ilike(pattern),
                    User.email.ilike(pattern),
                )
            )
        if status_code is not None:
            filters.append(ExceptionLog.status_code == status_code)
        base = (
            select(ExceptionLog, User)
            .outerjoin(User, ExceptionLog.user_id == User.id)
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
            base.order_by(ExceptionLog.occurred_at.desc())
            .limit(limit)
            .offset(offset)
        ).all()
        return [(row[0], row[1]) for row in rows], total

    def overview(self, now: datetime) -> tuple[int, int, int]:
        last_day = now - timedelta(hours=24)
        last_week = now - timedelta(days=7)
        last_24_hours = (
            self.db.scalar(
                select(func.count())
                .select_from(ExceptionLog)
                .where(ExceptionLog.occurred_at >= last_day)
            )
            or 0
        )
        last_7_days = (
            self.db.scalar(
                select(func.count())
                .select_from(ExceptionLog)
                .where(ExceptionLog.occurred_at >= last_week)
            )
            or 0
        )
        unique_last_24_hours = (
            self.db.scalar(
                select(func.count(func.distinct(ExceptionLog.fingerprint))).where(
                    ExceptionLog.occurred_at >= last_day
                )
            )
            or 0
        )
        return last_24_hours, last_7_days, unique_last_24_hours
