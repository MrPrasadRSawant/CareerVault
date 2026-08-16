def test_opportunity_crud(client, auth_headers):
    headers = auth_headers

    response = client.get("/api/v1/opportunities", headers=headers)
    assert response.status_code == 200
    assert response.json() == []

    created = client.post(
        "/api/v1/opportunities",
        headers=headers,
        json={
            "title": "Backend Engineer",
            "salary_range": "100k-130k",
            "required_skills": ["Python", "FastAPI"],
        },
    )
    assert created.status_code == 201
    opportunity = created.json()
    assert opportunity["title"] == "Backend Engineer"
    assert opportunity["status"] == "saved"
    assert opportunity["required_skills"] == ["Python", "FastAPI"]

    fetched = client.get(f"/api/v1/opportunities/{opportunity['id']}", headers=headers)
    assert fetched.status_code == 200

    updated = client.patch(
        f"/api/v1/opportunities/{opportunity['id']}",
        headers=headers,
        json={"status": "applied"},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "applied"

    deleted = client.delete(f"/api/v1/opportunities/{opportunity['id']}", headers=headers)
    assert deleted.status_code == 200
    assert client.get(f"/api/v1/opportunities/{opportunity['id']}", headers=headers).status_code == 404


def test_opportunity_requires_auth(client):
    assert client.post("/api/v1/opportunities", json={"title": "X"}).status_code == 401


def test_opportunities_are_user_scoped(client, auth_headers):
    created = client.post(
        "/api/v1/opportunities",
        headers=auth_headers,
        json={"title": "Private Role"},
    )
    opportunity_id = created.json()["id"]

    client.post(
        "/api/v1/auth/register",
        json={
            "email": "other@example.com",
            "full_name": "Other User",
            "password": "password123",
            "terms_accepted": True,
            "terms_version": 1,
        },
    )
    other_login = client.post(
        "/api/v1/auth/login",
        json={"email": "other@example.com", "password": "password123"},
    )
    other_headers = {
        "Authorization": f"Bearer {other_login.json()['access_token']}"
    }

    assert client.get("/api/v1/opportunities", headers=other_headers).json() == []
    assert (
        client.get(f"/api/v1/opportunities/{opportunity_id}", headers=other_headers).status_code
        == 404
    )


def test_bulk_delete_opportunities_is_owner_scoped(client, auth_headers):
    owned_ids = [
        client.post(
            "/api/v1/opportunities",
            headers=auth_headers,
            json={"title": title},
        ).json()["id"]
        for title in ("First Role", "Second Role")
    ]

    client.post(
        "/api/v1/auth/register",
        json={
            "email": "bulk-other@example.com",
            "full_name": "Bulk Other User",
            "password": "password123",
            "terms_accepted": True,
            "terms_version": 1,
        },
    )
    other_login = client.post(
        "/api/v1/auth/login",
        json={"email": "bulk-other@example.com", "password": "password123"},
    )
    other_headers = {
        "Authorization": f"Bearer {other_login.json()['access_token']}"
    }
    other_id = client.post(
        "/api/v1/opportunities",
        headers=other_headers,
        json={"title": "Other User Role"},
    ).json()["id"]

    deleted = client.post(
        "/api/v1/opportunities/bulk-delete",
        headers=auth_headers,
        json={"ids": [*owned_ids, other_id, owned_ids[0]]},
    )

    assert deleted.status_code == 200
    assert deleted.json() == {"deleted_count": 2}
    assert client.get("/api/v1/opportunities", headers=auth_headers).json() == []
    assert len(client.get("/api/v1/opportunities", headers=other_headers).json()) == 1
