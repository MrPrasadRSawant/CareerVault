import uuid

from fastapi import HTTPException, status
from sqlalchemy import select

from app.models.job_opportunity import JobOpportunity
from app.repositories.base import BaseRepository


class OpportunityRepository(BaseRepository[JobOpportunity]):
    model = JobOpportunity

    def list_owned(
        self, user_id: uuid.UUID, *, limit: int = 100, offset: int = 0
    ) -> list[JobOpportunity]:
        stmt = (
            select(JobOpportunity)
            .where(
                JobOpportunity.created_by == user_id,
                JobOpportunity.is_deleted.is_(False),
            )
            .order_by(JobOpportunity.created_on_utc.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.scalars(stmt))

    def get_owned(self, user_id: uuid.UUID, id: uuid.UUID) -> JobOpportunity:
        opportunity = self.db.scalar(
            select(JobOpportunity).where(
                JobOpportunity.id == id,
                JobOpportunity.created_by == user_id,
                JobOpportunity.is_deleted.is_(False),
            )
        )
        if opportunity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="JobOpportunity not found",
            )
        return opportunity
