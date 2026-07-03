"""Bootstrap AI agents."""

from __future__ import annotations

from src.agents.business.agent import BusinessAgent
from src.agents.knowledge.agent import KnowledgeAgent
from src.agents.registry import AgentRegistry
from src.bootstrap.mcp import create_mcp_service


def create_business_agent() -> BusinessAgent:
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

    mcp_service = create_mcp_service()

    registry = AgentRegistry()

    registry.register(
        KnowledgeAgent(
            mcp=mcp_service,
        ),
    )

    return BusinessAgent(
        registry=registry,
    )