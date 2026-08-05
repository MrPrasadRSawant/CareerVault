def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "new@example.com",
            "full_name": "New User",
            "password": "password123",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["access_token"]
    assert body["user"]["email"] == "new@example.com"
    assert "hashed_password" not in body["user"]


def test_register_duplicate_email(client):
    payload = {
        "email": "dup@example.com",
        "full_name": "Dup User",
        "password": "password123",
    }
    assert client.post("/auth/register", json=payload).status_code == 201
    assert client.post("/auth/register", json=payload).status_code == 409


def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "full_name": "Login User",
            "password": "password123",
        },
    )
    response = client.post(
        "/auth/login",
        json={"email": "login@example.com", "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_me_requires_auth(client):
    assert client.get("/auth/me").status_code == 401
