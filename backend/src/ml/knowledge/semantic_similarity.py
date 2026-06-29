"""Semantic similarity using Sentence Transformers."""

from __future__ import annotations

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


class SemanticSimilarity:
    """
    Computes semantic similarity between
    two answers.

    Score:
        0 → completely different
        1 → identical meaning
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> None:

        self.model = SentenceTransformer(
            model_name,
        )

    def score(
        self,
        generated_answer: str,
        reference_answer: str,
    ) -> float:
        """
        Returns cosine similarity.
        """

        embeddings = self.model.encode(
            [
                generated_answer,
                reference_answer,
            ],
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

        similarity = cos_sim(
            embeddings[0],
            embeddings[1],
        )

        return round(
            float(similarity.item()),
            4,
        )