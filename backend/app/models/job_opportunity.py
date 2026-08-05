import uuid
from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UuidPk
from app.models.enums import OpportunityStatus


class JobOpportunity(UuidPk, Base):
    __tablename__ = "job_opportunities"

    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    created_on_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    updated_on_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), index=True)
    company_name: Mapped[str | None] = mapped_column(String(255), index=True)
    post_url: Mapped[str | None] = mapped_column(String(500))
    company_career_page: Mapped[str | None] = mapped_column(String(500))
    company_url: Mapped[str | None] = mapped_column(String(500))
    posted_on_utc: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    job_location: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    required_skills: Mapped[list | None] = mapped_column(JSON)
    experience_level: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[OpportunityStatus] = mapped_column(
        Enum(OpportunityStatus, native_enum=False, length=30),
        default=OpportunityStatus.SAVED,
        index=True,
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

    applications = relationship(
        "Application", back_populates="opportunity", cascade="all, delete-orphan"
    )
