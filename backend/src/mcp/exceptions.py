"""Exceptions used by the MCP layer."""

from __future__ import annotations


class MCPError(Exception):
    """Base exception for all MCP errors."""


class MCPToolNotFoundError(MCPError):
    """Raised when an MCP tool has not been registered."""