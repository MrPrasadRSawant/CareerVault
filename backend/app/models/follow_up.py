import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UuidPk
from app.models.enums import FollowUpStatus


class FollowUp(UuidPk, Base, TimestampMixin):
    __tablename__ = "follow_ups"

    application_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("applications.id"), index=True
    )

    scheduled_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    subject: Mapped[str | None] = mapped_column(String(255))
    message: Mapped[str | None] = mapped_column(Text)
    status: Mapped[FollowUpStatus] = mapped_column(
        Enum(FollowUpStatus, native_enum=False, length=30),
        default=FollowUpStatus.PENDING,
        index=True,
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)

    application = relationship("Application", back_populates="follow_ups")
