"""
Database configuration and utilities for {{name}}
"""

{{#if database}}
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import structlog

from .config import settings
from .models import Base

logger = structlog.get_logger()

# Database URL mapping
DATABASE_URLS = {
    "sqlite": f"sqlite:///./{settings.DB_NAME}",
    "postgresql": f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
    "mysql": f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
}

ASYNC_DATABASE_URLS = {
    "sqlite": f"sqlite+aiosqlite:///./{settings.DB_NAME}",
    "postgresql": f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
    "mysql": f"mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
}

# Create engines
database_url = DATABASE_URLS.get("{{database}}")
async_database_url = ASYNC_DATABASE_URLS.get("{{database}}")

if not database_url:
    raise ValueError(f"Unsupported database type: {{database}}")

engine = create_engine(
    database_url,
    echo=settings.DEBUG,
    {{#if (eq database "sqlite")}}
    connect_args={"check_same_thread": False},
    {{/if}}
)

async_engine = create_async_engine(
    async_database_url,
    echo=settings.DEBUG,
    {{#if (eq database "sqlite")}}
    connect_args={"check_same_thread": False},
    {{/if}}
)

# Create session makers
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    """Initialize database tables."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created")


async def get_db():
    """Get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error("Database session error", error=str(e))
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_db_health():
    """Check database health."""
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
            return {"status": "healthy", "database": "{{database}}"}
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        return {"status": "unhealthy", "database": "{{database}}", "error": str(e)}
{{else}}
# No database configuration
async def init_db():
    """Initialize database (no-op when no database is configured)."""
    pass


async def get_db():
    """Get database session (no-op when no database is configured)."""
    yield None


async def get_db_health():
    """Check database health (no-op when no database is configured)."""
    return {"status": "not_configured", "database": "none"}
{{/if}}