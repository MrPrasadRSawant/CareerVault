from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=settings.database_connect_args,
    pool_pre_ping=True,
    **(
        {}
        if settings.DATABASE_URL.startswith("sqlite")
        else {
            "pool_size": settings.DATABASE_POOL_SIZE,
            "max_overflow": settings.DATABASE_MAX_OVERFLOW,
            "pool_timeout": settings.DATABASE_POOL_TIMEOUT_SECONDS,
            "pool_recycle": settings.DATABASE_POOL_RECYCLE_SECONDS,
        }
    ),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
