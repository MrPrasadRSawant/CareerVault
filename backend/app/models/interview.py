import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UuidPk
from app.models.enums import InterviewStatus, InterviewType


class Interview(UuidPk, Base, TimestampMixin):
    __tablename__ = "interviews"

    application_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("applications.id"), index=True
    )

    scheduled_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    type: Mapped[InterviewType] = mapped_column(
        Enum(InterviewType, native_enum=False, length=30),
        default=InterviewType.VIDEO,
    )
    location_or_link: Mapped[str | None] = mapped_column(String(500))
    status: Mapped[InterviewStatus] = mapped_column(
        Enum(InterviewStatus, native_enum=False, length=30),
        default=InterviewStatus.SCHEDULED,
        index=True,
    )
    notes: Mapped[str | None] = mapped_column(Text)

    application = relationship("Application", back_populates="interviews")
