"""
Logging configuration for SynapseOS.

This module centralizes application-wide logging configuration,
ensuring consistent formatting and log levels across all
components. Logging should be configured once during application
startup before any application services are initialized.
"""

from __future__ import annotations

import logging
import sys

from src.core.config import settings


def configure_logging() -> None:
    """
    Configure the application's root logger.

    The configuration applies to both the application and
    third-party libraries that use Python's logging framework.
    """

    logging.basicConfig(
        level=settings.log_level.upper(),
        format=(
            "%(asctime)s | "
            "%(levelname)-8s | "
            "%(name)s | "
            "%(message)s"
        ),
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        force=True,
    )