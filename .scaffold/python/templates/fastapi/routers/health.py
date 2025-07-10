"""
Health check endpoints for {{name}}
"""

from datetime import datetime
from fastapi import APIRouter, Depends
from ..models import HealthResponse
from ..database import get_db_health
from ..config import settings

router = APIRouter()


@router.get("/", response_model=HealthResponse)
async def health_check():
    """Basic health check endpoint."""
    db_health = await get_db_health()
    
    return HealthResponse(
        status="healthy",
        version="{{version}}",
        timestamp=datetime.utcnow(),
        {{#if database}}
        database=db_health["status"],
        {{/if}}
    )


@router.get("/ready")
async def readiness_check():
    """Readiness check for Kubernetes."""
    db_health = await get_db_health()
    
    {{#if database}}
    if db_health["status"] != "healthy":
        return {"status": "not_ready", "reason": "database_unhealthy"}
    {{/if}}
    
    return {"status": "ready"}


@router.get("/live")
async def liveness_check():
    """Liveness check for Kubernetes."""
    return {"status": "alive"}


@router.get("/metrics")
async def metrics():
    """Basic metrics endpoint."""
    return {
        "service": "{{name}}",
        "version": "{{version}}",
        "environment": settings.ENVIRONMENT,
        "uptime": "unknown",  # TODO: Implement uptime tracking
        "timestamp": datetime.utcnow(),
    }