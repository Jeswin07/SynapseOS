"""Routes for Business AI Assistant."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends

from src.modules.assistant.schemas import (
    AssistantChatRequest,
    AssistantChatResponse,
)
from src.modules.assistant.service import AssistantService
from src.modules.auth.dependencies import (
    get_current_tenant_id,
)

router = APIRouter(
    prefix="/assistant",
    tags=["AI Assistant"],
)


service = AssistantService()


@router.post(
    "/chat",
    response_model=AssistantChatResponse,
)
async def chat(
    request: AssistantChatRequest,
    tenant_id: UUID = Depends(
        get_current_tenant_id,
    ),
) -> AssistantChatResponse:
    """
    Chat with SynapseOS Business AI Assistant.
    """

    return await service.chat(
        request=request,
        tenant_id=tenant_id,
    )