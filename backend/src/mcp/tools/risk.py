"""Risk MCP tool."""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.mcp.models import (
    MCPToolRequest,
    MCPToolResponse,
)
from src.mcp.tools.base import (
    BaseTool,
)
from src.mcp.types import (
    MCPTool,
)
from src.modules.risk.service import (
    RiskService,
)


class RiskTool(BaseTool):
    """
    MCP tool exposing enterprise risk analysis.

    Handles:
    - business risk scoring
    - prediction impact analysis
    - mitigation recommendations
    """


    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            tool_name=MCPTool.RISK,
        )

        self.service = RiskService(
            db,
        )


    async def _execute(
        self,
        request: MCPToolRequest,
    ) -> MCPToolResponse:
        """
        Execute risk analysis.
        """

        result = self.service.analyze(
            created_by=request.user_id,
        )


        return MCPToolResponse(
            success=True,
            data={
                "risk": result,
            },
            message="Risk analysis completed.",
        )