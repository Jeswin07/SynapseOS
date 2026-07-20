"""Conversation service."""

from __future__ import annotations

import uuid

from fastapi import HTTPException, status

from src.models.conversation import Conversation
from src.modules.conversations.repository import ConversationRepository
from src.modules.conversations.schemas import (
    ConversationCreateRequest,
    ConversationUpdateRequest,
)


class ConversationService:
    """Service for conversation operations."""

    def __init__(self, repository: ConversationRepository):
        self.repository = repository

    async def create(
        self,
        *,
        tenant_id: uuid.UUID,
        user_id: uuid.UUID,
        request: ConversationCreateRequest,
    ) -> Conversation:
        return await self.repository.create(
            tenant_id=tenant_id,
            user_id=user_id,
            dataset_version_id=request.dataset_version_id,
            title=request.title,
        )

    async def get(
        self,
        *,
        conversation_id: uuid.UUID,
    ) -> Conversation:
        conversation = await self.repository.get(conversation_id)

        if conversation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found.",
            )

        return conversation

    async def list(
        self,
        *,
        tenant_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> list[Conversation]:
        return await self.repository.list_by_user(
            tenant_id=tenant_id,
            user_id=user_id,
        )

    async def update(
        self,
        *,
        conversation_id: uuid.UUID,
        request: ConversationUpdateRequest,
    ) -> Conversation:
        conversation = await self.get(
            conversation_id=conversation_id,
        )

        return await self.repository.update_title(
            conversation,
            request.title,
        )

    async def delete(
        self,
        *,
        conversation_id: uuid.UUID,
    ) -> None:
        conversation = await self.get(
            conversation_id=conversation_id,
        )

        await self.repository.delete(conversation)