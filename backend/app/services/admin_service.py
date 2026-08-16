import uuid
from collections import Counter
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enums import UserRole
from app.models.enums import AuthSessionEndReason
from app.models.user import User
from app.repositories.admin_repository import AdminRepository
from app.repositories.auth_audit_repository import AuthAuditRepository
from app.schemas.admin import (
    AdminOverviewRead,
    AdminRegistrationPeriodRead,
    AdminRoleCountRead,
    AdminUserPage,
    AdminUserRead,
)


class AdminService:
    def __init__(self, db: Session) -> None:
        self.repository = AdminRepository(db)
        self.auth_audit_repository = AuthAuditRepository(db)

    @staticmethod
    def _serialize_user(user: User) -> AdminUserRead:
        return AdminUserRead.model_validate(user)

    @staticmethod
    def _month_start(now: datetime, months_ago: int) -> datetime:
        month_index = now.year * 12 + now.month - 1 - months_ago
        return datetime(
            month_index // 12,
            month_index % 12 + 1,
            1,
            tzinfo=timezone.utc,
        )

    @staticmethod
    def _period(
        period: str,
        counts: Counter[tuple[str, UserRole]],
    ) -> AdminRegistrationPeriodRead:
        return AdminRegistrationPeriodRead(
            period=period,
            role_counts=[
                AdminRoleCountRead(
                    role=role,
                    count=counts[(period, role)],
                )
                for role in UserRole
            ],
        )

    def overview(self) -> AdminOverviewRead:
        now = datetime.now(timezone.utc)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        last_7_days_start = today_start - timedelta(days=6)
        last_30_days_start = today_start - timedelta(days=29)
        yearly_start = datetime(now.year - 4, 1, 1, tzinfo=timezone.utc)
        registrations = [
            (
                registered_at.replace(tzinfo=timezone.utc)
                if registered_at.tzinfo is None
                else registered_at.astimezone(timezone.utc),
                role,
            )
            for registered_at, role in self.repository.registrations_since(
                yearly_start
            )
        ]
        daily_counts = Counter(
            (registered_at.date().isoformat(), role)
            for registered_at, role in registrations
            if registered_at >= last_7_days_start
        )
        monthly_counts = Counter(
            (registered_at.strftime("%Y-%m"), role)
            for registered_at, role in registrations
            if registered_at >= self._month_start(now, 5)
        )
        yearly_counts = Counter(
            (str(registered_at.year), role)
            for registered_at, role in registrations
        )
        daily_periods = [
            (last_7_days_start + timedelta(days=day)).date().isoformat()
            for day in range(7)
        ]
        monthly_periods = [
            self._month_start(now, months_ago).strftime("%Y-%m")
            for months_ago in reversed(range(6))
        ]
        yearly_periods = [str(year) for year in range(now.year - 4, now.year + 1)]
        recent_users, _ = self.repository.list_users(limit=6)
        total = self.repository.count_users()
        active = self.repository.count_users(is_active=True)

        return AdminOverviewRead(
            total_users=total,
            active_users=active,
            blocked_users=total - active,
            registrations_today=sum(
                daily_counts[(now.date().isoformat(), role)] for role in UserRole
            ),
            new_users_last_7_days=self.repository.count_users(
                created_since=last_7_days_start
            ),
            new_users_last_30_days=self.repository.count_users(
                created_since=last_30_days_start
            ),
            role_counts=[
                AdminRoleCountRead(
                    role=role,
                    count=self.repository.count_users(role=role),
                )
                for role in UserRole
            ],
            registrations_by_day=[
                self._period(period, daily_counts) for period in daily_periods
            ],
            registrations_by_month=[
                self._period(period, monthly_counts) for period in monthly_periods
            ],
            registrations_by_year=[
                self._period(period, yearly_counts) for period in yearly_periods
            ],
            recent_users=[self._serialize_user(user) for user in recent_users],
        )

    def list_users(
        self,
        *,
        search: str | None,
        is_active: bool | None,
        role: UserRole | None,
        limit: int,
        offset: int,
    ) -> AdminUserPage:
        users, total = self.repository.list_users(
            search=search,
            is_active=is_active,
            role=role,
            limit=limit,
            offset=offset,
        )
        return AdminUserPage(
            items=[self._serialize_user(user) for user in users],
            total=total,
            limit=limit,
            offset=offset,
        )

    def get_user(self, user_id: uuid.UUID) -> AdminUserRead:
        user = self.repository.get_user(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return self._serialize_user(user)

    def set_user_active(
        self, user_id: uuid.UUID, *, is_active: bool
    ) -> AdminUserRead:
        user = self.repository.get_user(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        if user.role == UserRole.SYSTEM_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="System administrator accounts cannot be blocked",
            )
        if not is_active:
            self.auth_audit_repository.close_user_sessions(
                user.id, AuthSessionEndReason.ACCOUNT_BLOCKED
            )
        return self._serialize_user(
            self.repository.set_user_active(user, is_active)
        )
