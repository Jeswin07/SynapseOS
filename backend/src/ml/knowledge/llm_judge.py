"""LLM-as-a-Judge for Knowledge Generation Evaluation."""

from __future__ import annotations

import json

from groq import Groq

from src.core.config import settings


class LLMJudge:
    """
    Uses the production Groq model to evaluate
    generated answers.

    Returns all evaluation metrics
    in a single LLM call.
    """

    def __init__(self) -> None:

        self.client = Groq(
            api_key=settings.groq_api_key,
        )

        self.model = settings.groq_judge_model

    def evaluate(
        self,
        question: str,
        answer: str,
        reference: str,
        context: str,
    ) -> dict:
        """
        Evaluate a generated answer.

        Returns:
        {
            "faithfulness": float,
            "answer_correctness": float,
            "answer_relevancy": float,
            "context_recall": float,
            "faithfulness_reason": str,
            "correctness_reason": str,
            "relevancy_reason": str,
            "recall_reason": str,
        }
        """

        prompt = f"""
You are an expert evaluator for Retrieval-Augmented Generation (RAG).

Evaluate the generated answer using the retrieved context and the reference answer.

Question:
{question}

Retrieved Context:
{context}

Reference Answer:
{reference}

Generated Answer:
{answer}

Evaluate the following metrics on a scale from 0.0 to 1.0.

1. Faithfulness
Determine whether every factual claim in the generated answer is supported by the retrieved context.

2. Answer Correctness
Compare the generated answer with the reference answer and score factual correctness.

3. Answer Relevancy
Determine whether the generated answer directly answers the user's question.

4. Context Recall
Determine whether the retrieved context contains sufficient information to answer the question completely.

Return ONLY valid JSON.

{{
    "faithfulness": 0.0,
    "answer_correctness": 0.0,
    "answer_relevancy": 0.0,
    "context_recall": 0.0,
    "faithfulness_reason": "",
    "correctness_reason": "",
    "relevancy_reason": "",
    "recall_reason": ""
}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            response_format={
                "type": "json_object",
            },
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        result = json.loads(
            response.choices[0].message.content
        )

        return {
            "faithfulness": float(
                result["faithfulness"]
            ),
            "answer_correctness": float(
                result["answer_correctness"]
            ),
            "answer_relevancy": float(
                result["answer_relevancy"]
            ),
            "context_recall": float(
                result["context_recall"]
            ),
            "faithfulness_reason": result[
                "faithfulness_reason"
            ],
            "correctness_reason": result[
                "correctness_reason"
            ],
            "relevancy_reason": result[
                "relevancy_reason"
            ],
            "recall_reason": result[
                "recall_reason"
            ],
        }