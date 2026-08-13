def create_application_with_email(client, headers):
    opportunity = client.post(
        "/api/v1/opportunities",
        headers=headers,
        json={"title": "Platform Engineer", "company_name": "Contoso"},
    ).json()
    application = client.post(
        "/api/v1/applications",
        headers=headers,
        json={"opportunity_id": opportunity["id"]},
    ).json()
    email = client.post(
        "/api/v1/email-follow-ups",
        headers=headers,
        json={
            "application_id": application["id"],
            "external_message_id": "notification-email-1",
            "subject": "Interview availability",
            "sender_email": "recruiter@contoso.example",
            "sender_name": "Contoso Recruiting",
            "received_at": "2026-08-13T10:00:00Z",
            "outcome": "pending",
        },
    )
    assert email.status_code == 201


def test_notifications_are_generated_and_support_seen_actions(client, auth_headers):
    create_application_with_email(client, auth_headers)

    count = client.get("/api/v1/notifications/unseen-count", headers=auth_headers)
    assert count.status_code == 200
    assert count.json() == {"unseen_count": 2}

    response = client.get("/api/v1/notifications", headers=auth_headers)
    assert response.status_code == 200
    notifications = response.json()
    assert [item["type"] for item in notifications] == [
        "email_follow_up",
        "opportunity",
    ]
    assert notifications[0]["title"] == "New recruiter response"
    assert notifications[0]["action_path"] == "/email-follow-ups"
    assert notifications[1]["action_path"] == "/opportunities"
    assert (
        client.post(
            "/api/v1/notifications", headers=auth_headers, json={}
        ).status_code
        == 405
    )
    assert client.delete(
        f"/api/v1/notifications/{notifications[0]['id']}",
        headers=auth_headers,
    ).status_code in {404, 405}

    notification_id = notifications[0]["id"]
    marked_seen = client.patch(
        f"/api/v1/notifications/{notification_id}/seen",
        headers=auth_headers,
        json={"is_seen": True},
    )
    assert marked_seen.status_code == 200
    assert marked_seen.json()["is_seen"] is True
    assert marked_seen.json()["seen_at"] is not None
    assert client.get(
        "/api/v1/notifications/unseen-count", headers=auth_headers
    ).json() == {"unseen_count": 1}

    marked_unseen = client.patch(
        f"/api/v1/notifications/{notification_id}/seen",
        headers=auth_headers,
        json={"is_seen": False},
    )
    assert marked_unseen.status_code == 200
    assert marked_unseen.json()["is_seen"] is False
    assert marked_unseen.json()["seen_at"] is None

    mark_all = client.patch(
        "/api/v1/notifications/mark-all-seen", headers=auth_headers
    )
    assert mark_all.status_code == 200
    assert client.get(
        "/api/v1/notifications/unseen-count", headers=auth_headers
    ).json() == {"unseen_count": 0}


def test_notifications_are_user_scoped(client, auth_headers):
    client.post(
        "/api/v1/opportunities",
        headers=auth_headers,
        json={"title": "Private opportunity"},
    )
    owned_notification = client.get(
        "/api/v1/notifications", headers=auth_headers
    ).json()[0]

    client.post(
        "/api/v1/auth/register",
        json={
            "email": "notification-other@example.com",
            "full_name": "Other User",
            "password": "password123",
        },
    )
    login = client.post(
        "/api/v1/auth/login",
        json={
            "email": "notification-other@example.com",
            "password": "password123",
        },
    )
    other_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    assert client.get("/api/v1/notifications", headers=other_headers).json() == []
    assert (
        client.patch(
            f"/api/v1/notifications/{owned_notification['id']}/seen",
            headers=other_headers,
            json={"is_seen": True},
        ).status_code
        == 404
    )


def test_ai_opportunity_ingestion_generates_notifications(client, auth_headers):
    created_key = client.post(
        "/api/v1/settings/api-keys",
        headers=auth_headers,
        json={"name": "Opportunity agent"},
    ).json()
    agent_headers = {"X-CareerVault-Key": created_key["key"]}

    single = client.post(
        "/api/v1/ai/opportunities",
        headers=agent_headers,
        json={"title": "AI single opportunity"},
    )
    assert single.status_code == 201
    bulk = client.post(
        "/api/v1/ai/opportunities/bulk",
        headers=agent_headers,
        json={
            "opportunities": [
                {"title": "AI bulk one"},
                {"title": "AI bulk two"},
            ]
        },
    )
    assert bulk.status_code == 201

    assert client.get(
        "/api/v1/notifications/unseen-count", headers=auth_headers
    ).json() == {"unseen_count": 3}
