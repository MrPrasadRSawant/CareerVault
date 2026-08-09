from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "CareerVault"
    APP_ENV: str = "development"
    ENABLE_API_DOCS: bool = True
    SECRET_KEY: str = "replace-with-a-secure-random-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    DATABASE_URL: str = "sqlite:///./careervault.db"
    # These limits apply to each application worker when PostgreSQL is used.
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_POOL_TIMEOUT_SECONDS: int = 30
    DATABASE_POOL_RECYCLE_SECONDS: int = 1800

    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024

    FRONTEND_URL: str = "http://localhost:9000"

    @property
    def database_connect_args(self) -> dict:
        if self.DATABASE_URL.startswith("sqlite"):
            return {"check_same_thread": False}
        return {}


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
