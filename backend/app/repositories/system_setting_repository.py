import uuid
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as postgresql_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.orm import Session

from app.models.daily_registration_counter import DailyRegistrationCounter
from app.models.system_setting import SystemSetting

DAILY_REGISTRATION_LIMIT_KEY = "daily_registration_limit"
DEFAULT_DAILY_REGISTRATION_LIMIT = 1000
DAILY_REGISTRATION_LIMIT_DESCRIPTION = (
    "Maximum number of public account registrations allowed per UTC day."
)
FAILED_LOGIN_ATTEMPT_LIMIT_KEY = "failed_login_attempt_limit"
DEFAULT_FAILED_LOGIN_ATTEMPT_LIMIT = 3
LOGIN_LOCKOUT_DURATION_MINUTES_KEY = "login_lockout_duration_minutes"
DEFAULT_LOGIN_LOCKOUT_DURATION_MINUTES = 20
LOGIN_LOCKOUT_DURATION_MINUTES_DESCRIPTION = (
    "Minutes an account remains temporarily locked after too many failed "
    "login attempts."
)
FAILED_LOGIN_ATTEMPT_LIMIT_DESCRIPTION = (
    "Consecutive invalid-password attempts allowed before a 20-minute "
    "temporary account lock."
)
PASSWORD_MIN_LENGTH_KEY = "password_min_length"
PASSWORD_MAX_LENGTH_KEY = "password_max_length"
DEFAULT_PASSWORD_MIN_LENGTH = 8
DEFAULT_PASSWORD_MAX_LENGTH = 20
PASSWORD_MIN_LENGTH_DESCRIPTION = "Minimum accepted password character length."
PASSWORD_MAX_LENGTH_DESCRIPTION = "Maximum accepted password character length."


class SystemSettingRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_daily_registration_limit(self) -> int:
        setting = self.db.get(SystemSetting, DAILY_REGISTRATION_LIMIT_KEY)
        if setting is None:
            setting = SystemSetting(
                key=DAILY_REGISTRATION_LIMIT_KEY,
                value=str(DEFAULT_DAILY_REGISTRATION_LIMIT),
                description=DAILY_REGISTRATION_LIMIT_DESCRIPTION,
            )
            self.db.add(setting)
            self.db.flush()
        try:
            return max(1, int(setting.value))
        except ValueError:
            return DEFAULT_DAILY_REGISTRATION_LIMIT

    def get_failed_login_attempt_limit(self) -> int:
        setting = self.db.get(SystemSetting, FAILED_LOGIN_ATTEMPT_LIMIT_KEY)
        if setting is None:
            setting = SystemSetting(
                key=FAILED_LOGIN_ATTEMPT_LIMIT_KEY,
                value=str(DEFAULT_FAILED_LOGIN_ATTEMPT_LIMIT),
                description=FAILED_LOGIN_ATTEMPT_LIMIT_DESCRIPTION,
            )
            self.db.add(setting)
            self.db.flush()
        try:
            return max(1, int(setting.value))
        except ValueError:
            return DEFAULT_FAILED_LOGIN_ATTEMPT_LIMIT

    def get_login_lockout_duration_minutes(self) -> int:
        setting = self.db.get(
            SystemSetting, LOGIN_LOCKOUT_DURATION_MINUTES_KEY
        )
        if setting is None:
            setting = SystemSetting(
                key=LOGIN_LOCKOUT_DURATION_MINUTES_KEY,
                value=str(DEFAULT_LOGIN_LOCKOUT_DURATION_MINUTES),
                description=LOGIN_LOCKOUT_DURATION_MINUTES_DESCRIPTION,
            )
            self.db.add(setting)
            self.db.flush()
        try:
            return max(1, int(setting.value))
        except ValueError:
            return DEFAULT_LOGIN_LOCKOUT_DURATION_MINUTES

    def get_password_length_policy(self) -> tuple[int, int]:
        minimum_setting = self.db.get(SystemSetting, PASSWORD_MIN_LENGTH_KEY)
        if minimum_setting is None:
            minimum_setting = SystemSetting(
                key=PASSWORD_MIN_LENGTH_KEY,
                value=str(DEFAULT_PASSWORD_MIN_LENGTH),
                description=PASSWORD_MIN_LENGTH_DESCRIPTION,
            )
            self.db.add(minimum_setting)

        maximum_setting = self.db.get(SystemSetting, PASSWORD_MAX_LENGTH_KEY)
        if maximum_setting is None:
            maximum_setting = SystemSetting(
                key=PASSWORD_MAX_LENGTH_KEY,
                value=str(DEFAULT_PASSWORD_MAX_LENGTH),
                description=PASSWORD_MAX_LENGTH_DESCRIPTION,
            )
            self.db.add(maximum_setting)
        self.db.flush()

        try:
            minimum = int(minimum_setting.value)
            maximum = int(maximum_setting.value)
        except ValueError:
            return DEFAULT_PASSWORD_MIN_LENGTH, DEFAULT_PASSWORD_MAX_LENGTH
        if not 8 <= minimum <= maximum <= 20:
            return DEFAULT_PASSWORD_MIN_LENGTH, DEFAULT_PASSWORD_MAX_LENGTH
        return minimum, maximum

    def set_daily_registration_limit(
        self, limit: int, updated_by: uuid.UUID
    ) -> SystemSetting:
        setting = self.db.get(SystemSetting, DAILY_REGISTRATION_LIMIT_KEY)
        if setting is None:
            setting = SystemSetting(
                key=DAILY_REGISTRATION_LIMIT_KEY,
                value=str(limit),
                description=DAILY_REGISTRATION_LIMIT_DESCRIPTION,
                updated_by=updated_by,
            )
            self.db.add(setting)
        else:
            setting.value = str(limit)
            setting.updated_by = updated_by
        self.db.commit()
        self.db.refresh(setting)
        return setting

    def set_failed_login_attempt_limit(
        self, limit: int, updated_by: uuid.UUID
    ) -> SystemSetting:
        setting = self.db.get(SystemSetting, FAILED_LOGIN_ATTEMPT_LIMIT_KEY)
        if setting is None:
            setting = SystemSetting(
                key=FAILED_LOGIN_ATTEMPT_LIMIT_KEY,
                value=str(limit),
                description=FAILED_LOGIN_ATTEMPT_LIMIT_DESCRIPTION,
                updated_by=updated_by,
            )
            self.db.add(setting)
        else:
            setting.value = str(limit)
            setting.updated_by = updated_by
        self.db.commit()
        self.db.refresh(setting)
        return setting

    def set_login_lockout_duration_minutes(
        self, minutes: int, updated_by: uuid.UUID
    ) -> SystemSetting:
        setting = self.db.get(
            SystemSetting, LOGIN_LOCKOUT_DURATION_MINUTES_KEY
        )
        if setting is None:
            setting = SystemSetting(
                key=LOGIN_LOCKOUT_DURATION_MINUTES_KEY,
                value=str(minutes),
                description=LOGIN_LOCKOUT_DURATION_MINUTES_DESCRIPTION,
                updated_by=updated_by,
            )
            self.db.add(setting)
        else:
            setting.value = str(minutes)
            setting.updated_by = updated_by
        self.db.commit()
        self.db.refresh(setting)
        return setting

    def set_login_security_settings(
        self,
        *,
        attempt_limit: int,
        lockout_duration_minutes: int,
        updated_by: uuid.UUID,
    ) -> None:
        attempt_setting = self.db.get(
            SystemSetting, FAILED_LOGIN_ATTEMPT_LIMIT_KEY
        )
        if attempt_setting is None:
            attempt_setting = SystemSetting(
                key=FAILED_LOGIN_ATTEMPT_LIMIT_KEY,
                value=str(attempt_limit),
                description=FAILED_LOGIN_ATTEMPT_LIMIT_DESCRIPTION,
            )
            self.db.add(attempt_setting)
        attempt_setting.value = str(attempt_limit)
        attempt_setting.updated_by = updated_by

        duration_setting = self.db.get(
            SystemSetting, LOGIN_LOCKOUT_DURATION_MINUTES_KEY
        )
        if duration_setting is None:
            duration_setting = SystemSetting(
                key=LOGIN_LOCKOUT_DURATION_MINUTES_KEY,
                value=str(lockout_duration_minutes),
                description=LOGIN_LOCKOUT_DURATION_MINUTES_DESCRIPTION,
            )
            self.db.add(duration_setting)
        duration_setting.value = str(lockout_duration_minutes)
        duration_setting.updated_by = updated_by
        self.db.commit()

    def set_password_length_policy(
        self,
        *,
        minimum: int,
        maximum: int,
        updated_by: uuid.UUID,
    ) -> None:
        minimum_setting = self.db.get(SystemSetting, PASSWORD_MIN_LENGTH_KEY)
        if minimum_setting is None:
            minimum_setting = SystemSetting(
                key=PASSWORD_MIN_LENGTH_KEY,
                description=PASSWORD_MIN_LENGTH_DESCRIPTION,
            )
            self.db.add(minimum_setting)
        minimum_setting.value = str(minimum)
        minimum_setting.updated_by = updated_by

        maximum_setting = self.db.get(SystemSetting, PASSWORD_MAX_LENGTH_KEY)
        if maximum_setting is None:
            maximum_setting = SystemSetting(
                key=PASSWORD_MAX_LENGTH_KEY,
                description=PASSWORD_MAX_LENGTH_DESCRIPTION,
            )
            self.db.add(maximum_setting)
        maximum_setting.value = str(maximum)
        maximum_setting.updated_by = updated_by
        self.db.commit()

    def consume_daily_registration_slot(
        self, registration_date: date, limit: int
    ) -> bool:
        table = DailyRegistrationCounter
        dialect_name = self.db.get_bind().dialect.name
        if dialect_name == "postgresql":
            insert = postgresql_insert(table)
        elif dialect_name == "sqlite":
            insert = sqlite_insert(table)
        else:
            counter = self.db.scalar(
                select(table)
                .where(table.registration_date == registration_date)
                .with_for_update()
            )
            if counter is None:
                self.db.add(
                    table(
                        registration_date=registration_date,
                        registration_count=1,
                    )
                )
                self.db.flush()
                return True
            if counter.registration_count >= limit:
                return False
            counter.registration_count += 1
            self.db.flush()
            return True

        statement = (
            insert
            .values(
                registration_date=registration_date,
                registration_count=1,
            )
            .on_conflict_do_update(
                index_elements=[table.registration_date],
                set_={
                    "registration_count": table.registration_count + 1,
                    "updated_at": func.now(),
                },
                where=table.registration_count < limit,
            )
            .returning(table.registration_count)
        )
        return self.db.scalar(statement) is not None

    def registrations_used_on(self, registration_date: date) -> int:
        counter = self.db.get(DailyRegistrationCounter, registration_date)
        return counter.registration_count if counter is not None else 0
