from app.core.security import hash_password
from app.models.enums import UserRole
from app.models.user import User


def registration_payload(email: str, version: int = 1) -> dict:
    return {
        "email": email,
        "full_name": "Terms User",
        "password": "password123",
        "terms_accepted": True,
        "terms_version": version,
    }


def admin_headers(client, db_session) -> dict[str, str]:
    admin = User(
        email="terms-admin@example.com",
        full_name="Terms Admin",
        hashed_password=hash_password("admin-password-123"),
        role=UserRole.SYSTEM_ADMIN,
    )
    db_session.add(admin)
    db_session.commit()
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": admin.email,
            "password": "admin-password-123",
        },
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_terms_are_public_and_registration_requires_consent(client):
    terms = client.get("/api/v1/legal/terms-of-service")
    assert terms.status_code == 200
    assert terms.json()["version"] == 1
    assert "CareerVault Terms of Service" in terms.json()["content_html"]

    missing = client.post(
        "/api/v1/auth/register",
        json={
            "email": "missing-terms@example.com",
            "full_name": "Missing Terms",
            "password": "password123",
        },
    )
    declined = client.post(
        "/api/v1/auth/register",
        json={
            **registration_payload("declined-terms@example.com"),
            "terms_accepted": False,
        },
    )
    assert missing.status_code == 422
    assert declined.status_code == 422


def test_registration_stores_exact_terms_snapshot(client, db_session):
    terms = client.get("/api/v1/legal/terms-of-service").json()
    response = client.post(
        "/api/v1/auth/register",
        json=registration_payload("accepted@example.com", terms["version"]),
    )
    assert response.status_code == 201

    user = db_session.query(User).filter_by(email="accepted@example.com").one()
    assert user.terms_accepted_at is not None
    assert user.terms_accepted_version == terms["version"]
    assert user.terms_accepted_content == terms["content_html"]


def test_admin_publishes_sanitized_version_and_stale_registration_is_rejected(
    client, db_session
):
    headers = admin_headers(client, db_session)
    original = client.get("/api/v1/legal/terms-of-service").json()
    updated_html = (
        "<h1>Updated Terms</h1><p>These are the updated platform terms.</p>"
        "<script>alert('unsafe')</script>"
        '<p><a href="javascript:alert(1)">Unsafe link</a></p>'
    )
    updated = client.patch(
        "/api/v1/admin/settings/terms-of-service",
        headers=headers,
        json={"content_html": updated_html},
    )
    assert updated.status_code == 200
    body = updated.json()
    assert body["version"] == original["version"] + 1
    assert "script" not in body["content_html"]
    assert "javascript:" not in body["content_html"]

    stale = client.post(
        "/api/v1/auth/register",
        json=registration_payload("stale@example.com", original["version"]),
    )
    assert stale.status_code == 409

    accepted = client.post(
        "/api/v1/auth/register",
        json=registration_payload("current@example.com", body["version"]),
    )
    assert accepted.status_code == 201
    user = db_session.query(User).filter_by(email="current@example.com").one()
    assert user.terms_accepted_content == body["content_html"]


def test_applicant_cannot_edit_terms(client, auth_headers):
    response = client.patch(
        "/api/v1/admin/settings/terms-of-service",
        headers=auth_headers,
        json={
            "content_html": (
                "<h1>Unauthorized update</h1>"
                "<p>An applicant must not publish this content.</p>"
            )
        },
    )
    assert response.status_code == 403
