import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.exception_log import ExceptionLog
from app.models.user import User
from app.repositories.exception_log_repository import ExceptionLogRepository
from app.schemas.admin_exception import (
    AdminExceptionLogDetail,
    AdminExceptionLogPage,
    AdminExceptionLogRead,
    AdminExceptionOverviewRead,
)


class AdminExceptionService:
    def __init__(self, db: Session) -> None:
        self.repository = ExceptionLogRepository(db)

    @staticmethod
    def _read(entry: ExceptionLog, user: User | None) -> AdminExceptionLogRead:
        return AdminExceptionLogRead(
            id=entry.id,
            request_id=entry.request_id,
            user_id=entry.user_id,
            user_name=user.full_name if user else None,
            user_email=user.email if user else None,
            occurred_at=entry.occurred_at,
            method=entry.method,
            route_template=entry.route_template,
            query_parameter_names=(
                [name.strip() for name in entry.query_parameter_names.split(",")]
                if entry.query_parameter_names
                else []
            ),
            status_code=entry.status_code,
            exception_type=entry.exception_type,
            message=entry.message,
            fingerprint=entry.fingerprint,
            ip_address=entry.ip_address,
            user_agent=entry.user_agent,
            app_environment=entry.app_environment,
            is_handled=entry.is_handled,
        )

    def overview(self) -> AdminExceptionOverviewRead:
        last_day, last_week, unique = self.repository.overview(
            datetime.now(timezone.utc)
        )
        return AdminExceptionOverviewRead(
            exceptions_last_24_hours=last_day,
            exceptions_last_7_days=last_week,
            unique_fingerprints_last_24_hours=unique,
            retention_days=settings.EXCEPTION_LOG_RETENTION_DAYS,
        )

    def list_logs(
        self,
        *,
        search: str | None,
        status_code: int | None,
        limit: int,
        offset: int,
    ) -> AdminExceptionLogPage:
        rows, total = self.repository.list_logs(
            search=search,
            status_code=status_code,
            limit=limit,
            offset=offset,
        )
        return AdminExceptionLogPage(
            items=[self._read(entry, user) for entry, user in rows],
            total=total,
            limit=limit,
            offset=offset,
        )

    def detail(self, exception_id: uuid.UUID) -> AdminExceptionLogDetail:
        row = self.repository.get_with_user(exception_id)
        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exception log not found",
            )
        entry, user = row
        return AdminExceptionLogDetail(
            **self._read(entry, user).model_dump(),
            traceback=entry.traceback,
        )
