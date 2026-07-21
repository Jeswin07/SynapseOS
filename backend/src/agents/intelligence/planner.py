"""Hybrid intelligence planner."""

from __future__ import annotations

from src.agents.common.json_parser import parse_llm_json
from src.agents.common.llm import LLMClient
from src.agents.intelligence.schemas import (
    IntelligencePlan,
)
from src.mcp.types import MCPTool


class IntelligencePlanner:
    """
    Fast MCP tool router with LLM fallback.
    """


    def __init__(self) -> None:
        self.llm = LLMClient()


    async def plan(
        self,
        query: str,
    ) -> IntelligencePlan:


        q = query.lower()


        if any(
            x in q
            for x in [
                "risk",
                "threat",
                "problem",
                "issue",
                "impact",
            ]
        ):
            print("FAST ROUTER i")

            return IntelligencePlan(
                tools=[
                    MCPTool.RISK,
                ],
                sections=[
                    "risk",
                ],
                reasoning="Matched risk analysis intent.",
            )


        if any(
            x in q
            for x in [
                "predict",
                "prediction",
                "churn",
                "delay",
            ]
        ):
            print("FAST ROUTER i")

            return IntelligencePlan(
                tools=[
                    MCPTool.PREDICTION,
                ],
                sections=[
                    "prediction",
                ],
                reasoning="Matched ML prediction intent.",
            )


        if any(
            x in q
            for x in [
                "forecast",
                "future",
                "next month",
                "next week",
                "trend",
            ]
        ):


            return IntelligencePlan(
                tools=[
                    MCPTool.FORECAST,
                ],
                sections=[
                    "forecast",
                ],
                reasoning="Matched forecasting intent.",
            )


        if any(
            x in q
            for x in [
                "sales",
                "revenue",
                "customer",
                "product",
                "seller",
                "analytics",
                "kpi",
                "review",
                "performance",
            ]
        ):
            print("FAST ROUTER i")

            return IntelligencePlan(
                tools=[
                    MCPTool.ANALYTICS,
                ],
                sections=[
                    "analytics",
                ],
                reasoning="Matched analytics intent.",
            )


        # fallback LLM

        prompt = f"""
Choose MCP tools.

Tools:
analytics
forecast
prediction
risk


Question:
{query}


Return JSON:
{{
"tools":["analytics"],
"sections":["revenue"],
"reasoning":"..."
}}

Return ONLY JSON.

No markdown.

No explanation.

No code block.

No text before JSON.

No text after JSON.
"""


        response = await self.llm.generate(
            prompt,
        )


        data = parse_llm_json(
            response,
        )


        return IntelligencePlan(
            tools=[
                MCPTool(tool)
                for tool in data["tools"]
            ],
            sections=data["sections"],
            reasoning=data["reasoning"],
        )