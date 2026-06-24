"""Enterprise answer generation using Groq."""

from __future__ import annotations

from groq import Groq

from src.core.config import settings


SYSTEM_PROMPT = """
You are SynapseOS, an Enterprise Decision Intelligence Platform.

Your job is to answer ONLY using the provided enterprise context.

Rules:

1. Never use outside knowledge.
2. Never hallucinate.
3. If the answer is not present in the context, clearly state:
   "I could not find the answer in the uploaded enterprise documents."
4. Keep answers concise and professional.
5. Always synthesize information instead of copying large passages.
6. If multiple sources agree, combine them.
7. Mention important articles, sections or page references when available.

Return answers using this format:

## Summary
<short answer>

## Key Findings
- Bullet
- Bullet
- Bullet

## Evidence
- Mention important article/page if available

## Limitations
If the context is insufficient, clearly mention it.
"""


class GroqGenerator:
    """Enterprise answer generator."""

    def __init__(self) -> None:

        self.client = Groq(
            api_key=settings.groq_api_key,
        )

        self.model = settings.groq_model

    def generate_answer(
        self,
        query: str,
        context: list[str],
    ) -> str:

        context_text = "\n\n".join(context)

        prompt = f"""
Enterprise Context
==================

{context_text}

==================

User Question

{query}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.1,
            max_tokens=700,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return response.choices[0].message.content.strip()