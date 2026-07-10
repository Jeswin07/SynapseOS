"""Routes for Business AI Assistant."""

from __future__ import annotations

from uuid import UUID
from src.models.user import User

from src.modules.auth.dependencies import (
    get_current_user,
)
from fastapi import APIRouter, Depends

from src.modules.assistant.schemas import (
    AssistantChatRequest,
    AssistantChatResponse,
)
from src.modules.assistant.service import AssistantService
from src.modules.auth.dependencies import (
    get_current_tenant_id,
)
from sqlalchemy.orm import Session

from src.db.session import get_db


router = APIRouter(
    prefix="/assistant",
    tags=["AI Assistant"],
)


@router.post(
    "/chat",
    response_model=AssistantChatResponse,
)
async def chat(
    request: AssistantChatRequest,
    db: Session = Depends(
        get_db,
    ),
    current_user: User = Depends(
        get_current_user,
    ),
) -> AssistantChatResponse:
    """
    Chat with SynapseOS Business AI Assistant.
    """

    service = AssistantService(
        db,
    )

    return await service.chat(
        request=request,
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
    )