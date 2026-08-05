from app.models.follow_up import FollowUp
from app.repositories.base import BaseRepository


class FollowUpRepository(BaseRepository[FollowUp]):
    model = FollowUp
