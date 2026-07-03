"""Aggregates responses from multiple AI agents."""

from __future__ import annotations

from src.agents.models import (
    AgentMetadata,
    AgentOutput,
)
from src.agents.types import AgentType


class BusinessAggregator:
    """
    Combines outputs from multiple AI agents into a single response.
    """

    def aggregate(
        self,
        outputs: dict[
            AgentType,
            AgentOutput,
        ],
    ) -> AgentOutput:
        """
        Aggregate agent outputs into a unified response.
        """

        if not outputs:
            return AgentOutput(
                answer="No response could be generated.",
                metadata=AgentMetadata(
                    agent_name="Business Aggregator",
                    agent_type="aggregator",
                    success=False,
                ),
            )

        if len(outputs) == 1:
            return next(
                iter(outputs.values())
            )

        answers: list[str] = []

        sources: list[dict] = []

        recommendations: list[str] = []

        data: dict = {}

        for output in outputs.values():

            answers.append(output.answer)

            sources.extend(output.sources)

            recommendations.extend(
                output.recommendations
            )

            data.update(output.data)

        return AgentOutput(
            answer="\n\n".join(answers),
            metadata=AgentMetadata(
                agent_name="Business Aggregator",
                agent_type="aggregator",
            ),
            sources=sources,
            recommendations=list(
                dict.fromkeys(recommendations)
            ),
            data=data,
        )