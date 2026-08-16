import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UuidPk
from app.models.enums import AuthEventType, AuthSessionEndReason


class AuthSession(UuidPk, Base):
    __tablename__ = "auth_sessions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    auth_method: Mapped[AuthEventType] = mapped_column(
        Enum(
            AuthEventType,
            native_enum=False,
            length=20,
            create_constraint=True,
            validate_strings=True,
        )
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    end_reason: Mapped[AuthSessionEndReason | None] = mapped_column(
        Enum(
            AuthSessionEndReason,
            native_enum=False,
            length=30,
            create_constraint=True,
            validate_strings=True,
        )
    )
    ip_address: Mapped[str | None] = mapped_column(String(45))
    user_agent: Mapped[str | None] = mapped_column(String(512))

    user = relationship("User", back_populates="auth_sessions")
    login_events = relationship("LoginAuditLog", back_populates="auth_session")
