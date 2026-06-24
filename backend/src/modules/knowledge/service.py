"""Business logic orchestration for the Knowledge module."""

from __future__ import annotations

import time
import uuid
from datetime import datetime
from pathlib import Path
from src.ml.knowledge.embeddings import EmbeddingEngine
from src.ml.knowledge.generator import GroqGenerator
from src.ml.knowledge.retriever import Retriever
from src.modules.knowledge.repository import QdrantRepository
from src.modules.knowledge.schemas import (
    DocumentUploadResponse,
    QueryMetrics,
    QueryRequest,
    QueryResponse,
    SourceChunk,
)


class KnowledgeService:
    """Orchestrates RAG workflows."""

    def __init__(self) -> None:
        self.embedding_engine = EmbeddingEngine()
        self.repository = QdrantRepository()
        self.generator = GroqGenerator()
        self.retriever = Retriever()

    def process_document(
        self,
        file_path: str,
        file_name: str,
        collection_name: str = "enterprise_docs",
    ) -> DocumentUploadResponse:
        """
        Process a document into semantic chunks and store them in Qdrant.
        """

        document_id = str(uuid.uuid4())

        metadata = {
            "document_id": document_id,
            "file_name": file_name,
            "uploaded_at": datetime.now().isoformat(),
        }

        # ----------------------------
        # Chunk document
        # ----------------------------
        nodes = self.embedding_engine.chunk_document(
            file_path=file_path,
            metadata=metadata,
        )

        chunks = [
            node.get_content()
            for node in nodes
        ]

        # ----------------------------
        # Metadata
        # ----------------------------
        file_type = Path(file_name).suffix.lower().replace(".", "")

        chunk_metadata: list[dict] = []

        for index, node in enumerate(nodes):

            chunk_text = node.get_content()

            chunk_metadata.append(
                {
                    "document_id": document_id,
                    "file_name": file_name,
                    "file_type": file_type,
                    "page_label": str(
                        node.metadata.get(
                            "page_label",
                            "1",
                        )
                    ),
                    "chunk_index": index,
                    "chunk_length": len(chunk_text),
                    "uploaded_at": metadata["uploaded_at"],
                }
            )

        # ----------------------------
        # Embeddings
        # ----------------------------
        embeddings = self.embedding_engine.generate_embeddings(
            chunks
        )

        # ----------------------------
        # Store
        # ----------------------------
        self.repository.upsert_chunks(
            collection_name=collection_name,
            chunks=chunks,
            embeddings=embeddings,
            metadata=chunk_metadata,
        )

        return DocumentUploadResponse(
            message="Document processed successfully.",
            document_id=document_id,
            chunks_processed=len(chunks),
            collection_name=collection_name,
        )

    def query_knowledge_base(
        self,
        request: QueryRequest,
    ) -> QueryResponse:
        """
        Query the enterprise knowledge base.
        """

        total_start = time.perf_counter()

        # ---------------------------------
        # Retrieve
        # ---------------------------------

        retrieval = self.retriever.retrieve(
            query=request.query,
            collection_name=request.collection_name,
            top_k=request.top_k,
        )

        context: list[str] = []
        sources: list[SourceChunk] = []

        for point in retrieval.points:
            payload = point.payload or {}

            text = str(payload.get("text", ""))

            context.append(text)

            sources.append(
                SourceChunk(
                    text=text[:200] + ("..." if len(text) > 200 else ""),
                    score=round(float(point.score), 4),
                    file_name=str(payload.get("file_name", "Unknown")),
                    page_label=str(payload.get("page_label", "1")),
                    chunk_index=payload.get("chunk_index"),
                    file_type=payload.get("file_type"),
                    chunk_length=payload.get("chunk_length"),
)
            )

        # ---------------------------------
        # Generate
        # ---------------------------------

        generation_start = time.perf_counter()

        answer = self.generator.generate_answer(
            query=request.query,
            context=context,
        )

        generation_time_ms = round(
            (time.perf_counter() - generation_start)
            * 1000,
            2,
        )

        total_time_ms = round(
            (time.perf_counter() - total_start)
            * 1000,
            2,
        )

        return QueryResponse(
            answer=answer,
            sources=sources,
            metrics=QueryMetrics(
                retrieval_time_ms=retrieval.retrieval_time_ms,
                generation_time_ms=generation_time_ms,
                total_time_ms=total_time_ms,
                chunks_retrieved=len(sources),
            ),
        )