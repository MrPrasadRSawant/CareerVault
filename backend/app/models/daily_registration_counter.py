from datetime import date, datetime

from sqlalchemy import CheckConstraint, Date, DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class DailyRegistrationCounter(Base):
    __tablename__ = "daily_registration_counters"
    __table_args__ = (
        CheckConstraint(
            "registration_count >= 0",
            name="registration_count_non_negative",
        ),
    )

    registration_date: Mapped[date] = mapped_column(Date, primary_key=True)
    registration_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
