"""Enterprise Retriever for semantic document retrieval."""

from __future__ import annotations

from qdrant_client.models import ScoredPoint

from src.ml.knowledge.embeddings import EmbeddingEngine
from src.modules.knowledge.repository import QdrantRepository


class Retriever:
    """Handles semantic retrieval from the vector database."""

    def __init__(self) -> None:
        self.embedding_engine = EmbeddingEngine()
        self.repository = QdrantRepository()

    def retrieve(
        self,
        query: str,
        collection_name: str,
        top_k: int = 5,
    ) -> list[ScoredPoint]:
        """
        Retrieves the most relevant chunks for a user query.

        Steps
        -----
        1. Embed query
        2. Search Qdrant
        3. Return ranked chunks
        """

        query_vector = self.embedding_engine.generate_embeddings([query])[0]

        results = self.repository.search(
            collection_name=collection_name,
            query_vector=query_vector,
            top_k=top_k,
        )

        return results