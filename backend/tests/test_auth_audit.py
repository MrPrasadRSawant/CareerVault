from app.core.request_context import auth_client_context
from app.core.security import hash_password
from app.models.enums import UserRole
from app.repositories.user_repository import UserRepository
from starlette.requests import Request


ADMIN_EMAIL = "security-owner@example.com"
ADMIN_PASSWORD = "admin-password-123"


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


def test_auth_context_uses_validated_client_ip_and_sanitizes_user_agent():
    request = Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/api/v1/auth/login",
            "headers": [(b"user-agent", b"Browser/1.0\x00injected")],
            "client": ("203.0.113.15", 443),
            "server": ("testserver", 80),
            "scheme": "https",
            "query_string": b"",
        }
    )
    context = auth_client_context(request)
    assert context.ip_address == "203.0.113.15"
    assert context.user_agent == "Browser/1.0 injected"


def test_login_failures_successes_and_session_logout_are_audited(
    client, db_session
):
    register = client.post(
        "/api/v1/auth/register",
        headers={"user-agent": "AuditBrowser/1.0"},
        json={
            "email": "audited@example.com",
            "full_name": "Audited User",
            "password": "password123",
            "terms_accepted": True,
            "terms_version": 1,
        },
    )
    assert register.status_code == 201

    failed = client.post(
        "/api/v1/auth/login",
        headers={"user-agent": "AuditBrowser/1.0"},
        json={"email": "audited@example.com", "password": "wrong-password"},
    )
    assert failed.status_code == 401

    unknown = client.post(
        "/api/v1/auth/login",
        json={"email": "unknown@example.com", "password": "wrong-password"},
    )
    assert unknown.status_code == 401

    successful = client.post(
        "/api/v1/auth/login",
        headers={"user-agent": "AuditBrowser/1.0"},
        json={"email": "audited@example.com", "password": "password123"},
    )
    assert successful.status_code == 200
    applicant_headers = {
        "Authorization": f"Bearer {successful.json()['access_token']}"
    }

    headers = admin_headers(client, db_session)
    overview = client.get("/api/v1/admin/security/overview", headers=headers)
    assert overview.status_code == 200
    assert overview.json()["successful_logins_last_24_hours"] >= 2
    assert overview.json()["failed_logins_last_24_hours"] == 2
    assert overview.json()["active_sessions"] >= 2

    failed_events = client.get(
        "/api/v1/admin/security/login-events?outcome=failure",
        headers=headers,
    )
    assert failed_events.status_code == 200
    assert failed_events.json()["total"] == 2
    known_event = next(
        item
        for item in failed_events.json()["items"]
        if item["account_known"]
    )
    assert known_event["user_email"] == "audited@example.com"
    assert known_event["failure_reason"] == "invalid_credentials"
    assert known_event["user_agent"] == "AuditBrowser/1.0"
    unknown_event = next(
        item
        for item in failed_events.json()["items"]
        if not item["account_known"]
    )
    assert unknown_event["user_email"] is None
    assert len(unknown_event["unknown_account_reference"]) == 12

    sessions = client.get(
        "/api/v1/admin/security/sessions?search=audited",
        headers=headers,
    )
    assert sessions.status_code == 200
    assert sessions.json()["total"] == 2
    assert {
        item["auth_method"] for item in sessions.json()["items"]
    } == {"login", "registration"}

    logout = client.post("/api/v1/auth/logout", headers=applicant_headers)
    assert logout.status_code == 204

    sessions_after_logout = client.get(
        "/api/v1/admin/security/sessions?search=audited",
        headers=headers,
    )
    login_session = next(
        item
        for item in sessions_after_logout.json()["items"]
        if item["auth_method"] == "login"
    )
    assert login_session["status"] == "ended"
    assert login_session["duration_basis"] == "exact"
    assert login_session["end_reason"] == "logout"


def test_applicant_cannot_read_authentication_audit(client, auth_headers):
    response = client.get(
        "/api/v1/admin/security/login-events", headers=auth_headers
    )
    assert response.status_code == 403
