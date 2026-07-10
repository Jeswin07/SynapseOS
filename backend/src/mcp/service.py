"""High-level interface for executing MCP tools."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from src.mcp.client import MCPClient
from src.mcp.models import (
    MCPToolRequest,
    MCPToolResponse,
)
from src.mcp.types import MCPTool


class MCPService:
    """
    High-level service used by AI agents.

    This service hides the underlying MCP implementation
    from the agent layer.
    """

    def __init__(
        self,
        client: MCPClient,
    ) -> None:
        self.client = client

    async def execute(
        self,
        *,
        tool: MCPTool,
        tenant_id: UUID,
        user_id: UUID,
        query: str = "",
        **parameters: Any,
    ) -> MCPToolResponse:
        """
        Execute an MCP tool.
        """

        request = MCPToolRequest(
            tool=tool,
            tenant_id=tenant_id,
            user_id=user_id,
            query=query,
            parameters=parameters,
        )

        return await self.client.invoke(
            request,
        )