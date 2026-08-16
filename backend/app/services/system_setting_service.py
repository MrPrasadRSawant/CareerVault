import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.html_sanitizer import sanitize_rich_text
from app.models.system_setting import SystemSetting
from app.repositories.system_setting_repository import (
    FAILED_LOGIN_ATTEMPT_LIMIT_KEY,
    LOGIN_LOCKOUT_DURATION_MINUTES_KEY,
    PASSWORD_MAX_LENGTH_KEY,
    PASSWORD_MIN_LENGTH_KEY,
    SystemSettingRepository,
)
from app.schemas.system_setting import (
    LoginSecuritySettingsRead,
    PasswordPolicyAdminRead,
    PasswordPolicyRead,
    RegistrationSettingsRead,
    TermsOfServiceRead,
)


class SystemSettingService:
    def __init__(self, db: Session) -> None:
        self.repository = SystemSettingRepository(db)

    def registration_settings(self) -> RegistrationSettingsRead:
        today = datetime.now(timezone.utc).date()
        limit = self.repository.get_daily_registration_limit()
        setting = self.repository.db.get(
            SystemSetting, "daily_registration_limit"
        )
        assert setting is not None
        used = self.repository.registrations_used_on(today)
        return RegistrationSettingsRead(
            daily_registration_limit=limit,
            registrations_used_today=used,
            registrations_remaining_today=max(0, limit - used),
            counter_date_utc=today,
            updated_at=setting.updated_at,
        )

    def update_daily_registration_limit(
        self, limit: int, updated_by: uuid.UUID
    ) -> RegistrationSettingsRead:
        self.repository.set_daily_registration_limit(limit, updated_by)
        return self.registration_settings()

    def login_security_settings(self) -> LoginSecuritySettingsRead:
        attempt_limit = self.repository.get_failed_login_attempt_limit()
        attempt_setting = self.repository.db.get(
            SystemSetting, FAILED_LOGIN_ATTEMPT_LIMIT_KEY
        )
        duration = self.repository.get_login_lockout_duration_minutes()
        duration_setting = self.repository.db.get(
            SystemSetting, LOGIN_LOCKOUT_DURATION_MINUTES_KEY
        )
        assert attempt_setting is not None
        assert duration_setting is not None
        return LoginSecuritySettingsRead(
            failed_login_attempt_limit=attempt_limit,
            lockout_duration_minutes=duration,
            updated_at=max(
                attempt_setting.updated_at,
                duration_setting.updated_at,
            ),
        )

    def update_login_security_settings(
        self,
        attempt_limit: int,
        lockout_duration_minutes: int,
        updated_by: uuid.UUID,
    ) -> LoginSecuritySettingsRead:
        self.repository.set_login_security_settings(
            attempt_limit=attempt_limit,
            lockout_duration_minutes=lockout_duration_minutes,
            updated_by=updated_by,
        )
        return self.login_security_settings()

    def password_policy(self) -> PasswordPolicyRead:
        minimum, maximum = self.repository.get_password_length_policy()
        return PasswordPolicyRead(
            minimum_length=minimum,
            maximum_length=maximum,
        )

    def password_policy_admin(self) -> PasswordPolicyAdminRead:
        policy = self.password_policy()
        minimum_setting = self.repository.db.get(
            SystemSetting, PASSWORD_MIN_LENGTH_KEY
        )
        maximum_setting = self.repository.db.get(
            SystemSetting, PASSWORD_MAX_LENGTH_KEY
        )
        assert minimum_setting is not None
        assert maximum_setting is not None
        return PasswordPolicyAdminRead(
            **policy.model_dump(),
            updated_at=max(
                minimum_setting.updated_at,
                maximum_setting.updated_at,
            ),
        )

    def update_password_policy(
        self,
        minimum: int,
        maximum: int,
        updated_by: uuid.UUID,
    ) -> PasswordPolicyAdminRead:
        self.repository.set_password_length_policy(
            minimum=minimum,
            maximum=maximum,
            updated_by=updated_by,
        )
        return self.password_policy_admin()

    def terms_of_service(self) -> TermsOfServiceRead:
        content, version, setting = self.repository.get_terms_of_service()
        return TermsOfServiceRead(
            content_html=content,
            version=version,
            updated_at=setting.updated_at,
        )

    def update_terms_of_service(
        self, content_html: str, updated_by: uuid.UUID
    ) -> TermsOfServiceRead:
        sanitized = sanitize_rich_text(content_html)
        if len(sanitized) < 20:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Terms of Service content cannot be empty",
            )
        self.repository.set_terms_of_service(sanitized, updated_by)
        return self.terms_of_service()
