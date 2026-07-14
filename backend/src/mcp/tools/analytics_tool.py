"""Analytics MCP tool."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from src.mcp.models import (
    MCPToolRequest,
    MCPToolResponse,
)
from src.mcp.tools.base import BaseTool
from src.mcp.types import MCPTool
from src.modules.analytics.service import (
    AnalyticsService,
)


class AnalyticsTool(BaseTool):
    """
    MCP tool exposing analytics capability.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            tool_name=MCPTool.ANALYTICS,
        )

        self.service = AnalyticsService(
            db,
        )


    async def _execute(
        self,
        request: MCPToolRequest,
    ) -> MCPToolResponse:
        """
        Run analytics.
        """

        dataset_version_id = uuid.UUID(
            request.parameters[
                "dataset_version_id"
            ]
        )


        analytics = self.service.analyze(
            dataset_version_id,
        )


        return MCPToolResponse(
            success=True,
            data={
                "analytics": analytics,
            },
            message="Analytics completed.",
        )