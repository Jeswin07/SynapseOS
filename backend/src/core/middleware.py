"""
Application middleware for SynapseOS.

Registers middleware responsible for request tracing,
logging, timing, and context propagation.
"""

from __future__ import annotations

import logging
import time
import uuid

from fastapi import FastAPI, Request

from src.core.request_context import (
    set_request_id,
    set_tenant_id,
    set_user_id,
)

logger = logging.getLogger("synapseos.middleware")


def register_middlewares(app: FastAPI) -> None:
    """
    Register all application middleware.
    """

    @app.middleware("http")
    async def request_logging_middleware(request: Request, call_next):
        """
        Logs every HTTP request and stores request-scoped context.
        """

        request_id = uuid.uuid4().hex

        set_request_id(request_id)

        # --------------------------------------------------
        # Extract optional context
        # --------------------------------------------------

        tenant_id = (
            request.headers.get("X-Tenant-ID")
            or request.headers.get("X-Tenant")
            or "-"
        )

        user_id = "-"

        if hasattr(request.state, "user"):
            user = request.state.user

            if getattr(user, "id", None):
                user_id = str(user.id)

        set_tenant_id(tenant_id)
        set_user_id(user_id)

        client_ip = request.client.host if request.client else "-"

        user_agent = request.headers.get("User-Agent", "-")

        method = request.method

        path = request.url.path

        logger.info(
            "[%s] Started %s %s | ip=%s | tenant=%s | user=%s",
            request_id,
            method,
            path,
            client_ip,
            tenant_id,
            user_id,
        )

        start_time = time.perf_counter()

        try:
            response = await call_next(request)

        except Exception:

            duration_ms = (time.perf_counter() - start_time) * 1000

            logger.exception(
                "[%s] Failed %s %s | %.2f ms",
                request_id,
                method,
                path,
                duration_ms,
            )

            raise

        duration_ms = (time.perf_counter() - start_time) * 1000

        response.headers["X-Request-ID"] = request_id

        if duration_ms >= 3000:

            logger.warning(
                "[%s] Completed %s %s -> %s | %.2f ms | SLOW REQUEST | UA=%s",
                request_id,
                method,
                path,
                response.status_code,
                duration_ms,
                user_agent,
            )

        else:

            logger.info(
                "[%s] Completed %s %s -> %s | %.2f ms | UA=%s",
                request_id,
                method,
                path,
                response.status_code,
                duration_ms,
                user_agent,
            )

        return response