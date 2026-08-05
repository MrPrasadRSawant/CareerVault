import uuid

from app.models.application import Application
from app.repositories.base import BaseRepository


class ApplicationRepository(BaseRepository[Application]):
    model = Application

    def get_owned_by_application_user(
        self, user_id: uuid.UUID, id: uuid.UUID
    ) -> Application:
        return self.get_owned(user_id, id)
