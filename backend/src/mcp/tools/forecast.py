"""Forecast MCP tool."""

from __future__ import annotations

from src.mcp.models import (
    MCPToolRequest,
    MCPToolResponse,
)
from src.mcp.tools.base import BaseTool
from src.mcp.types import MCPTool
from src.modules.forecast.service import (
    ForecastService,
)


class ForecastTool(BaseTool):
    """
    Forecast MCP Tool.

    Handles:
    - auto training
    - prediction
    """

    def __init__(
        self,
        db,
    ) -> None:

        super().__init__(
            tool_name=MCPTool.FORECAST,
        )

        self.service = ForecastService(
            db,
        )


    async def _execute(
        self,
        request: MCPToolRequest,
    ) -> MCPToolResponse:


        dataset_version_id = (
            request.parameters.get(
                "dataset_version_id",
            )
        )


        if dataset_version_id is None:

            return MCPToolResponse(
                success=False,
                message="dataset_version_id required",
            )


        try:

            result = (
                await self.service.auto_forecast(
                    dataset_version_id=dataset_version_id,
                    user_id=request.user_id,
                    periods=30,
                    query=request.query
                )
            )


            return MCPToolResponse(
                success=True,
                data={
                    "forecast": result,
                },
            )


        except Exception as exc:

            return MCPToolResponse(
                success=False,
                data={
                    "forecast": {
                        "error": str(exc),
                    }
                },
                message=str(exc),
            )