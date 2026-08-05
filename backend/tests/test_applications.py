def test_application_flow(client, auth_headers):
    headers = auth_headers

    opportunity = client.post(
        "/opportunities",
        headers=headers,
        json={"title": "Frontend Developer"},
    ).json()

    created = client.post(
        "/applications",
        headers=headers,
        json={"opportunity_id": opportunity["id"]},
    )
    assert created.status_code == 201
    application = created.json()
    assert application["status"] == "applied"

    status_updated = client.post(
        f"/applications/{application['id']}/status",
        headers=headers,
        json={"status": "interview_scheduled", "note": "First round"},
    )
    assert status_updated.status_code == 200
    assert status_updated.json()["status"] == "interview_scheduled"

    history = client.get(
        f"/applications/{application['id']}/status-history", headers=headers
    )
    assert history.status_code == 200
    statuses = [entry["status"] for entry in history.json()]
    assert statuses == ["interview_scheduled"]

    interview = client.post(
        "/interviews",
        headers=headers,
        json={
            "application_id": application["id"],
            "scheduled_at": "2026-09-01T10:00:00Z",
            "type": "video",
        },
    )
    assert interview.status_code == 201
    assert interview.json()["application_id"] == application["id"]

    follow_up = client.post(
        "/follow-ups",
        headers=headers,
        json={
            "application_id": application["id"],
            "scheduled_at": "2026-09-05T10:00:00Z",
            "subject": "Status check",
        },
    )
    assert follow_up.status_code == 201


def test_interview_scoped_to_application_owner(client, auth_headers):
    headers = auth_headers

    opportunity = client.post(
        "/opportunities", headers=headers, json={"title": "DevOps"}
    ).json()
    application = client.post(
        "/applications",
        headers=headers,
        json={"opportunity_id": opportunity["id"]},
    ).json()
    interview = client.post(
        "/interviews",
        headers=headers,
        json={
            "application_id": application["id"],
            "scheduled_at": "2026-09-01T10:00:00Z",
        },
    ).json()

    client.post(
        "/auth/register",
        json={
            "email": "other2@example.com",
            "full_name": "Other User",
            "password": "password123",
        },
    )
    other_login = client.post(
        "/auth/login",
        json={"email": "other2@example.com", "password": "password123"},
    )
    other_headers = {
        "Authorization": f"Bearer {other_login.json()['access_token']}"
    }

    assert (
        client.get(f"/interviews/{interview['id']}", headers=other_headers).status_code
        == 404
    )
