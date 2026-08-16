import uuid
from datetime import datetime

from pydantic import EmailStr, Field

from app.schemas.common import ORMModel
from app.models.enums import UserRole


class UserCreate(ORMModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(ORMModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=255)


class UserRead(ORMModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    is_active: bool
    role: UserRole
    created_at: datetime
