from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.core.security import hash_password
from app.main import app
from app.models.enums import UserRole
from app.models.exception_log import ExceptionLog
from app.repositories.user_repository import UserRepository


def _raise_unexpected_error():
    raise RuntimeError(
        "Unable to process user@example.com password=super-secret-value"
    )


app.add_api_route(
    "/api/v1/_test/unhandled-exception",
    _raise_unexpected_error,
    methods=["GET"],
    include_in_schema=False,
)


def _raise_handled_server_error():
    raise HTTPException(status_code=503, detail="Dependency unavailable")


app.add_api_route(
    "/api/v1/_test/handled-server-error",
    _raise_handled_server_error,
    methods=["GET"],
    include_in_schema=False,
)


def create_admin_headers(client, db_session):
    UserRepository(db_session).create(
        email="exception-owner@example.com",
        full_name="Exception Owner",
        hashed_password=hash_password("admin-password-123"),
        is_active=True,
        role=UserRole.SYSTEM_ADMIN,
    )
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "exception-owner@example.com",
            "password": "admin-password-123",
        },
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_unhandled_exceptions_are_appended_and_sensitive_values_are_redacted(
    client, auth_headers, db_session
):
    with TestClient(app, raise_server_exceptions=False) as safe_client:
        first = safe_client.get(
            "/api/v1/_test/unhandled-exception",
            params={"debug_token": "do-not-store-this-value"},
            headers={
                **auth_headers,
                "User-Agent": "Exception test browser",
            },
        )
        second = safe_client.get(
            "/api/v1/_test/unhandled-exception",
            headers=auth_headers,
        )

    assert first.status_code == 500
    assert first.json()["detail"] == "An unexpected server error occurred"
    assert first.json()["request_id"] == first.headers["x-request-id"]
    assert second.status_code == 500

    entries = list(db_session.scalars(select(ExceptionLog)))
    assert len(entries) == 2
    assert entries[0].id != entries[1].id
    assert entries[0].request_id != entries[1].request_id
    assert entries[0].fingerprint == entries[1].fingerprint
    assert entries[0].route_template == "/api/v1/_test/unhandled-exception"
    assert entries[0].query_parameter_names == "debug_token"
    assert "do-not-store-this-value" not in entries[0].message
    assert "do-not-store-this-value" not in entries[0].traceback
    assert "user@example.com" not in entries[0].message
    assert "super-secret-value" not in entries[0].message
    assert "[email-redacted]" in entries[0].message
    assert "password=[redacted]" in entries[0].message
    assert entries[0].user_id is not None
    assert entries[0].ip_address is None


def test_expected_client_errors_are_not_exception_logs(client, db_session):
    response = client.get("/api/v1/does-not-exist")

    assert response.status_code == 404
    assert list(db_session.scalars(select(ExceptionLog))) == []


def test_explicit_server_errors_are_logged_as_handled(client, db_session):
    response = client.get("/api/v1/_test/handled-server-error")

    assert response.status_code == 503
    entry = db_session.scalar(select(ExceptionLog))
    assert entry is not None
    assert entry.status_code == 503
    assert entry.is_handled is True
    assert entry.request_id == response.headers["x-request-id"]


def test_only_admin_can_view_exception_logs(client, auth_headers, db_session):
    assert (
        client.get("/api/v1/admin/exceptions", headers=auth_headers).status_code
        == 403
    )

    admin_headers = create_admin_headers(client, db_session)
    with TestClient(app, raise_server_exceptions=False) as safe_client:
        safe_client.get("/api/v1/_test/unhandled-exception")

    listing = client.get("/api/v1/admin/exceptions", headers=admin_headers)
    assert listing.status_code == 200
    assert listing.json()["total"] == 1
    item = listing.json()["items"][0]
    assert "traceback" not in item

    detail = client.get(
        f"/api/v1/admin/exceptions/{item['id']}", headers=admin_headers
    )
    assert detail.status_code == 200
    assert "RuntimeError" in detail.json()["traceback"]

    overview = client.get(
        "/api/v1/admin/exceptions/overview", headers=admin_headers
    )
    assert overview.status_code == 200
    assert overview.json()["exceptions_last_24_hours"] == 1
