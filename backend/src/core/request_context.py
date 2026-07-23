"""
Request context management for SynapseOS.

This module provides request-scoped context that can be accessed
from anywhere during the lifetime of an HTTP request.

The context is stored using Python ContextVars, making it safe
for asynchronous FastAPI applications.

Context available:
- request_id
- tenant_id
- user_id
"""

from __future__ import annotations

from contextvars import ContextVar

# ---------------------------------------------------------
# Context Variables
# ---------------------------------------------------------

request_id_context: ContextVar[str] = ContextVar(
    "request_id",
    default="-",
)

tenant_id_context: ContextVar[str] = ContextVar(
    "tenant_id",
    default="-",
)

user_id_context: ContextVar[str] = ContextVar(
    "user_id",
    default="-",
)


# ---------------------------------------------------------
# Request ID
# ---------------------------------------------------------

def get_request_id() -> str:
    """Return current request ID."""
    return request_id_context.get()


def set_request_id(request_id: str) -> None:
    """Store current request ID."""
    request_id_context.set(request_id)


# ---------------------------------------------------------
# Tenant ID
# ---------------------------------------------------------

def get_tenant_id() -> str:
    """Return current tenant ID."""
    return tenant_id_context.get()


def set_tenant_id(tenant_id: str) -> None:
    """Store current tenant ID."""
    tenant_id_context.set(tenant_id)


# ---------------------------------------------------------
# User ID
# ---------------------------------------------------------

def get_user_id() -> str:
    """Return current user ID."""
    return user_id_context.get()


def set_user_id(user_id: str) -> None:
    """Store current user ID."""
    user_id_context.set(user_id)