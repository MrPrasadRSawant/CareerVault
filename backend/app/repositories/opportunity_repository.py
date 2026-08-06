import uuid
from datetime import datetime

from fastapi import HTTPException, status

from sqlalchemy import select, update

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

    def soft_delete_owned(
        self,
        user_id: uuid.UUID,
        ids: list[uuid.UUID],
        *,
        updated_by: uuid.UUID,
        updated_on_utc: datetime,
    ) -> int:
        result = self.db.execute(
            update(JobOpportunity)
            .where(
                JobOpportunity.id.in_(ids),
                JobOpportunity.created_by == user_id,
                JobOpportunity.is_deleted.is_(False),
            )
            .values(
                is_deleted=True,
                updated_by=updated_by,
                updated_on_utc=updated_on_utc,
            )
        )
        self.db.commit()
        return result.rowcount or 0
