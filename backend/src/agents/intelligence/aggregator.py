"""LLM intelligence aggregation."""

from __future__ import annotations

import json
from typing import Any

from src.agents.common.llm import (
    LLMClient,
)

from src.agents.intelligence.schemas import (
    IntelligencePlan,
)


class IntelligenceAggregator:
    """
    Converts tool results into
    executive business answers.
    """


    def __init__(
        self,
    ) -> None:

        self.llm = LLMClient()


    async def aggregate(
        self,
        *,
        query: str,
        plan: IntelligencePlan,
        results: dict[str, Any],
    ) -> str:
        """
        Generate final AI response.
        """


        prompt = f"""
You are SynapseOS Enterprise Intelligence Agent.

You answer business questions using ONLY provided data.

User question:
{query}


Planner reasoning:
{plan.reasoning}


Relevant sections:
{plan.sections}


Business data:
{json.dumps(results, indent=2)}


Instructions:

- Give a clear executive answer.
- Mention important numbers.
- Explain business impact.
- Provide recommendations if useful.
- Do not invent missing data.

Forecast response contains:

forecast_config.metric tells what is predicted.

Do not assume all forecasts are revenue.

Examples:
- metric=revenue → discuss sales/revenue
- metric=product_count → discuss demand/orders
- metric=review_score → discuss satisfaction trend

Use total_expected_value and average_daily_value with the correct business meaning.
Formatting rules:

If aggregation=count:
- Values represent counts.
- Never show decimal places.
- Example:
  1200 orders
  40 deliveries/day

If aggregation=sum:
- Values represent totals.
- Use money format only for revenue metrics.

Never call order forecasts revenue.
Never call delivery forecasts sales.
"""


        return await self.llm.generate(
            prompt,
        )