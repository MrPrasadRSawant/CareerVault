from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="Job opportunity and application management platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/ai/openapi.json", include_in_schema=False)
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
            if path.startswith("/ai/") and path != "/ai/openapi.json"
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


@app.get("/health", tags=["health"])
def health() -> dict:
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.APP_ENV}
