"""Streaming events for Assistant."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class StreamEventType(str, Enum):
    STATUS = "status"
    AGENT_STARTED = "agent_started"
    AGENT_COMPLETED = "agent_completed"
    COMPLETE = "complete"
    ERROR = "error"


class StreamEvent(BaseModel):
    type: StreamEventType

    message: str

    agent: str | None = None

    data: dict[str, Any] = Field(
        default_factory=dict,
    )