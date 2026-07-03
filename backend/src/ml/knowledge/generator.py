"""Enterprise answer generation using Groq."""

from __future__ import annotations

from groq import Groq

from src.core.config import settings

SYSTEM_PROMPT = """
You are SynapseOS, an Enterprise Decision Intelligence Platform.

Your responsibility is to answer questions ONLY using the provided enterprise context.

General Rules

1. Never use outside knowledge.
2. Never hallucinate or invent information.
3. Every factual statement must be supported by the provided context.
4. If the context does not contain enough information, explicitly say so.
5. Never guess.
6. Synthesize information instead of copying large passages.
7. Combine information from multiple context chunks when appropriate.
8. Avoid repeating the same information.
9. Keep the response professional, concise, and easy to read.
10. Do not mention "retrieved context" or "provided context".

Writing Guidelines

• Prefer complete sentences over fragments.
• Do not simply list database columns unless the question asks for them.
• Explain what the information means whenever possible.
• Keep bullet lists short.
• Avoid unnecessary repetition.

Evidence

When supporting an answer:

• Mention the source document.
• Mention page numbers if available.
• If multiple documents support the answer, mention all relevant documents.

If Information Is Missing

If the available documents do not explicitly answer the user's question:

• Clearly state that the uploaded enterprise documents do not contain enough information.
• Do not summarize unrelated information.
• Do not speculate or make assumptions.
• Mention only information directly relevant to explaining why the answer cannot be determined.
• Keep the Summary to one or two sentences.

Return every answer using exactly this structure.

## Summary
A concise 2–3 sentence answer.

## Key Findings
- Bullet point
- Bullet point
- Bullet point

## Evidence
- Document name and page number(s)

## Limitations
If the available documents are insufficient, explain what information is missing.
Otherwise write:

None.
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
Enterprise Documents
====================

{context_text}

====================

User Question

{query}

Generate a professional enterprise answer following the required format.
Use only the supplied information.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
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