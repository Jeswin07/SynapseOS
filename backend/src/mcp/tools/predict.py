"""Prediction MCP tool."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from src.mcp.models import (
    MCPToolRequest,
    MCPToolResponse,
)
from src.mcp.tools.base import BaseTool
from src.mcp.types import MCPTool
from src.modules.prediction.service import (
    PredictionService,
)


class PredictTool(BaseTool):
    """
    MCP tool exposing ML prediction capability.

    Handles:
    - customer churn prediction
    - delivery risk prediction
    """


    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(
            tool_name=MCPTool.PREDICTION,
        )

        self.service = PredictionService(
            db,
        )


    async def _execute(
        self,
        request: MCPToolRequest,
    ) -> MCPToolResponse:
        """
        Execute prediction workflow.
        """


        dataset_version_id = (
            request.parameters.get(
                "dataset_version_id",
            )
        )


        if dataset_version_id is None:

            return MCPToolResponse(
                success=False,
                message="dataset_version_id required.",
            )


        prediction_type = (
            request.parameters.get(
                "prediction_type",
                "customer_churn",
            )
        )


        result = self.service.predict(
             created_by=request.user_id,
            dataset_version_id=uuid.UUID(
                dataset_version_id,
            ),
            prediction_type=prediction_type,
        )


        return MCPToolResponse(
            success=True,
            data={
                "prediction": (
                    result.model_dump()
                ),
            },
            message="Prediction completed.",
        )