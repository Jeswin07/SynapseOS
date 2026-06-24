"""Data access layer for the Qdrant Vector Database."""

import uuid

from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.models import ScoredPoint


class QdrantRepository:
    """Handles connection and operations for the Qdrant vector database."""

    def __init__(self, host: str = "localhost", port: int = 6333) -> None:
        """Initializes the Qdrant client."""
        self.client = QdrantClient(host=host, port=port)
        self.vector_size = 384  # Output size for BAAI/bge-small-en-v1.5

    def ensure_collection(self, collection_name: str) -> None:
        """Creates the specified collection if it does not already exist."""
        collections = self.client.get_collections().collections
        if not any(c.name == collection_name for c in collections):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size,
                    distance=models.Distance.COSINE,
                ),
            )

    def upsert_chunks(
        self,
        collection_name: str,
        chunks: list[str],
        embeddings: list[list[float]],
        metadata: list[dict],
    ) -> None:
        """Inserts text chunks, their vectors, and metadata into Qdrant."""
        self.ensure_collection(collection_name)

        points = []
        for chunk, embedding, meta in zip(chunks, embeddings, metadata):
            payload = {"text": chunk}
            payload.update(meta)

            points.append(
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload=payload,
                )
            )

        self.client.upsert(collection_name=collection_name, points=points)

    def search(
        self,
        collection_name: str,
        query_vector: list[float],
        top_k: int = 5,
    ) -> list[ScoredPoint]:
        """Finds semantically similar chunks using the modern query API."""
        results = self.client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=top_k,
        )
        # query_points returns a QueryResponse object containing .points
        return results.points