"""Module for quantitative evaluation of the RAG pipeline metrics."""

import json
from src.ml.knowledge.generator import GroqGenerator


class RAGEvaluator:
    """Evaluates RAG outputs for Faithfulness and Answer Relevance."""

    def __init__(self) -> None:
        """Initializes the judge LLM engine."""
        # Using the 70B model ensures deep reasoning capacity for auditing
        self.judge = GroqGenerator(model_name="llama-3.3-70b-versatile")

    def evaluate_faithfulness(self, answer: str, context: list[str]) -> float:
        """Calculates faithfulness score (0.0 to 1.0) to detect hallucinations."""
        context_text = "\n---\n".join(context)
        prompt = (
            "Analyze the provided Answer and determine if it is completely "
            "supported by the Context. Ignore outside knowledge.\n"
            f"Context: {context_text}\n"
            f"Answer: {answer}\n\n"
            "Respond strictly in the following valid JSON format:\n"
            '{"score": 0.0 to 1.0, "reasoning": "brief explanation"}'
        )
        try:
            raw_response = self.judge.generate_answer(prompt, [])
            data = json.loads(raw_response)
            return float(data.get("score", 0.0))
        except (json.JSONDecodeError, ValueError):
            return 0.0

    def evaluate_relevance(self, query: str, answer: str) -> float:
        """Calculates how directly the answer addresses the original query."""
        prompt = (
            "Analyze if the Answer directly and completely addresses the Query.\n"
            f"Query: {query}\n"
            f"Answer: {answer}\n\n"
            "Respond strictly in the following valid JSON format:\n"
            '{"score": 0.0 to 1.0, "reasoning": "brief explanation"}'
        )
        try:
            raw_response = self.judge.generate_answer(prompt, [])
            data = json.loads(raw_response)
            return float(data.get("score", 0.0))
        except (json.JSONDecodeError, ValueError):
            return 0.0