"""Scenario Agent."""

from __future__ import annotations

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

        scenario = await self.scenario_planner.plan(
            request.query,
        )

        # ---------------------------------------
        # Decide evidence
        # ---------------------------------------

        evidence_plan = self.evidence_planner.plan(
            scenario,
        )

        evidence: dict = {}

        # ---------------------------------------
        # Collect evidence
        # ---------------------------------------

        for tool in evidence_plan.tools:

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

        simulation = self.simulation_engine.run(
            scenario=scenario.model_dump(),
            evidence=evidence,
        )

        # ---------------------------------------
        # Build executive decision
        # ---------------------------------------

        report = await self.builder.build(
            scenario=request.query,
            evidence=evidence,
            simulation=simulation,
        )

        # ---------------------------------------
        # Return structured output
        # ---------------------------------------

        return AgentOutput(
            answer="",
            data={
                "scenario": scenario.model_dump(),
                "evidence_plan": evidence_plan.model_dump(),
                "simulation": simulation,
                "decision": report.model_dump(),
            },
        )