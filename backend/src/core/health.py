"""
Health check endpoints for SynapseOS.

These endpoints are primarily used by:

- Docker health checks
- Kubernetes liveness/readiness probes
- Load balancers
- Monitoring systems
- Manual operational verification

Endpoint Summary
----------------
GET /live
    Indicates whether the application process is alive.

GET /ready
    Indicates whether the application and its required
    infrastructure dependencies are ready to serve requests.

GET /health
    Returns general application health information.
"""

from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from src.core.config import settings
from src.db.session import SessionLocal

router = APIRouter(tags=["Health"])


@router.get("/live", summary="Liveness Probe")
def liveness() -> dict[str, str]:
    """
    Liveness probe.

    This endpoint verifies that the FastAPI application
    process is running.

    External dependencies are intentionally not checked.

    Returns:
        Dictionary containing service status.
    """
    return {"status": "alive"}


@router.get("/ready", summary="Readiness Probe")
def readiness() -> dict[str, str]:
    """
    Readiness probe.

    Confirms that the application can communicate with
    critical infrastructure before accepting traffic.

    Current checks:
        - PostgreSQL connectivity

    Future checks:
        - MinIO
        - Neo4j
        - Qdrant
        - Redis
        - Kafka

    Raises:
        HTTPException:
            If one or more dependencies are unavailable.

    Returns:
        Dictionary indicating service readiness.
    """

    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Database unavailable: {exc}",
        ) from exc

    return {"status": "ready"}


@router.get("/health", summary="Application Health")
def health() -> dict:
    """
    Returns basic application metadata.

    Useful for monitoring dashboards and
    operational verification.

    Returns:
        Dictionary containing application status.
    """

    return {
        "application": settings.app_name,
        "status": "healthy",
        "environment": settings.environment,
        "version": "1.0.0",
        "timestamp": datetime.now(UTC).isoformat(),
    }