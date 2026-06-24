"""LLM Adapter for generating answers from retrieved context."""

from src.core.config import settings
from abc import ABC, abstractmethod

from groq import Groq


class BaseGenerator(ABC):
    """Abstract interface for answer generation."""

    @abstractmethod
    def generate_answer(self, query: str, context: list[str]) -> str:
        """Generates an answer based strictly on the provided context."""
        pass


class GroqGenerator(BaseGenerator):
    """Implementation of the generator using the free Groq API."""

    def __init__(self, model_name: str = "llama-3.3-70b-versatile") -> None:
        """Initializes the Groq client."""
        api_key = settings.groq_api_key
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is missing.")

        self.client = Groq(api_key=api_key)
        self.model_name = model_name

    def generate_answer(self, query: str, context: list[str]) -> str:
        """Constructs a prompt and queries the LLM for a grounded answer."""
        context_text = "\n\n---\n\n".join(context)

        system_prompt = (
            "You are SynapseOS, an Enterprise Decision Intelligence Platform. "
            "Answer the user's query strictly using the provided context. "
            "If the answer is not in the context, state that you cannot answer "
            "based on the provided enterprise documents. Do not hallucinate."
        )

        user_prompt = f"Context:\n{context_text}\n\nQuery: {query}"

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            model=self.model_name,
            temperature=0.0,
            max_tokens=1024,
        )

        return str(response.choices[0].message.content or "Generation error.")