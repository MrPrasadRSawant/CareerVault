from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.core.security import hash_password
from app.models.enums import AuthEventType, AuthFailureReason, AuthOutcome, UserRole
from app.models.login_audit_log import LoginAuditLog
from app.repositories.user_repository import UserRepository


ADMIN_EMAIL = "security-owner@example.com"
ADMIN_PASSWORD = "admin-password-123"
USER_EMAIL = "lockout-user@example.com"
USER_PASSWORD = "password123"


def register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": USER_EMAIL,
            "full_name": "Lockout User",
            "password": USER_PASSWORD,
            "terms_accepted": True,
            "terms_version": 1,
        },
    )
    assert response.status_code == 201


def login(client, password: str = USER_PASSWORD):
    return client.post(
        "/api/v1/auth/login",
        json={"email": USER_EMAIL, "password": password},
    )


def admin_headers(client, db_session):
    UserRepository(db_session).create(
        email=ADMIN_EMAIL,
        full_name="Security Owner",
        hashed_password=hash_password(ADMIN_PASSWORD),
        is_active=True,
        role=UserRole.SYSTEM_ADMIN,
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_every_attempt_is_appended_and_third_failure_locks_account(
    client, db_session
):
    register_user(client)

    assert login(client, "wrong-one").status_code == 401
    assert login(client, "wrong-two").status_code == 401
    third = login(client, "wrong-three")
    assert third.status_code == 423
    assert int(third.headers["retry-after"]) > 0

    locked_attempt = login(client)
    assert locked_attempt.status_code == 423

    user = UserRepository(db_session).get_by_email(USER_EMAIL)
    db_session.refresh(user)
    assert user.failed_login_attempts == 0
    assert user.locked_until is not None
    lock_duration = (
        user.locked_until.replace(tzinfo=timezone.utc)
        if user.locked_until.tzinfo is None
        else user.locked_until.astimezone(timezone.utc)
    ) - datetime.now(timezone.utc)
    assert timedelta(minutes=19) < lock_duration <= timedelta(minutes=20)

    events = list(
        db_session.scalars(
            select(LoginAuditLog).where(
                LoginAuditLog.user_id == user.id,
                LoginAuditLog.event_type == AuthEventType.LOGIN,
            )
        )
    )
    assert len(events) == 4
    assert sum(
        event.failure_reason == AuthFailureReason.INVALID_CREDENTIALS
        for event in events
    ) == 2
    assert sum(
        event.failure_reason == AuthFailureReason.TEMPORARILY_LOCKED
        for event in events
    ) == 2


def test_expired_lock_allows_login_and_success_resets_failures(client, db_session):
    register_user(client)
    for password in ("wrong-one", "wrong-two", "wrong-three"):
        login(client, password)

    user = UserRepository(db_session).get_by_email(USER_EMAIL)
    user.locked_until = datetime.now(timezone.utc) - timedelta(seconds=1)
    user.failed_login_attempts = 2
    db_session.commit()

    successful = login(client)
    assert successful.status_code == 200
    db_session.refresh(user)
    assert user.failed_login_attempts == 0
    assert user.locked_until is None

    events = list(
        db_session.scalars(
            select(LoginAuditLog).where(
                LoginAuditLog.user_id == user.id,
                LoginAuditLog.event_type == AuthEventType.LOGIN,
            )
        )
    )
    assert len(events) == 4
    assert sum(event.outcome == AuthOutcome.SUCCESS for event in events) == 1


def test_success_breaks_the_consecutive_failure_sequence(client, db_session):
    register_user(client)
    assert login(client, "wrong-one").status_code == 401
    assert login(client).status_code == 200
    assert login(client, "wrong-two").status_code == 401
    assert login(client, "wrong-three").status_code == 401

    user = UserRepository(db_session).get_by_email(USER_EMAIL)
    db_session.refresh(user)
    assert user.failed_login_attempts == 2
    assert user.locked_until is None


def test_admin_can_edit_failed_attempt_limit(client, db_session):
    headers = admin_headers(client, db_session)
    defaults = client.get(
        "/api/v1/admin/settings/login-security", headers=headers
    )
    assert defaults.status_code == 200
    assert defaults.json()["failed_login_attempt_limit"] == 3
    assert defaults.json()["lockout_duration_minutes"] == 20

    update = client.patch(
        "/api/v1/admin/settings/login-security",
        headers=headers,
        json={
            "failed_login_attempt_limit": 2,
            "lockout_duration_minutes": 5,
        },
    )
    assert update.status_code == 200
    assert update.json()["failed_login_attempt_limit"] == 2
    assert update.json()["lockout_duration_minutes"] == 5

    register_user(client)
    assert login(client, "wrong-one").status_code == 401
    assert login(client, "wrong-two").status_code == 423
    user = UserRepository(db_session).get_by_email(USER_EMAIL)
    db_session.refresh(user)
    locked_until = (
        user.locked_until.replace(tzinfo=timezone.utc)
        if user.locked_until.tzinfo is None
        else user.locked_until.astimezone(timezone.utc)
    )
    remaining = locked_until - datetime.now(timezone.utc)
    assert timedelta(minutes=4) < remaining <= timedelta(minutes=5)


def test_applicant_cannot_change_login_security_setting(client, auth_headers):
    response = client.patch(
        "/api/v1/admin/settings/login-security",
        headers=auth_headers,
        json={
            "failed_login_attempt_limit": 10,
            "lockout_duration_minutes": 30,
        },
    )
    assert response.status_code == 403
