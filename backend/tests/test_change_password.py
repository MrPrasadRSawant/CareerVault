from app.core.security import hash_password
from app.models.enums import UserRole
from app.models.user import User


def register_and_headers(client) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "password-change@example.com",
            "full_name": "Password Change User",
            "password": "password123",
            "terms_accepted": True,
            "terms_version": 1,
        },
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_change_password_requires_current_password_and_policy(client):
    headers = register_and_headers(client)

    wrong_current = client.post(
        "/api/v1/auth/change-password",
        headers=headers,
        json={
            "current_password": "not-the-current-password",
            "new_password": "new-password-123",
        },
    )
    reused = client.post(
        "/api/v1/auth/change-password",
        headers=headers,
        json={
            "current_password": "password123",
            "new_password": "password123",
        },
    )
    too_short = client.post(
        "/api/v1/auth/change-password",
        headers=headers,
        json={
            "current_password": "password123",
            "new_password": "short",
        },
    )

    assert wrong_current.status_code == 400
    assert wrong_current.json()["detail"] == "Current password is incorrect"
    assert reused.status_code == 422
    assert too_short.status_code == 422


def test_applicant_changes_password_and_keeps_current_session(client):
    headers = register_and_headers(client)
    response = client.post(
        "/api/v1/auth/change-password",
        headers=headers,
        json={
            "current_password": "password123",
            "new_password": "new-password-123",
        },
    )

    assert response.status_code == 204
    assert client.get("/api/v1/auth/me", headers=headers).status_code == 200
    assert (
        client.post(
            "/api/v1/auth/login",
            json={
                "email": "password-change@example.com",
                "password": "password123",
            },
        ).status_code
        == 401
    )
    assert (
        client.post(
            "/api/v1/auth/login",
            json={
                "email": "password-change@example.com",
                "password": "new-password-123",
            },
        ).status_code
        == 200
    )


def test_system_admin_can_change_password(client, db_session):
    admin = User(
        email="password-admin@example.com",
        full_name="Password Admin",
        hashed_password=hash_password("admin-password-123"),
        role=UserRole.SYSTEM_ADMIN,
    )
    db_session.add(admin)
    db_session.commit()
    login = client.post(
        "/api/v1/auth/login",
        json={
            "email": admin.email,
            "password": "admin-password-123",
        },
    )
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    response = client.post(
        "/api/v1/auth/change-password",
        headers=headers,
        json={
            "current_password": "admin-password-123",
            "new_password": "updated-admin-123",
        },
    )
    assert response.status_code == 204
    assert (
        client.post(
            "/api/v1/auth/login",
            json={
                "email": admin.email,
                "password": "updated-admin-123",
            },
        ).status_code
        == 200
    )
