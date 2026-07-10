"""Shared models for the MCP tool layer."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from src.mcp.types import MCPTool


class MCPToolRequest(BaseModel):
    """
    Standard request passed to an MCP tool.
    """

    tool: MCPTool

    tenant_id: UUID

    user_id: UUID

    parameters: dict[str, Any] = Field(
        default_factory=dict,
    )

    query: str = ""


class MCPToolResponse(BaseModel):
    """
    Standard response returned by an MCP tool.
    """

    success: bool = True

    data: dict[str, Any] = Field(
        default_factory=dict,
    )

    message: str | None = None