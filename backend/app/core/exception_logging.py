import hashlib
import logging
import re
import traceback
import uuid
from datetime import datetime, timezone

from fastapi import Request
from jwt import InvalidTokenError

from app.core.config import settings
from app.core.database import SessionLocal
from app.core.request_context import auth_client_context
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.exception_log_repository import ExceptionLogRepository

logger = logging.getLogger(__name__)

CONTROL_CHARACTERS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]+")
EMAIL_ADDRESS = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
JWT_VALUE = re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b")
SENSITIVE_ASSIGNMENT = re.compile(
    r"(?i)\b(password|passwd|secret|token|authorization|cookie)"
    r"\s*[:=]\s*([^\s,;]+)"
)
DATABASE_PARAMETERS = re.compile(r"(?is)\[parameters?:.*?\]")

MAX_MESSAGE_LENGTH = 4_000
MAX_TRACEBACK_LENGTH = 32_000


def request_id_for(request: Request) -> str:
    existing = getattr(request.state, "request_id", None)
    if existing:
        return str(existing)
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    return request_id


def _redact(value: str, maximum_length: int) -> str:
    value = CONTROL_CHARACTERS.sub(" ", value)
    value = EMAIL_ADDRESS.sub("[email-redacted]", value)
    value = JWT_VALUE.sub("[token-redacted]", value)
    value = SENSITIVE_ASSIGNMENT.sub(r"\1=[redacted]", value)
    value = DATABASE_PARAMETERS.sub("[parameters-redacted]", value)
    return value.strip()[:maximum_length]


def _authenticated_user_id(request: Request) -> uuid.UUID | None:
    authorization = request.headers.get("authorization", "")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    try:
        return uuid.UUID(str(decode_access_token(token).get("sub")))
    except (InvalidTokenError, TypeError, ValueError):
        return None


def _route_template(request: Request) -> str:
    route = request.scope.get("route")
    route_path = getattr(route, "path", None)
    return str(route_path)[:500] if route_path else "<unresolved-route>"


def _fingerprint(exc: Exception, route_template: str) -> str:
    frames = traceback.extract_tb(exc.__traceback__)
    final_frame = frames[-1] if frames else None
    location = (
        f"{final_frame.name}:{final_frame.lineno}" if final_frame else "unknown"
    )
    source = f"{type(exc).__name__}|{route_template}|{location}"
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def record_unexpected_exception(
    request: Request,
    exc: Exception,
    *,
    status_code: int = 500,
    is_handled: bool = False,
) -> str:
    request_id = request_id_for(request)
    route_template = _route_template(request)
    trace = "".join(
        traceback.format_exception(type(exc), exc, exc.__traceback__)
    )
    query_names = sorted(
        {
            CONTROL_CHARACTERS.sub("", name)[:80]
            for name in request.query_params.keys()
            if name
        }
    )
    client = auth_client_context(request)
    try:
        session_factory = getattr(
            request.app.state,
            "exception_log_session_factory",
            SessionLocal,
        )
        with session_factory() as db:
            authenticated_user_id = _authenticated_user_id(request)
            user_id = (
                authenticated_user_id
                if authenticated_user_id is not None
                and db.get(User, authenticated_user_id) is not None
                else None
            )
            ExceptionLogRepository(db).record(
                request_id=request_id,
                user_id=user_id,
                occurred_at=datetime.now(timezone.utc),
                method=request.method[:10],
                route_template=route_template,
                query_parameter_names=(
                    ", ".join(query_names)[:1000] or None
                ),
                status_code=status_code,
                exception_type=type(exc).__name__[:255],
                message=_redact(str(exc) or type(exc).__name__, MAX_MESSAGE_LENGTH),
                traceback=_redact(trace, MAX_TRACEBACK_LENGTH),
                fingerprint=_fingerprint(exc, route_template),
                ip_address=client.ip_address,
                user_agent=client.user_agent,
                app_environment=settings.APP_ENV[:50],
                is_handled=is_handled,
            )
    except Exception:
        logger.exception(
            "Failed to persist exception log for request %s", request_id
        )
    return request_id
