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
"""


        return await self.llm.generate(
            prompt,
        )