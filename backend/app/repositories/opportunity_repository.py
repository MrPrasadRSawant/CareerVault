from app.models.job_opportunity import JobOpportunity
from app.repositories.base import BaseRepository


class OpportunityRepository(BaseRepository[JobOpportunity]):
    model = JobOpportunity
