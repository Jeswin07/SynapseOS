"""Bootstrap AI agents."""

from __future__ import annotations

from sqlalchemy.orm import Session

from src.agents.business.agent import BusinessAgent
from src.agents.intelligence.agent import IntelligenceAgent
from src.agents.knowledge.agent import KnowledgeAgent
from src.agents.scenario.agent import ScenarioAgent
from src.agents.registry import AgentRegistry
from src.bootstrap.mcp import create_mcp_service


def create_business_agent(db: Session,) -> BusinessAgent:
    """
    Creates the complete agent system.

    Flow:
        BusinessAgent
            ↓
        AgentRegistry
            ↓
        Specialized Agents
            ↓
        MCP
    """

    mcp_service = create_mcp_service(db,)

    registry = AgentRegistry()

    registry.register(
        KnowledgeAgent(
            mcp=mcp_service,
        ),
    )

    registry.register(
        IntelligenceAgent(
            mcp=mcp_service,
        ),
    )

    scenario = ScenarioAgent(
        intelligence=IntelligenceAgent(
            mcp=mcp_service,
        ),
    )

    registry.register(
        scenario,
    )

    print(
        "REGISTERED:",
        registry._agents.keys(),
    )

    return BusinessAgent(
        registry=registry,
    )