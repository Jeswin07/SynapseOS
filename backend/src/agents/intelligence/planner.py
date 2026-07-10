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

forecast:
Use for:
- future prediction
- revenue forecasting
- demand forecasting
- future trends

User question:

{query}


Return ONLY JSON.

Example:

{{
 "tools":["analytics"],
 "sections":["revenue"],
 "reasoning":"Analytics data is required."
}}

You are an enterprise forecasting planner.

Your job is to understand business meaning,
not memorize column names.

Use semantic matching.

Rules:

Revenue/Sales:
Choose columns representing:
- payment amount
- selling price
- revenue
- total amount
- sales value
- transaction value

Orders:
Choose identifiers representing:
- order id
- transaction id
- invoice id

Demand:
Choose:
- quantity
- item count
- product count
- units sold

Customer satisfaction:
Choose:
- rating
- review score
- feedback score

Delivery:
Choose:
- delivery date
- shipment date
- delivery duration

Never invent columns.
Only choose from available columns.

Return JSON only.

Delivery rules:

If user asks:
"delivery volume"
"number of deliveries"
"deliveries next month"

Use:
target_column = order_id
date_column = order_delivered_customer_date
aggregation = count


If user asks:
"delivery time"
"delivery performance"
"delivery speed"
"delivery delay"

Use:
target_column = delivery_days
aggregation = mean
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