from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.router import api_router
from app.core.config import settings
from app.core.database import SessionLocal
from app.core.exception_logging import (
    record_unexpected_exception,
    request_id_for,
)

API_V1_PREFIX = "/api/v1"


app = FastAPI(
    title=settings.APP_NAME,
    description="Job opportunity and application management platform",
    version="0.1.0",
    docs_url=f"{API_V1_PREFIX}/docs" if settings.ENABLE_API_DOCS else None,
    redoc_url=f"{API_V1_PREFIX}/redoc" if settings.ENABLE_API_DOCS else None,
    openapi_url=f"{API_V1_PREFIX}/openapi.json" if settings.ENABLE_API_DOCS else None,
)
app.state.exception_log_session_factory = SessionLocal


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = request_id_for(request)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    request_id = request_id_for(request)
    if exc.status_code >= 500:
        request_id = record_unexpected_exception(
            request,
            exc,
            status_code=exc.status_code,
            is_handled=True,
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers={**(exc.headers or {}), "X-Request-ID": request_id},
    )


@app.exception_handler(Exception)
async def unexpected_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    request_id = record_unexpected_exception(request, exc)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected server error occurred",
            "request_id": request_id,
        },
        headers={"X-Request-ID": request_id},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get(f"{API_V1_PREFIX}/ai/openapi.json", include_in_schema=False)
def ai_openapi_schema(request: Request) -> JSONResponse:
    """Return the isolated OpenAPI contract intended for Custom GPT Actions."""
    full_schema = app.openapi()
    ai_schema = {
        "openapi": full_schema["openapi"],
        "info": {
            "title": "CareerVault AI Actions",
            "description": "Create, search, and manage draft job opportunities for the authenticated CareerVault user.",
            "version": full_schema["info"].get("version", "1.0.0"),
        },
        "servers": [{"url": str(request.base_url).rstrip("/")}],
        "paths": {
            path: definition
            for path, definition in full_schema.get("paths", {}).items()
            if path.startswith(f"{API_V1_PREFIX}/ai/") and path != f"{API_V1_PREFIX}/ai/openapi.json"
        },
        "components": {
            "schemas": full_schema.get("components", {}).get("schemas", {}),
            "securitySchemes": {
                "APIKeyHeader": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-CareerVault-Key",
                }
            },
        },
    }
    return JSONResponse(ai_schema)


@app.get(f"{API_V1_PREFIX}/health", tags=["health"])
def health() -> dict:
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.APP_ENV}


@app.get(f"{API_V1_PREFIX}/email-agent/openapi.json", include_in_schema=False)
def email_agent_openapi_schema(request: Request) -> JSONResponse:
    """Return the isolated contract for n8n and email-classification agents."""
    full_schema = app.openapi()
    prefix = f"{API_V1_PREFIX}/email-agent/"
    return JSONResponse(
        {
            "openapi": full_schema["openapi"],
            "info": {
                "title": "CareerVault Email Agent API",
                "description": "Match recruiter email replies to applications and record their outcomes.",
                "version": full_schema["info"].get("version", "1.0.0"),
            },
            "servers": [{"url": str(request.base_url).rstrip("/")}],
            "paths": {
                path: definition
                for path, definition in full_schema.get("paths", {}).items()
                if path.startswith(prefix) and path != f"{prefix}openapi.json"
            },
            "components": {
                "schemas": full_schema.get("components", {}).get("schemas", {}),
                "securitySchemes": {
                    "APIKeyHeader": {
                        "type": "apiKey",
                        "in": "header",
                        "name": "X-CareerVault-Key",
                    }
                },
            },
        }
    )
