"""Scenario Planner."""

from __future__ import annotations

import json

from src.agents.common.llm import LLMClient
from src.agents.scenario.models import (
    ScenarioIntent,
    ScenarioPlan,
    ScenarioType,
)
from src.agents.scenario.normalizer import (
    PlannerNormalizer,
)
from src.agents.scenario.prompts import (
    SCENARIO_PLANNER_PROMPT,
)


class ScenarioPlanner:
    """
    Uses an LLM to understand the user's scenario.

    Responsibilities
    ----------------
    - Detect business intent
    - Detect scenario type
    - Extract parameters

    It NEVER executes tools.
    """

    def __init__(
        self,
    ) -> None:

        self.llm = LLMClient()

    async def plan(
        self,
        query: str,
    ) -> ScenarioPlan:

        prompt = SCENARIO_PLANNER_PROMPT.format(
            query=query,
        )

        response = await self.llm.generate(
            prompt,
        )

        try:

            data = json.loads(response)

            return PlannerNormalizer.normalize(
                data,
            )

        except Exception:

            return ScenarioPlan(
                intent=ScenarioIntent.WHAT_IF,
                scenario_type=ScenarioType.GENERAL,
                reasoning="Planner fallback.",
                parameters=[],
            )