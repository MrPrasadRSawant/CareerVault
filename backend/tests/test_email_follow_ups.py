def create_application(client, headers, title="Backend Engineer", company="Acme"):
    opportunity = client.post(
        "/api/v1/opportunities",
        headers=headers,
        json={"title": title, "company_name": company},
    ).json()
    return client.post(
        "/api/v1/applications",
        headers=headers,
        json={"opportunity_id": opportunity["id"]},
    ).json()


def email_payload(application_id, message_id, received_at, subject="Application update"):
    return {
        "application_id": application_id,
        "external_message_id": message_id,
        "thread_id": "thread-123",
        "subject": subject,
        "sender_email": "recruiter@acme.example",
        "sender_name": "Acme Recruiting",
        "recipient_emails": ["candidate@example.com"],
        "received_at": received_at,
        "body_text": "Thank you for your application.",
        "outcome": "pending",
        "reason": "The application is still being reviewed.",
        "reason_category": "screening",
        "ai_confidence": 0.93,
        "raw_metadata": {"source": "n8n"},
    }


def test_email_follow_up_crud_is_grouped_and_ordered(client, auth_headers):
    application = create_application(client, auth_headers)
    older = client.post(
        "/api/v1/email-follow-ups",
        headers=auth_headers,
        json=email_payload(
            application["id"], "message-1", "2026-08-10T09:00:00Z", "First reply"
        ),
    )
    newer = client.post(
        "/api/v1/email-follow-ups",
        headers=auth_headers,
        json=email_payload(
            application["id"], "message-2", "2026-08-12T09:00:00Z", "Final reply"
        ),
    )
    assert older.status_code == 201
    assert newer.status_code == 201

    grouped = client.get("/api/v1/email-follow-ups", headers=auth_headers)
    assert grouped.status_code == 200
    groups = grouped.json()
    assert len(groups) == 1
    assert groups[0]["application_id"] == application["id"]
    assert groups[0]["opportunity_title"] == "Backend Engineer"
    assert groups[0]["company_name"] == "Acme"
    assert groups[0]["email_count"] == 2
    assert [email["subject"] for email in groups[0]["emails"]] == [
        "Final reply",
        "First reply",
    ]

    updated = client.patch(
        f"/api/v1/email-follow-ups/{newer.json()['id']}",
        headers=auth_headers,
        json={
            "outcome": "lost",
            "reason_category": "qualifications",
            "reason": "Another candidate was selected.",
        },
    )
    assert updated.status_code == 200
    assert updated.json()["outcome"] == "lost"

    deleted = client.delete(
        f"/api/v1/email-follow-ups/{older.json()['id']}", headers=auth_headers
    )
    assert deleted.status_code == 200
    assert client.get(
        f"/api/v1/email-follow-ups/{older.json()['id']}", headers=auth_headers
    ).status_code == 404


def test_email_agent_uses_careervault_key_and_is_idempotent(client, auth_headers):
    application = create_application(client, auth_headers, "Data Engineer", "Northwind")
    created_key = client.post(
        "/api/v1/settings/api-keys",
        headers=auth_headers,
        json={"name": "n8n email workflow"},
    )
    assert created_key.status_code == 201
    agent_headers = {"X-CareerVault-Key": created_key.json()["key"]}

    assert client.get("/api/v1/email-agent/applications").status_code == 401
    assert (
        client.get(
            "/api/v1/email-agent/applications",
            headers={"X-API-Key": created_key.json()["key"]},
        ).status_code
        == 401
    )
    matches = client.get(
        "/api/v1/email-agent/applications",
        headers=agent_headers,
        params={"query": "Northwind"},
    )
    assert matches.status_code == 200
    assert matches.json()[0]["application_id"] == application["id"]

    payload = email_payload(
        application["id"], "provider-message-42", "2026-08-13T10:00:00Z"
    )
    first = client.post(
        "/api/v1/email-agent/follow-ups", headers=agent_headers, json=payload
    )
    retry = client.post(
        "/api/v1/email-agent/follow-ups", headers=agent_headers, json=payload
    )
    assert first.status_code == 201
    assert retry.status_code == 201
    assert retry.json()["id"] == first.json()["id"]

    grouped = client.get("/api/v1/email-follow-ups", headers=auth_headers).json()
    assert grouped[0]["email_count"] == 1

    schema = client.get("/api/v1/email-agent/openapi.json")
    assert schema.status_code == 200
    assert schema.json()["components"]["securitySchemes"]["APIKeyHeader"][
        "name"
    ] == "X-CareerVault-Key"
