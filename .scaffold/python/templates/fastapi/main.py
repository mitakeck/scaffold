"""
{{name}} FastAPI Application
{{description}}

Generated on {{date}} by {{author}}
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog
import uvicorn

from .config import settings
from .database import init_db
from .routers import health, users


# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting {{name}} service", version="{{version}}")
    
    {{#if database}}
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    {{/if}}
    
    yield
    
    # Shutdown
    logger.info("Shutting down {{name}} service")


# Create FastAPI application
app = FastAPI(
    title="{{name}}",
    description="{{description}}",
    version="{{version}}",
    lifespan=lifespan,
    {{#if docs}}
    docs_url="/docs",
    redoc_url="/redoc",
    {{else}}
    docs_url=None,
    redoc_url=None,
    {{/if}}
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error("Unhandled exception", exc_info=exc, path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "{{name}}",
        "version": "{{version}}",
        "description": "{{description}}",
        "status": "running"
    }


if __name__ == "__main__":
    uvicorn.run(
        "{{module}}.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )