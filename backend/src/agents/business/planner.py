"""Business request planner."""

from __future__ import annotations

import re

from src.agents.business.models import ExecutionPlan
from src.agents.types import AgentType


class BusinessPlanner:
    """
    Creates execution plans for incoming business requests.

    The current implementation uses lightweight rule-based
    intent detection. It is intentionally designed so that
    it can later be replaced by an LLM-powered planner
    without affecting the rest of the architecture.
    """

    def plan(
        self,
        query: str,
    ) -> ExecutionPlan:
        """
        Returns an execution plan for the given query.
        """

        query = query.lower().strip()

        # --------------------------------------------------
        # Scenario Simulation
        # --------------------------------------------------

        if self._is_simulation(query):

            return ExecutionPlan(
                agents=[
                    AgentType.SIMULATION,
                    AgentType.ENTERPRISE
                ],
                reasoning="Scenario evaluation requires enterprise analysis.",
            )

        # --------------------------------------------------
        # Enterprise Intelligence
        # --------------------------------------------------

        if self._is_enterprise(query):

            return ExecutionPlan(
                agents=[
                    AgentType.ENTERPRISE,
                ],
                reasoning="Structured enterprise analysis requested.",
            )

        # --------------------------------------------------
        # Knowledge
        # --------------------------------------------------

        if self._needs_business_context(query):

            return ExecutionPlan(
                agents=[
                    AgentType.KNOWLEDGE,
                    AgentType.ENTERPRISE,
                ],
                parallel=True,
                reasoning=(
                    "Knowledge retrieval and enterprise analysis required."
                ),
            )

        return ExecutionPlan(
            agents=[
                AgentType.KNOWLEDGE,
            ],
        )

    @staticmethod
    def _is_simulation(
        query: str,
    ) -> bool:

        patterns = [
            r"\bwhat if\b",
            r"\bif\b",
            r"\bincrease\b",
            r"\bdecrease\b",
            r"\bimpact\b",
            r"\bscenario\b",
        ]

        return any(
            re.search(pattern, query)
            for pattern in patterns
        )

    @staticmethod
    def _is_enterprise(
        query: str,
    ) -> bool:

        keywords = {
            "forecast",
            "predict",
            "prediction",
            "analytics",
            "dashboard",
            "risk",
            "train",
            "model",
            "shap",
            "kpi",
            "revenue",
            "sales",
            "orders",
        }

        return any(
            keyword in query
            for keyword in keywords
        )

    
    @staticmethod
    def _needs_business_context(
        query: str,
    ) -> bool:

        keywords = {
            "why",
            "trend",
            "performance",
            "increase",
            "decrease",
            "delay",
            "growth",
            "compare",
            "recommend",
            "improve",
        }

        return any(
            keyword in query
            for keyword in keywords
        )