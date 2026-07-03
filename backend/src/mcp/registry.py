"""Registry for MCP tools."""

from __future__ import annotations

from src.mcp.exceptions import MCPToolNotFoundError
from src.mcp.tools.base import BaseTool
from src.mcp.types import MCPTool


class MCPRegistry:
    """
    Stores all registered MCP tools.
    """

    def __init__(self) -> None:

        self._tools: dict[
            MCPTool,
            BaseTool,
        ] = {}

    def register(
        self,
        tool: BaseTool,
    ) -> None:
        """
        Register an MCP tool.
        """

        self._tools[
            tool.tool_name
        ] = tool

    def get(
        self,
        tool: MCPTool,
    ) -> BaseTool:
        """
        Returns a registered MCP tool.
        """

        toolS = self._tools.get(tool)

        if toolS is None:
            raise MCPToolNotFoundError(
                (
                    f"MCP tool '{tool}' "
                    "has not been registered."
                ),
            )

        return toolS

    def exists(
        self,
        tool: MCPTool,
    ) -> bool:
        """
        Checks whether a tool has been registered.
        """

        return tool in self._tools