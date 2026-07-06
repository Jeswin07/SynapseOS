"""Shared LLM client."""

from __future__ import annotations

from groq import AsyncGroq

from src.core.config import settings


class LLMClient:
    """
    Wrapper around LLM providers.
    """


    def __init__(
        self,
    ) -> None:

        self.client = AsyncGroq(
            api_key=settings.groq_api_key,
        )


    async def generate(
        self,
        prompt: str,
    ) -> str:


        response = (
            await self.client.chat.completions.create(
                model=settings.groq_model,

                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],

                temperature=0,
            )
        )


        message = (
            response
            .choices[0]
            .message
        )


        if message.content is None:
            raise ValueError(
                "LLM returned empty response."
            )


        return message.content