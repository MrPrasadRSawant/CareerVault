import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, Enum, Float, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UuidPk
from app.models.enums import EmailFollowUpOutcome


class EmailFollowUp(UuidPk, Base, TimestampMixin):
    __tablename__ = "email_follow_ups"
    __table_args__ = (
        UniqueConstraint(
            "application_id",
            "external_message_id",
            name="uq_email_follow_ups_application_message",
        ),
    )

    application_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"), index=True
    )
    external_message_id: Mapped[str | None] = mapped_column(String(500), index=True)
    thread_id: Mapped[str | None] = mapped_column(String(500), index=True)
    subject: Mapped[str] = mapped_column(String(500))
    sender_email: Mapped[str] = mapped_column(String(320), index=True)
    sender_name: Mapped[str | None] = mapped_column(String(255))
    recipient_emails: Mapped[list[str] | None] = mapped_column(JSON)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    body_text: Mapped[str | None] = mapped_column(Text)
    outcome: Mapped[EmailFollowUpOutcome] = mapped_column(
        Enum(EmailFollowUpOutcome, native_enum=False, length=30),
        default=EmailFollowUpOutcome.PENDING,
        index=True,
    )
    reason: Mapped[str | None] = mapped_column(Text)
    reason_category: Mapped[str | None] = mapped_column(String(100), index=True)
    ai_confidence: Mapped[float | None] = mapped_column(Float)
    raw_metadata: Mapped[dict | None] = mapped_column(JSON)

    application = relationship("Application", back_populates="email_follow_ups")
