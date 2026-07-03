"""Knowledge MCP tool."""

from __future__ import annotations

from src.mcp.models import (
    MCPToolRequest,
    MCPToolResponse,
)
from src.mcp.tools.base import BaseTool
from src.mcp.types import MCPTool
from src.modules.knowledge.service import KnowledgeService


class KnowledgeTool(BaseTool):
    """
    MCP tool exposing enterprise knowledge retrieval.
    """

    def __init__(self) -> None:
        super().__init__(
            tool_name=MCPTool.KNOWLEDGE_SEARCH,
        )

        self.service = KnowledgeService()

    async def _execute(
        self,
        request: MCPToolRequest,
    ) -> MCPToolResponse:

        query = request.parameters.get("query")

        if not query:
            return MCPToolResponse(
                success=False,
                message="Missing required parameter: query.",
            )

        response = self.service.answer(
            query=query,
        )

        return MCPToolResponse(
            success=True,
            data={
                "answer": response.answer,
                "sources": [
                    source.model_dump()
                    for source in response.sources
                ],
                "metrics": response.metrics.model_dump(),
            },
        )