from datetime import datetime

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.enums import UserRole
from app.models.user import User


class AdminRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_users(
        self,
        *,
        search: str | None = None,
        is_active: bool | None = None,
        role: UserRole | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[User], int]:
        filters = []
        if search:
            pattern = f"%{search.strip()}%"
            filters.append(
                or_(User.full_name.ilike(pattern), User.email.ilike(pattern))
            )
        if is_active is not None:
            filters.append(User.is_active.is_(is_active))
        if role is not None:
            filters.append(User.role == role)

        total = (
            self.db.scalar(select(func.count()).select_from(User).where(*filters))
            or 0
        )
        users = list(
            self.db.scalars(
                select(User)
                .where(*filters)
                .order_by(User.created_at.desc())
                .limit(limit)
                .offset(offset)
            ).all()
        )
        return users, total

    def get_user(self, user_id) -> User | None:
        return self.db.scalar(select(User).where(User.id == user_id))

    def count_users(
        self,
        *,
        is_active: bool | None = None,
        role: UserRole | None = None,
        created_since: datetime | None = None,
    ) -> int:
        filters = []
        if is_active is not None:
            filters.append(User.is_active.is_(is_active))
        if role is not None:
            filters.append(User.role == role)
        if created_since is not None:
            filters.append(User.created_at >= created_since)
        return (
            self.db.scalar(select(func.count()).select_from(User).where(*filters))
            or 0
        )

    def registrations_since(
        self, created_since: datetime
    ) -> list[tuple[datetime, UserRole]]:
        return [
            (row[0], row[1])
            for row in self.db.execute(
                select(User.created_at, User.role).where(
                    User.created_at >= created_since
                )
            ).all()
        ]

    def set_user_active(self, user: User, is_active: bool) -> User:
        user.is_active = is_active
        self.db.commit()
        self.db.refresh(user)
        return user
