from datetime import datetime, timedelta, timezone

from app.core.security import hash_password
from app.models.daily_registration_counter import DailyRegistrationCounter
from app.models.enums import UserRole
from app.repositories.user_repository import UserRepository


ADMIN_EMAIL = "settings-owner@example.com"
ADMIN_PASSWORD = "admin-password-123"


def register(client, email: str):
    return client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "full_name": "Limited Applicant",
            "password": "password123",
            "terms_accepted": True,
            "terms_version": 1,
        },
    )


def admin_headers(client, db_session):
    UserRepository(db_session).create(
        email=ADMIN_EMAIL,
        full_name="Settings Owner",
        hashed_password=hash_password(ADMIN_PASSWORD),
        is_active=True,
        role=UserRole.SYSTEM_ADMIN,
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_daily_registration_limit_defaults_to_one_thousand(client, db_session):
    headers = admin_headers(client, db_session)

    response = client.get(
        "/api/v1/admin/settings/registration", headers=headers
    )

    assert response.status_code == 200
    assert response.json()["daily_registration_limit"] == 1000
    assert response.json()["registrations_used_today"] == 0


def test_admin_can_change_limit_and_registration_is_capped(client, db_session):
    headers = admin_headers(client, db_session)
    update = client.patch(
        "/api/v1/admin/settings/registration",
        headers=headers,
        json={"daily_registration_limit": 2},
    )
    assert update.status_code == 200
    assert update.json()["daily_registration_limit"] == 2

    assert register(client, "first@example.com").status_code == 201
    assert register(client, "second@example.com").status_code == 201

    rejected = register(client, "third@example.com")
    assert rejected.status_code == 429
    assert "registration limit" in rejected.json()["detail"]
    assert int(rejected.headers["retry-after"]) > 0
    assert (
        UserRepository(db_session).get_by_email("third@example.com") is None
    )

    status_response = client.get(
        "/api/v1/admin/settings/registration", headers=headers
    )
    assert status_response.json()["registrations_used_today"] == 2
    assert status_response.json()["registrations_remaining_today"] == 0


def test_registration_counter_is_scoped_to_utc_day(client, db_session):
    headers = admin_headers(client, db_session)
    client.patch(
        "/api/v1/admin/settings/registration",
        headers=headers,
        json={"daily_registration_limit": 1},
    )
    yesterday = datetime.now(timezone.utc).date() - timedelta(days=1)
    db_session.add(
        DailyRegistrationCounter(
            registration_date=yesterday,
            registration_count=1,
        )
    )
    db_session.commit()

    assert register(client, "new-day@example.com").status_code == 201


def test_applicant_cannot_read_or_change_system_settings(client, auth_headers):
    assert (
        client.get(
            "/api/v1/admin/settings/registration", headers=auth_headers
        ).status_code
        == 403
    )
    assert (
        client.patch(
            "/api/v1/admin/settings/registration",
            headers=auth_headers,
            json={"daily_registration_limit": 10},
        ).status_code
        == 403
    )
