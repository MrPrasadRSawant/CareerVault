import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.email_follow_up import EmailFollowUp
from app.models.enums import NotificationType
from app.models.job_opportunity import JobOpportunity
from app.models.notification import Notification


class NotificationService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def opportunity_added(
        self, user_id: uuid.UUID, opportunity: JobOpportunity, *, commit: bool = True
    ) -> Notification:
        company = f" at {opportunity.company_name}" if opportunity.company_name else ""
        notification = Notification(
            user_id=user_id,
            type=NotificationType.OPPORTUNITY,
            title="New opportunity added",
            message=f"{opportunity.title}{company} was added to your opportunity inbox.",
            entity_id=opportunity.id,
            action_path="/opportunities",
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(notification)
        if commit:
            self.db.commit()
            self.db.refresh(notification)
        return notification

    def email_follow_up_added(
        self,
        user_id: uuid.UUID,
        email: EmailFollowUp,
        application: Application,
    ) -> Notification:
        opportunity = application.opportunity
        company = f" at {opportunity.company_name}" if opportunity.company_name else ""
        sender = email.sender_name or email.sender_email
        notification = Notification(
            user_id=user_id,
            type=NotificationType.EMAIL_FOLLOW_UP,
            title="New recruiter response",
            message=f"{sender} replied about {opportunity.title}{company}: {email.subject}",
            entity_id=email.id,
            action_path="/email-follow-ups",
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification
