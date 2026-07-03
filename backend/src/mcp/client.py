"""Internal MCP client."""

from __future__ import annotations

from src.mcp.models import (
    MCPToolRequest,
    MCPToolResponse,
)
from src.mcp.server import MCPServer


class MCPClient:
    """
    Internal client used by AI agents to invoke MCP tools.
    """

    def __init__(
        self,
        server: MCPServer,
    ) -> None:
        self.server = server

    async def invoke(
        self,
        request: MCPToolRequest,
    ) -> MCPToolResponse:
        """
        Invoke an MCP tool.
        """

        return await self.server.invoke(
            request,
        )