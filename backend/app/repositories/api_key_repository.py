import hashlib
import secrets
import uuid
from datetime import datetime, timezone

from sqlalchemy import select

from app.models.api_key import ApiKey
from app.repositories.base import BaseRepository


class ApiKeyRepository(BaseRepository[ApiKey]):
    model = ApiKey

    @staticmethod
    def hash_key(key: str) -> str:
        return hashlib.sha256(key.encode("utf-8")).hexdigest()

    def create_for_user(self, user_id: uuid.UUID, *, name: str, expires_on_utc: datetime | None = None) -> tuple[ApiKey, str]:
        raw_key = f"cvai_{secrets.token_urlsafe(32)}"
        instance = self.create(user_id=user_id, name=name.strip(), key_prefix=raw_key[:12], key_hash=self.hash_key(raw_key), expires_on_utc=expires_on_utc)
        return instance, raw_key

    def authenticate(self, raw_key: str) -> ApiKey | None:
        instance = self.db.scalar(select(ApiKey).where(ApiKey.key_hash == self.hash_key(raw_key), ApiKey.is_revoked.is_(False)))
        if instance is None or (instance.expires_on_utc and instance.expires_on_utc <= datetime.now(timezone.utc)):
            return None
        instance.last_used_on_utc = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(instance)
        return instance
