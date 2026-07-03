"""Embedded MCP server."""

from __future__ import annotations

from src.mcp.models import (
    MCPToolRequest,
    MCPToolResponse,
)
from src.mcp.registry import MCPRegistry


class MCPServer:
    """
    Embedded Model Context Protocol server.

    The server is responsible for locating the requested tool
    and delegating execution to it.

    It intentionally contains no business logic.
    """

    def __init__(
        self,
        registry: MCPRegistry,
    ) -> None:

        self.registry = registry

    async def invoke(
        self,
        request: MCPToolRequest,
    ) -> MCPToolResponse:
        """
        Execute an MCP tool.
        """

        tool = self.registry.get(
            request.tool,
        )

        return await tool.invoke(
            request,
        )