"""Data access layer for the Qdrant Vector Database."""

from __future__ import annotations

import uuid

from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.models import ScoredPoint

from src.core.config import settings


class QdrantRepository:
    """Handles connection and operations for the Qdrant vector database."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
    ) -> None:
        """Initialize the Qdrant client."""
        self.client = QdrantClient(host=host, port=port)
        self.vector_size = settings.embedding_dimension  # BAAI/bge-small-en-v1.5

    def ensure_collection(self, collection_name: str) -> None:
        """Create the collection if it does not already exist."""

        collections = self.client.get_collections().collections

        if any(c.name == collection_name for c in collections):
            return

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
        """Insert document chunks into Qdrant."""

        self.ensure_collection(collection_name)

        points: list[models.PointStruct] = []

        for chunk, embedding, meta in zip(
            chunks,
            embeddings,
            metadata,
            strict=False,
        ):
            payload = dict(meta)
            payload["text"] = chunk

            points.append(
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload=payload,
                )
            )

        self.client.upsert(
            collection_name=collection_name,
            points=points,
            wait=True,
        )

    def search(
        self,
        collection_name: str,
        query_vector: list[float],
        top_k: int = 5,
    ) -> list[ScoredPoint]:
        """Perform semantic search."""

        response = self.client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=top_k,
            with_payload=True,
            with_vectors=False,
        )

        return response.points

    def delete_document(
        self,
        collection_name: str,
        document_id: str,
    ) -> None:
        """Delete all chunks belonging to a document."""

        self.client.delete(
            collection_name=collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="document_id",
                            match=models.MatchValue(
                                value=document_id,
                            ),
                        )
                    ]
                )
            ),
        )

    def collection_exists(self, collection_name: str) -> bool:
        """Return True if a collection exists."""

        collections = self.client.get_collections().collections

        return any(
            collection.name == collection_name
            for collection in collections
        )

    def get_all_chunks(
        self,
        collection_name: str,
    ) -> list[dict]:
        """
        Returns every chunk stored in a collection.

        Used for building the local BM25 index.
        """

        records: list[dict] = []

        offset = None

        while True:

            points, offset = self.client.scroll(
                collection_name=collection_name,
                limit=100,
                offset=offset,
                with_payload=True,
                with_vectors=False,
            )

            for point in points:

                payload = point.payload or {}

                records.append(
                    {
                        "text": str(
                            payload.get(
                                "text",
                                "",
                            )
                        ),
                        "payload": payload,
                    }
                )

            if offset is None:
                break

        return records