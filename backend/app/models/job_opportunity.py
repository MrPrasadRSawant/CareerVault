import uuid
from datetime import date

from sqlalchemy import JSON, Date, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UuidPk
from app.models.enums import OpportunityStatus


class JobOpportunity(UuidPk, Base, TimestampMixin):
    __tablename__ = "job_opportunities"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    company_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("companies.id"), index=True
    )

    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    application_link: Mapped[str | None] = mapped_column(String(500))
    salary_range: Mapped[str | None] = mapped_column(String(100))
    required_skills: Mapped[list | None] = mapped_column(JSON)
    experience_level: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[OpportunityStatus] = mapped_column(
        Enum(OpportunityStatus, native_enum=False, length=30),
        default=OpportunityStatus.SAVED,
        index=True,
    )
    source: Mapped[str | None] = mapped_column(String(255))
    posted_date: Mapped[date | None] = mapped_column(Date)
    deadline: Mapped[date | None] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text)

    user = relationship("User", back_populates="opportunities")
    company = relationship("Company", back_populates="opportunities")
    applications = relationship(
        "Application", back_populates="opportunity", cascade="all, delete-orphan"
    )
