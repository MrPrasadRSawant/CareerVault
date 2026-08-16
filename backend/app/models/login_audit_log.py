import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, SmallInteger, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UuidPk
from app.models.enums import (
    AuthEventType,
    AuthFailureReason,
    AuthOutcome,
    UserRole,
)


class LoginAuditLog(UuidPk, Base):
    __tablename__ = "login_audit_logs"

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    auth_session_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("auth_sessions.id", ondelete="SET NULL"), index=True
    )
    event_type: Mapped[AuthEventType] = mapped_column(
        Enum(
            AuthEventType,
            native_enum=False,
            length=20,
            create_constraint=True,
            validate_strings=True,
        ),
        index=True,
    )
    outcome: Mapped[AuthOutcome] = mapped_column(
        Enum(
            AuthOutcome,
            native_enum=False,
            length=20,
            create_constraint=True,
            validate_strings=True,
        ),
        index=True,
    )
    failure_reason: Mapped[AuthFailureReason | None] = mapped_column(
        Enum(
            AuthFailureReason,
            native_enum=False,
            length=30,
            create_constraint=True,
            validate_strings=True,
        )
    )
    role: Mapped[UserRole | None] = mapped_column(
        Enum(
            UserRole,
            native_enum=False,
            length=30,
            create_constraint=True,
            validate_strings=True,
        ),
        index=True,
    )
    identifier_hash: Mapped[str] = mapped_column(String(64), index=True)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    ip_address: Mapped[str | None] = mapped_column(String(45))
    user_agent: Mapped[str | None] = mapped_column(String(512))
    http_status: Mapped[int] = mapped_column(SmallInteger)

    user = relationship("User", back_populates="login_audit_logs")
    auth_session = relationship("AuthSession", back_populates="login_events")
