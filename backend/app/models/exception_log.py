import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UuidPk


class ExceptionLog(UuidPk, Base):
    __tablename__ = "exception_logs"

    request_id: Mapped[str] = mapped_column(
        String(36), unique=True, index=True
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    method: Mapped[str] = mapped_column(String(10))
    route_template: Mapped[str] = mapped_column(String(500))
    query_parameter_names: Mapped[str | None] = mapped_column(String(1000))
    status_code: Mapped[int] = mapped_column(Integer, index=True)
    exception_type: Mapped[str] = mapped_column(String(255), index=True)
    message: Mapped[str] = mapped_column(Text)
    traceback: Mapped[str] = mapped_column(Text)
    fingerprint: Mapped[str] = mapped_column(String(64), index=True)
    ip_address: Mapped[str | None] = mapped_column(String(45))
    user_agent: Mapped[str | None] = mapped_column(String(512))
    app_environment: Mapped[str] = mapped_column(String(50))
    is_handled: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="0", nullable=False
    )

    user = relationship("User", back_populates="exception_logs")
