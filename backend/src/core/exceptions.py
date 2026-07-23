"""
Global exception handlers for SynapseOS.

This module centralizes exception handling for the entire application.

Goals
-----
- Return consistent API error responses.
- Log unexpected exceptions with stack traces.
- Prevent internal implementation details from leaking to clients.
- Improve observability for production deployments.

All exception handlers registered here automatically apply to every
endpoint in the application.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger("synapseos")


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all global exception handlers.

    This function should be called exactly once during application
    startup after the FastAPI application has been created.

    Args:
        app:
            FastAPI application instance.
    """

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        """
        Handle request validation errors.

        Triggered when incoming request data fails Pydantic validation.
        """

        logger.warning(
            "Request validation failed.",
            extra={
                "path": request.url.path,
                "method": request.method,
            },
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": "Validation Error",
                "details": exc.errors(),
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        """
        Handle expected HTTP exceptions.
        """

        logger.warning(
            "HTTP exception raised.",
            extra={
                "status_code": exc.status_code,
                "path": request.url.path,
                "method": request.method,
            },
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": exc.detail,
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """
        Handle unexpected server exceptions.

        Any exception not explicitly handled elsewhere reaches this
        handler, ensuring the client receives a safe response while
        the server logs the complete stack trace.
        """

        logger.exception(
            "Unhandled application exception.",
            extra={
                "path": request.url.path,
                "method": request.method,
            },
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": "Internal Server Error",
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )