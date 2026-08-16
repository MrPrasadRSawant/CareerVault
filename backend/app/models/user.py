from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UuidPk
from app.models.enums import UserRole


class User(UuidPk, Base, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    failed_login_attempts: Mapped[int] = mapped_column(
        Integer, default=0, server_default="0", nullable=False
    )
    locked_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    terms_accepted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    terms_accepted_version: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )
    terms_accepted_content: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            native_enum=False,
            length=30,
            create_constraint=True,
            validate_strings=True,
        ),
        default=UserRole.JOB_APPLICANT,
        index=True,
    )

    opportunities = relationship(
        "JobOpportunity",
        cascade="all, delete-orphan",
        foreign_keys="JobOpportunity.created_by",
    )
    api_keys = relationship("ApiKey", back_populates="user", cascade="all, delete-orphan")
    applications = relationship(
        "Application", back_populates="user", cascade="all, delete-orphan"
    )
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    cover_letters = relationship(
        "CoverLetter", back_populates="user", cascade="all, delete-orphan"
    )
    notifications = relationship(
        "Notification", back_populates="user", cascade="all, delete-orphan"
    )
    auth_sessions = relationship(
        "AuthSession", back_populates="user", cascade="all, delete-orphan"
    )
    login_audit_logs = relationship("LoginAuditLog", back_populates="user")
    exception_logs = relationship("ExceptionLog", back_populates="user")
