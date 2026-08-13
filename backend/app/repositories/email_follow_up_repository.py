import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.application import Application
from app.models.email_follow_up import EmailFollowUp
from app.repositories.base import BaseRepository


class EmailFollowUpRepository(BaseRepository[EmailFollowUp]):
    model = EmailFollowUp

    def get_owned(self, user_id: uuid.UUID, id: uuid.UUID) -> EmailFollowUp:
        statement = (
            select(EmailFollowUp)
            .join(EmailFollowUp.application)
            .where(EmailFollowUp.id == id, Application.user_id == user_id)
        )
        instance = self.db.scalar(statement)
        if instance is None:
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail="Email follow-up not found")
        return instance

    def list_grouped_source(
        self, user_id: uuid.UUID, application_id: uuid.UUID | None = None
    ) -> list[Application]:
        statement = (
            select(Application)
            .join(Application.email_follow_ups)
            .where(Application.user_id == user_id)
            .options(
                selectinload(Application.opportunity),
                selectinload(Application.email_follow_ups),
            )
            .order_by(Application.applied_date.desc(), Application.created_at.desc())
        )
        if application_id is not None:
            statement = statement.where(Application.id == application_id)
        return list(self.db.scalars(statement).unique())

    def find_by_external_message(
        self, user_id: uuid.UUID, application_id: uuid.UUID, external_message_id: str
    ) -> EmailFollowUp | None:
        return self.db.scalar(
            select(EmailFollowUp)
            .join(EmailFollowUp.application)
            .where(
                Application.user_id == user_id,
                EmailFollowUp.application_id == application_id,
                EmailFollowUp.external_message_id == external_message_id,
            )
        )
