"""LLM based intelligence planner."""

from __future__ import annotations

import json

from src.agents.common.llm import LLMClient

from src.agents.intelligence.schemas import (
    IntelligencePlan,
)
from src.agents.common.json_parser import (
    parse_llm_json,
)
from src.mcp.types import MCPTool


class IntelligencePlanner:
    """
    Uses LLM reasoning to decide required tools.
    """


    def __init__(
        self,
    ) -> None:

        self.llm = LLMClient()


    async def plan(
        self,
        query: str,
    ) -> IntelligencePlan:


        prompt = f"""
You are SynapseOS Intelligence Planner.

Your job:
Choose which MCP tools are required.

Available MCP tools:

analytics:
Use for:
- revenue analysis
- sales performance
- customer analytics
- product analytics
- seller analytics
- reviews
- operations
- KPIs
- trends


User question:

{query}


Return ONLY JSON.

Example:

{{
 "tools":["analytics"],
 "sections":["revenue"],
 "reasoning":"Analytics data is required."
}}
"""


        response = await self.llm.generate(
            prompt,
        )


        data = parse_llm_json(
            response,
        )

        selected_tools = [
            MCPTool(tool)
            for tool in data["tools"]
            if tool in MCPTool._value2member_map_
        ]


        if not selected_tools:

            selected_tools = [
                MCPTool.ANALYTICS,
            ]


        return IntelligencePlan(
            tools=selected_tools,

            sections=data[
                "sections"
            ],

            reasoning=data[
                "reasoning"
            ],
        )