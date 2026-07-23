"""Knowledge Agent."""

from __future__ import annotations

import logging

from src.agents.base import BaseAgent
from src.agents.models import (
    AgentInput,
    AgentOutput,
)
from src.agents.types import AgentType
from src.mcp.service import MCPService
from src.mcp.types import MCPTool

logger = logging.getLogger(__name__)

class KnowledgeAgent(BaseAgent):
    """
    Agent responsible for enterprise knowledge workflows.

    The agent orchestrates enterprise knowledge capabilities
    through the MCP layer.
    """

    def __init__(
        self,
        mcp: MCPService,
    ) -> None:

        super().__init__(
            agent_type=AgentType.KNOWLEDGE,
            agent_name="Knowledge Agent",
        )

        self.mcp = mcp

    async def _execute(
        self,
        request: AgentInput,
    ) -> AgentOutput:

        logger.info(
            "Knowledge Agent execution started | conversation_id=%s",
            request.conversation_id,
        )

        try:
            logger.info(
                "Executing knowledge search via MCP"
            )
            response = await self.mcp.execute(
                tool=MCPTool.KNOWLEDGE_SEARCH,
                tenant_id=request.tenant_id,
                user_id=request.user_id,
                query=request.query,
            )

            logger.info(
                "Knowledge search completed"
            )

            return AgentOutput(
                answer="",
                sources=response.data.get(
                    "sources",
                    [],
                ),
                data=response.data,
            )

        except Exception:
            logger.exception(
                "Knowledge Agent execution failed | conversation_id=%s",
                request.conversation_id,
            )
            raise