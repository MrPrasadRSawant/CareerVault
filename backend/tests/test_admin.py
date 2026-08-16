from app.core.security import hash_password
from app.models.enums import UserRole
from app.repositories.user_repository import UserRepository


ADMIN_EMAIL = "owner@example.com"
ADMIN_PASSWORD = "admin-password-123"


def create_admin(db_session):
    return UserRepository(db_session).create(
        email=ADMIN_EMAIL,
        full_name="Product Owner",
        hashed_password=hash_password(ADMIN_PASSWORD),
        is_active=True,
        role=UserRole.SYSTEM_ADMIN,
    )


def admin_headers(client, db_session):
    create_admin(db_session)
    response = client.post(
        "/api/v1/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    assert response.status_code == 200
    assert response.json()["user"]["role"] == "system_admin"
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_registration_assigns_applicant_role(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "applicant@example.com",
            "full_name": "Job Applicant",
            "password": "password123",
        },
    )
    assert response.status_code == 201
    assert response.json()["user"]["role"] == "job_applicant"


def test_shared_login_returns_each_users_role(client, db_session):
    create_admin(db_session)
    admin_login = client.post(
        "/api/v1/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    assert admin_login.status_code == 200
    assert admin_login.json()["user"]["role"] == "system_admin"

    client.post(
        "/api/v1/auth/register",
        json={
            "email": "candidate@example.com",
            "full_name": "Candidate",
            "password": "password123",
        },
    )
    applicant_login = client.post(
        "/api/v1/auth/login",
        json={"email": "candidate@example.com", "password": "password123"},
    )
    assert applicant_login.status_code == 200
    assert applicant_login.json()["user"]["role"] == "job_applicant"


def test_applicant_cannot_access_admin_api(client, auth_headers):
    response = client.get("/api/v1/admin/overview", headers=auth_headers)
    assert response.status_code == 403


def test_admin_overview_and_user_management(client, db_session):
    headers = admin_headers(client, db_session)
    register = client.post(
        "/api/v1/auth/register",
        json={
            "email": "managed@example.com",
            "full_name": "Managed Applicant",
            "password": "password123",
        },
    )
    applicant_id = register.json()["user"]["id"]

    overview = client.get("/api/v1/admin/overview", headers=headers)
    assert overview.status_code == 200
    assert overview.json()["total_users"] == 2
    assert overview.json()["active_users"] == 2
    assert overview.json()["new_users_last_30_days"] == 2
    assert len(overview.json()["registrations_by_day"]) == 7
    assert len(overview.json()["registrations_by_month"]) == 6
    assert len(overview.json()["registrations_by_year"]) == 5
    for series_name in (
        "registrations_by_day",
        "registrations_by_month",
        "registrations_by_year",
    ):
        latest_role_counts = {
            item["role"]: item["count"]
            for item in overview.json()[series_name][-1]["role_counts"]
        }
        assert latest_role_counts == {
            "job_applicant": 1,
            "system_admin": 1,
        }
    assert {
        item["role"]: item["count"] for item in overview.json()["role_counts"]
    } == {"job_applicant": 1, "system_admin": 1}

    users = client.get("/api/v1/admin/users?search=managed", headers=headers)
    assert users.status_code == 200
    assert users.json()["total"] == 1
    assert users.json()["items"][0]["email"] == "managed@example.com"
    assert users.json()["items"][0]["role"] == "job_applicant"
    assert "opportunity_count" not in users.json()["items"][0]
    assert "application_count" not in users.json()["items"][0]
    assert "resume_count" not in users.json()["items"][0]

    status_response = client.patch(
        f"/api/v1/admin/users/{applicant_id}/status",
        headers=headers,
        json={"is_active": False},
    )
    assert status_response.status_code == 200
    assert status_response.json()["is_active"] is False

    inactive_login = client.post(
        "/api/v1/auth/login",
        json={"email": "managed@example.com", "password": "password123"},
    )
    assert inactive_login.status_code == 403

    admin_users = client.get(
        "/api/v1/admin/users?role=system_admin", headers=headers
    )
    assert admin_users.status_code == 200
    assert admin_users.json()["total"] == 1
    admin_id = admin_users.json()["items"][0]["id"]
    protected_status = client.patch(
        f"/api/v1/admin/users/{admin_id}/status",
        headers=headers,
        json={"is_active": False},
    )
    assert protected_status.status_code == 403


def test_admin_token_cannot_access_applicant_api(client, db_session):
    headers = admin_headers(client, db_session)
    response = client.get("/api/v1/opportunities", headers=headers)
    assert response.status_code == 403
