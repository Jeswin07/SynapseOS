"""Routes for Business AI Assistant."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.models.user import User
from src.modules.assistant.schemas import (
    AssistantChatRequest,
    AssistantChatResponse,
)
from src.modules.assistant.service import AssistantService
from src.modules.auth.dependencies import (
    get_current_user,
)

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

@router.post("/chat/stream")
async def chat_stream(
    request: AssistantChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service = AssistantService(db)

    return StreamingResponse(
        service.chat_stream(
            request=request,
            tenant_id=current_user.tenant_id,
            user_id=current_user.id,
        ),
        media_type="text/event-stream",
    )