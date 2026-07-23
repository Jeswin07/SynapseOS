"""Scenario Agent."""

from __future__ import annotations

import logging

from src.agents.base import BaseAgent
from src.agents.intelligence.agent import IntelligenceAgent
from src.agents.models import (
    AgentInput,
    AgentOutput,
)
from src.agents.scenario.decision_builder import (
    DecisionBuilder,
)
from src.agents.scenario.evidence import (
    EvidencePlanner,
)
from src.agents.scenario.planner import (
    ScenarioPlanner,
)
from src.agents.scenario.simulation_engine import (
    SimulationEngine,
)
from src.agents.types import AgentType

logger = logging.getLogger(__name__)

class ScenarioAgent(BaseAgent):
    """
    Enterprise Scenario Agent.

    Responsibilities

    - Understand business scenario
    - Determine required evidence
    - Collect enterprise evidence
    - Build structured decision

    It NEVER writes executive summaries.
    """

    def __init__(
        self,
        intelligence: IntelligenceAgent,
    ) -> None:

        super().__init__(
            agent_type=AgentType.SCENARIO,
            agent_name="Scenario Agent",
        )

        self.intelligence = intelligence

        self.scenario_planner = (
            ScenarioPlanner()
        )

        self.evidence_planner = (
            EvidencePlanner()
        )

        self.builder = (
            DecisionBuilder()
        )

        self.simulation_engine = (
            SimulationEngine()
        )

    async def _execute(
        self,
        request: AgentInput,
    ) -> AgentOutput:

        # ---------------------------------------
        # Understand scenario
        # ---------------------------------------

        logger.info(
            "Scenario Agent execution started | conversation_id=%s",
            request.conversation_id,
        )

        try:

            logger.info(
                "Generating scenario execution plan"
            )

            scenario = await self.scenario_planner.plan(
                request.query,
            )

            logger.info(
                "Scenario plan generated | type=%s intent=%s",
                scenario.scenario_type.value,
                scenario.intent.value,
            )

            # ---------------------------------------
            # Decide evidence
            # ---------------------------------------

            logger.info(
                "Generating evidence plan"
            )

            evidence_plan = self.evidence_planner.plan(
                scenario,
            )

            logger.info(
                "Evidence plan generated | tools=%s",
                [tool.value for tool in evidence_plan.tools],
            )

            evidence: dict = {}

            # ---------------------------------------
            # Collect evidence
            # ---------------------------------------
            logger.info(
                "Collecting evidence using %d intelligence tool(s)",
                len(evidence_plan.tools),
            )

            for tool in evidence_plan.tools:

                logger.info(
                    "Executing intelligence tool: %s",
                    tool.value,
                )

                intelligence_request = AgentInput(
                    query=request.query,
                    tenant_id=request.tenant_id,
                    user_id=request.user_id,
                    session_id=request.session_id,
                    conversation_id=request.conversation_id,
                    context=request.context,
                    metadata={
                        **request.metadata,
                        "forced_tools": [tool],
                    },
                )

                response = await self.intelligence.invoke(
                    intelligence_request,
                )

                logger.info(
                    "Completed intelligence tool: %s",
                    tool.value,
                )

                results = response.data.get(
                    "results",
                    {},
                )

                evidence.update(
                    results,
                )

            # ---------------------------------------
            # Run deterministic simulation
            # ---------------------------------------
            logger.info(
                "Running deterministic scenario simulation"
            )

            simulation = self.simulation_engine.run(
                scenario=scenario.model_dump(),
                evidence=evidence,
            )

            logger.info(
                "Scenario simulation completed"
            )
            # ---------------------------------------
            # Build executive decision
            # ---------------------------------------
            logger.info(
                "Building decision report"
            )

            report = await self.builder.build(
                scenario=request.query,
                evidence=evidence,
                simulation=simulation,
            )

            logger.info(
                "Decision report generated"
            )

            # ---------------------------------------
            # Return structured output
            # ---------------------------------------
            logger.info(
                "Scenario Agent execution completed"
            )

            return AgentOutput(
                answer="",
                data={
                    "scenario": scenario.model_dump(),
                    "evidence_plan": evidence_plan.model_dump(),
                    "simulation": simulation,
                    "decision": report.model_dump(),
                },
            )

        except Exception:
            logger.exception(
                "Scenario Agent execution failed | conversation_id=%s",
                request.conversation_id,
            )
            raise