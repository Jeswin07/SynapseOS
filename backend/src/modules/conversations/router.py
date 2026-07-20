"""Conversation router."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.models.user import User
from src.modules.auth.dependencies import get_current_user
from src.modules.conversations.repository import ConversationRepository
from src.modules.conversations.schemas import (
    ConversationCreateRequest,
    ConversationResponse,
    ConversationUpdateRequest,
)
from src.modules.conversations.service import ConversationService

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


def get_service(
    db: AsyncSession = Depends(get_db),
) -> ConversationService:
    repository = ConversationRepository(db)
    return ConversationService(repository)


@router.post(
    "",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_conversation(
    request: ConversationCreateRequest,
    current_user: User = Depends(get_current_user),
    service: ConversationService = Depends(get_service),
):
    return await service.create(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        request=request,
    )


@router.get(
    "",
    response_model=list[ConversationResponse],
)
async def list_conversations(
    current_user: User = Depends(get_current_user),
    service: ConversationService = Depends(get_service),
):
    return await service.list(
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
    )


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
async def get_conversation(
    conversation_id: uuid.UUID,
    service: ConversationService = Depends(get_service),
):
    return await service.get(
        conversation_id=conversation_id,
    )


@router.patch(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
async def update_conversation(
    conversation_id: uuid.UUID,
    request: ConversationUpdateRequest,
    service: ConversationService = Depends(get_service),
):
    return await service.update(
        conversation_id=conversation_id,
        request=request,
    )


@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_conversation(
    conversation_id: uuid.UUID,
    service: ConversationService = Depends(get_service),
):
    await service.delete(
        conversation_id=conversation_id,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)