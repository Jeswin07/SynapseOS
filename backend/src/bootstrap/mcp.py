"""Bootstrap MCP infrastructure."""

from __future__ import annotations
from sqlalchemy.orm import Session

from src.mcp.client import MCPClient
from src.mcp.registry import MCPRegistry
from src.mcp.server import MCPServer
from src.mcp.service import MCPService
from src.mcp.tools.knowledge import KnowledgeTool
from src.mcp.tools.analytics_tool import AnalyticsTool
from src.mcp.tools.forecast import ForecastTool

def create_mcp_service(
        db:Session
) -> MCPService:
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

    registry.register(
        AnalyticsTool(db)
    )

    registry.register(
        ForecastTool(db)
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