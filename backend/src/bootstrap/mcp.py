"""Bootstrap MCP infrastructure."""

from __future__ import annotations

from src.mcp.client import MCPClient
from src.mcp.registry import MCPRegistry
from src.mcp.server import MCPServer
from src.mcp.service import MCPService
from src.mcp.tools.knowledge import KnowledgeTool


def create_mcp_service() -> MCPService:
    """
    Create the internal MCP stack.

    Flow:
        MCPService
            ↓
        MCPClient
            ↓
        MCPServer
            ↓
        MCPRegistry
            ↓
        MCPTools
    """

    registry = MCPRegistry()

    # Register tools
    registry.register(
        KnowledgeTool(),
    )

    server = MCPServer(
        registry,
    )

    client = MCPClient(
        server,
    )

    return MCPService(
        client,
    )