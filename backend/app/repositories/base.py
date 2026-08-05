import uuid
from typing import Any, Generic, TypeVar

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.base import Base

Model = TypeVar("Model", bound=Base)


class BaseRepository(Generic[Model]):
    model: type[Model]

    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, id: uuid.UUID) -> Model | None:
        return self.db.get(self.model, id)

    def get_or_404(self, id: uuid.UUID) -> Model:
        instance = self.get(id)
        if instance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found",
            )
        return instance

    def list_all(self, *, limit: int = 100, offset: int = 0) -> list[Model]:
        stmt = (
            select(self.model)
            .order_by(self.model.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.scalars(stmt))

    def count(self) -> int:
        return self.db.scalar(select(func.count()).select_from(self.model)) or 0

    def get_owned(self, user_id: uuid.UUID, id: uuid.UUID) -> Model:
        instance = self.db.scalar(
            select(self.model).where(
                self.model.id == id, self.model.user_id == user_id
            )
        )
        if instance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.model.__name__} not found",
            )
        return instance

    def list_owned(
        self, user_id: uuid.UUID, *, limit: int = 100, offset: int = 0
    ) -> list[Model]:
        stmt = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .order_by(self.model.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(self.db.scalars(stmt))

    def create(self, **values: Any) -> Model:
        instance = self.model(**values)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def update(self, instance: Model, **values: Any) -> Model:
        for key, value in values.items():
            setattr(instance, key, value)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def delete(self, instance: Model) -> None:
        self.db.delete(instance)
        self.db.commit()
