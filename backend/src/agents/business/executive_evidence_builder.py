"""Executive evidence builder."""

from __future__ import annotations

from typing import Any

from src.agents.models import AgentOutput


class ExecutiveEvidenceBuilder:
    """
    Converts merged agent output into a clean executive
    context for the Business Agent LLM.

    This class performs NO reasoning and NO LLM calls.
    It only extracts and structures evidence.
    """

    def build(
        self,
        response: AgentOutput,
    ) -> dict[str, Any]:

        data = response.data or {}
        

        context: dict[str, Any] = {
            "executive_context": data.get(
                "executive_context",
                {}
            ),
            "knowledge": None,
            "analytics": None,
            "forecast": None,
            "prediction": None,
            "risk": None,
            "scenario": None,
            "recommendations": [],
            "sources": [],
        }

        # -------------------------
        # Knowledge
        # -------------------------

        knowledge = data.get("knowledge")

        if knowledge:

            context["knowledge"] = {
                "answer": knowledge.get("answer"),
                "sources": knowledge.get("sources", []),
            }

        # -------------------------
        # Intelligence
        # -------------------------

        intelligence = data.get("intelligence")

        if intelligence:

            results = intelligence.get("results", {})

            context["analytics"] = results.get("analytics")

            context["forecast"] = results.get("forecast")

            context["prediction"] = results.get("prediction")

            context["risk"] = results.get("risk")

        # -------------------------
        # Scenario
        # -------------------------

        scenario = data.get("scenario")

        if scenario:

            decision = scenario.get("decision", {})

            context["scenario"] = {
                "summary": decision.get("summary"),
                "impacts": decision.get("impacts"),
                "tradeoffs": decision.get("tradeoffs"),
                "risks": decision.get("risks"),
                "confidence": decision.get("confidence"),
            }

        # -------------------------
        # Recommendations
        # -------------------------

        if response.recommendations:

            context["recommendations"] = (
                response.recommendations
            )

        # -------------------------
        # Sources
        # -------------------------

        if response.sources:
            context["sources"] = response.sources

        return context