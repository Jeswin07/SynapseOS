"""Business response aggregator."""

from __future__ import annotations

from src.agents.models import (
    AgentMetadata,
    AgentOutput,
)
from src.agents.types import AgentType


class BusinessAggregator:
    """
    Aggregates outputs from multiple agents into a
    single structured response.

    This class NEVER calls an LLM.
    """

    def aggregate(
        self,
        outputs: dict[
            AgentType,
            AgentOutput,
        ],
    ) -> AgentOutput:

        if not outputs:

            return AgentOutput(
                answer="",
                metadata=AgentMetadata(
                    agent_name="Business Aggregator",
                    agent_type="aggregator",
                    success=False,
                ),
            )

        merged_data = {}

        merged_sources = []

        merged_recommendations = []

        metadata = {}

        executive_context = {
            "agents_used": [],
            "knowledge_available": False,
            "analytics_available": False,
            "forecast_available": False,
            "prediction_available": False,
            "risk_available": False,
            "scenario_available": False,
            "coverage": "",
            "agent_count": 0,
        }

        for agent_type, output in outputs.items():

            executive_context["agents_used"].append(
                agent_type.value
            )

            if agent_type.value == "knowledge":
                executive_context["knowledge_available"] = True

            elif agent_type.value == "intelligence":

                results = (
                    output.data or {}
                ).get("results", {})

                executive_context["analytics_available"] = (
                    results.get("analytics") is not None
                )

                executive_context["forecast_available"] = (
                    results.get("forecast") is not None
                )

                executive_context["prediction_available"] = (
                    results.get("prediction") is not None
                )

                executive_context["risk_available"] = (
                    results.get("risk") is not None
                )

            elif agent_type.value == "scenario":
                executive_context["scenario_available"] = True

            merged_data[
                agent_type.value
            ] = output.data

            for source in output.sources:
                if source not in merged_sources:
                    merged_sources.append(source)

            merged_recommendations.extend(
                output.recommendations
            )

            if output.metadata:

                metadata[
                    agent_type.value
                ] = output.metadata.model_dump()

        executive_context["agent_count"] = len(
            executive_context["agents_used"]
        )

        coverage = []

        if executive_context["knowledge_available"]:
            coverage.append("Knowledge")

        if executive_context["analytics_available"]:
            coverage.append("Analytics")

        if executive_context["forecast_available"]:
            coverage.append("Forecast")

        if executive_context["prediction_available"]:
            coverage.append("Prediction")

        if executive_context["risk_available"]:
            coverage.append("Risk")

        if executive_context["scenario_available"]:
            coverage.append("Scenario")

        executive_context["coverage"] = (
            " + ".join(coverage)
            if coverage
            else "None"
        )

        return AgentOutput(

            answer="",

            metadata=AgentMetadata(
                agent_name="Business Aggregator",
                agent_type="aggregator",
            ),

            data={

                **merged_data,

                "metadata": metadata,

                "executive_context": executive_context,

            },

            sources=merged_sources,

            recommendations=list(
                dict.fromkeys(
                    merged_recommendations,
                )
            ),
        )