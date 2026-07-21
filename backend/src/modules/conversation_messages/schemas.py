"""Conversation message schemas."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ChatMessage(BaseModel):
    """
    Lightweight schema used internally for LLM conversation history.
    """

    role: str
    content: str


class ConversationMessageResponse(BaseModel):
    """
    API response schema for conversation messages.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    conversation_id: uuid.UUID
    role: str
    content: str
    created_at: datetime