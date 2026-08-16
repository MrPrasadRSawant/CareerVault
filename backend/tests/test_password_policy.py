from sqlalchemy import select

from app.core.security import hash_password
from app.models.enums import AuthEventType, AuthFailureReason, UserRole
from app.models.login_audit_log import LoginAuditLog
from app.models.system_setting import SystemSetting
from app.repositories.user_repository import UserRepository


ADMIN_EMAIL = "password-policy-owner@example.com"
ADMIN_PASSWORD = "admin-password-123"


def admin_headers(client, db_session):
    UserRepository(db_session).create(
        email=ADMIN_EMAIL,
        full_name="Password Policy Owner",
        hashed_password=hash_password(ADMIN_PASSWORD),
        is_active=True,
        role=UserRole.SYSTEM_ADMIN,
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def register(client, email: str, password: str):
    return client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "full_name": "Password Policy User",
            "password": password,
            "terms_accepted": True,
            "terms_version": 1,
        },
    )


def test_default_password_policy_is_public_and_enforced_on_registration(client):
    policy = client.get("/api/v1/auth/password-policy")
    assert policy.status_code == 200
    assert policy.json() == {"minimum_length": 8, "maximum_length": 20}

    too_short = register(client, "short@example.com", "1234567")
    too_long = register(client, "long@example.com", "x" * 21)
    minimum = register(client, "minimum@example.com", "x" * 8)
    maximum = register(client, "maximum@example.com", "x" * 20)

    assert too_short.status_code == 422
    assert too_long.status_code == 422
    assert minimum.status_code == 201
    assert maximum.status_code == 201


def test_admin_can_edit_password_policy_within_eight_to_twenty(
    client, db_session
):
    headers = admin_headers(client, db_session)
    response = client.patch(
        "/api/v1/admin/settings/password-policy",
        headers=headers,
        json={"minimum_length": 10, "maximum_length": 16},
    )

    assert response.status_code == 200
    assert response.json()["minimum_length"] == 10
    assert response.json()["maximum_length"] == 16
    stored = {
        item.key: item.value
        for item in db_session.scalars(
            select(SystemSetting).where(
                SystemSetting.key.in_(
                    ["password_min_length", "password_max_length"]
                )
            )
        )
    }
    assert stored == {
        "password_min_length": "10",
        "password_max_length": "16",
    }

    assert register(client, "nine@example.com", "x" * 9).status_code == 422
    assert register(client, "ten@example.com", "x" * 10).status_code == 201


def test_invalid_admin_password_ranges_are_rejected(client, db_session):
    headers = admin_headers(client, db_session)

    reversed_range = client.patch(
        "/api/v1/admin/settings/password-policy",
        headers=headers,
        json={"minimum_length": 16, "maximum_length": 10},
    )
    below_boundary = client.patch(
        "/api/v1/admin/settings/password-policy",
        headers=headers,
        json={"minimum_length": 7, "maximum_length": 20},
    )

    assert reversed_range.status_code == 422
    assert below_boundary.status_code == 422


def test_login_length_failure_is_audited_and_counts_as_failed_attempt(
    client, db_session
):
    assert register(client, "existing@example.com", "password123").status_code == 201
    headers = admin_headers(client, db_session)
    client.patch(
        "/api/v1/admin/settings/password-policy",
        headers=headers,
        json={"minimum_length": 12, "maximum_length": 20},
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "existing@example.com", "password": "password123"},
    )
    assert response.status_code == 401

    user = UserRepository(db_session).get_by_email("existing@example.com")
    db_session.refresh(user)
    assert user.failed_login_attempts == 1
    event = db_session.scalar(
        select(LoginAuditLog)
        .where(
            LoginAuditLog.user_id == user.id,
            LoginAuditLog.event_type == AuthEventType.LOGIN,
        )
        .order_by(LoginAuditLog.occurred_at.desc())
    )
    assert event is not None
    assert event.failure_reason == AuthFailureReason.INVALID_CREDENTIALS


def test_applicant_cannot_change_password_policy(client, auth_headers):
    response = client.patch(
        "/api/v1/admin/settings/password-policy",
        headers=auth_headers,
        json={"minimum_length": 10, "maximum_length": 18},
    )
    assert response.status_code == 403
