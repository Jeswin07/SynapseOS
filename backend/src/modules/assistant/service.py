"""Business AI Assistant service."""

from __future__ import annotations

from uuid import UUID

from src.agents.models import AgentInput
from src.bootstrap.agents import create_business_agent
from src.modules.assistant.schemas import (
    AssistantChatRequest,
    AssistantChatResponse,
)


class AssistantService:
    """
    Entry point for user interaction with SynapseOS AI.
    """

    def __init__(self) -> None:

        self.agent = create_business_agent()

    async def chat(
        self,
        request: AssistantChatRequest,
        tenant_id: UUID,
    ) -> AssistantChatResponse:

        response = await self.agent.invoke(
            AgentInput(
                query=request.message,
                tenant_id=tenant_id,
            ),
        )

        return AssistantChatResponse(
            answer=response.answer,
            sources=response.sources,
            recommendations=response.recommendations,
            data=response.data,
            tenant_id=tenant_id,
            agent=(
                response.metadata.agent_name
                if response.metadata
                else None
            ),
        )