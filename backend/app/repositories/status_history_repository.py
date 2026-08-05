from app.models.application_status_history import ApplicationStatusHistory
from app.repositories.base import BaseRepository


class ApplicationStatusHistoryRepository(BaseRepository[ApplicationStatusHistory]):
    model = ApplicationStatusHistory
