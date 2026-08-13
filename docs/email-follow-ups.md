# Email follow-up module

CareerVault exposes two separate API groups for recruiter email tracking:

- `/api/v1/email-follow-ups` is the application-facing CRUD API. It uses the normal bearer token and returns emails grouped by application with each chain ordered by `received_at` descending.
- `/api/v1/email-agent` is the n8n/AI-agent API. It uses the same `X-CareerVault-Key` header and API keys as the existing AI Actions API, while remaining isolated in its own OpenAPI document at `/api/v1/email-agent/openapi.json`.

Create a key in **Settings → API keys**. The same stored key mechanism is used for existing AI Actions, but the email agent must send it as:

```http
X-CareerVault-Key: cvai_your_key_here
```

## Suggested n8n agent flow

1. Trigger when a new email arrives.
2. Let the agent decide whether it is an application reply.
3. Call `GET /api/v1/email-agent/applications?query=...` using a company name, role, or other identifying text from the email.
4. If a confident application match is found, call `POST /api/v1/email-agent/follow-ups` with the matched `application_id` and classification.
5. Always provide the email provider's stable ID as `external_message_id`. Repeated requests with the same application and message ID return the existing record rather than creating a duplicate.

The record accepts `outcome` (`pending`, `won`, or `lost`), free-form `reason_category`, `reason`, `ai_confidence` from 0 to 1, and `raw_metadata` for provider-specific information.
