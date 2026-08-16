import ipaddress
import re
from dataclasses import dataclass

from fastapi import Request

CONTROL_CHARACTERS = re.compile(r"[\x00-\x1f\x7f]+")


@dataclass(frozen=True)
class AuthClientContext:
    ip_address: str | None
    user_agent: str | None


def _normalized_ip(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return ipaddress.ip_address(value).compressed
    except ValueError:
        return None


def _sanitized_user_agent(value: str | None) -> str | None:
    if not value:
        return None
    sanitized = CONTROL_CHARACTERS.sub(" ", value).strip()
    return sanitized[:512] or None


def auth_client_context(request: Request) -> AuthClientContext:
    # Use the ASGI client address only. Proxy headers must be validated by the
    # trusted deployment proxy/server before they are reflected in this value.
    return AuthClientContext(
        ip_address=_normalized_ip(
            request.client.host if request.client is not None else None
        ),
        user_agent=_sanitized_user_agent(request.headers.get("user-agent")),
    )
