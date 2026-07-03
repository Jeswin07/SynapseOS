"""Base class for all MCP tools."""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.mcp.models import (
    MCPToolRequest,
    MCPToolResponse,
)
from src.mcp.types import MCPTool


class BaseTool(ABC):
    """
    Base class for every MCP tool.
    """

    tool_name: MCPTool

    def __init__(
        self,
        tool_name: MCPTool,
    ) -> None:
        self.tool_name = tool_name

    async def invoke(
        self,
        request: MCPToolRequest,
    ) -> MCPToolResponse:
        """
        Executes the MCP tool.
        """

        return await self._execute(
            request,
        )

    @abstractmethod
    async def _execute(
        self,
        request: MCPToolRequest,
    ) -> MCPToolResponse:
        """
        Executes tool-specific logic.
        """