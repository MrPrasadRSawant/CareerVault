import uuid
from datetime import date, datetime, timedelta

from sqlalchemy import case, select, update

from app.models.enums import UserRole
from app.models.user import User
from app.repositories.base import BaseRepository
from app.repositories.system_setting_repository import SystemSettingRepository


class UserRepository(BaseRepository[User]):
    model = User

    def get_by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email))

    def create_with_daily_registration_quota(
        self,
        *,
        email: str,
        full_name: str,
        hashed_password: str,
        registration_date: date,
        daily_limit: int,
    ) -> User | None:
        settings_repo = SystemSettingRepository(self.db)
        if not settings_repo.consume_daily_registration_slot(
            registration_date, daily_limit
        ):
            self.db.rollback()
            return None

        user = User(
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
            role=UserRole.JOB_APPLICANT,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def record_failed_login_attempt(
        self,
        user_id: uuid.UUID,
        *,
        attempt_limit: int,
        lock_minutes: int,
        now: datetime,
    ) -> datetime | None:
        next_attempt = User.failed_login_attempts + 1
        should_lock = next_attempt >= attempt_limit
        lock_expires_at = now + timedelta(minutes=lock_minutes)
        statement = (
            update(User)
            .where(User.id == user_id)
            .values(
                failed_login_attempts=case(
                    (should_lock, 0), else_=next_attempt
                ),
                locked_until=case(
                    (should_lock, lock_expires_at),
                    else_=None,
                ),
            )
            .returning(User.locked_until)
            .execution_options(synchronize_session=False)
        )
        return self.db.scalar(statement)

    def reset_failed_login_attempts(self, user_id: uuid.UUID) -> None:
        self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(failed_login_attempts=0, locked_until=None)
            .execution_options(synchronize_session=False)
        )
        self.db.commit()
