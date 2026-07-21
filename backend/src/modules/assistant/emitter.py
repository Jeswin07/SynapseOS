"""Assistant event emitter."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator

from src.modules.assistant.events import StreamEvent


class StreamEmitter:
    """
    Async event emitter used by LangGraph
    and consumed by StreamingResponse.
    """

    def __init__(self) -> None:

        self._queue: asyncio.Queue[
            StreamEvent
        ] = asyncio.Queue()

    async def emit(
        self,
        event: StreamEvent,
    ) -> None:
        print("EMIT:", event.type, event.message)

        await self._queue.put(event)

    async def stream(
        self,
    ) -> AsyncGenerator[StreamEvent]:

        while True:

            event = await self._queue.get()

            yield event

            if event.type.value == "complete":
                break