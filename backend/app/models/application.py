import uuid
from datetime import date

from sqlalchemy import Date, Enum, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UuidPk
from app.models.enums import ApplicationStatus


class Application(UuidPk, Base, TimestampMixin):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("user_id", "opportunity_id", name="uq_applications_user_opportunity"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    opportunity_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("job_opportunities.id"), index=True
    )
    resume_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("resumes.id"))
    cover_letter_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("cover_letters.id"))

    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus, native_enum=False, length=30),
        default=ApplicationStatus.APPLIED,
        index=True,
    )
    applied_date: Mapped[date | None] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text)

    user = relationship("User", back_populates="applications")
    opportunity = relationship("JobOpportunity", back_populates="applications")
    resume = relationship("Resume", back_populates="applications")
    cover_letter = relationship("CoverLetter", back_populates="applications")
    status_history = relationship(
        "ApplicationStatusHistory",
        back_populates="application",
        cascade="all, delete-orphan",
        order_by="ApplicationStatusHistory.changed_at",
    )
    interviews = relationship(
        "Interview", back_populates="application", cascade="all, delete-orphan"
    )
    follow_ups = relationship(
        "FollowUp", back_populates="application", cascade="all, delete-orphan"
    )
    email_follow_ups = relationship(
        "EmailFollowUp",
        back_populates="application",
        cascade="all, delete-orphan",
        order_by="EmailFollowUp.received_at.desc()",
    )
