from app.schemas.email_follow_up import EmailFollowUpCreate, EmailFollowUpUpdate


def email_follow_up_create_values(payload: EmailFollowUpCreate) -> dict:
    values = payload.model_dump()
    values["sender_email"] = str(payload.sender_email)
    if payload.recipient_emails is not None:
        values["recipient_emails"] = [str(email) for email in payload.recipient_emails]
    return values


def email_follow_up_update_values(payload: EmailFollowUpUpdate) -> dict:
    values = payload.model_dump(exclude_unset=True)
    for required_field in (
        "application_id",
        "subject",
        "sender_email",
        "received_at",
        "outcome",
    ):
        if values.get(required_field) is None:
            values.pop(required_field, None)
    if "sender_email" in values:
        values["sender_email"] = str(values["sender_email"])
    if "recipient_emails" in values and values["recipient_emails"] is not None:
        values["recipient_emails"] = [str(email) for email in values["recipient_emails"]]
    return values
