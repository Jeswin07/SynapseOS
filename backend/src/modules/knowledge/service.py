"""Business logic orchestration for the Knowledge module."""

from __future__ import annotations

import time
import uuid
from datetime import datetime
from pathlib import Path

from src.core.config import settings
from src.ml.knowledge.embeddings import EmbeddingEngine
from src.ml.knowledge.generator import GroqGenerator
from src.ml.knowledge.graph.graph_builder import GraphBuilder
from src.ml.knowledge.graph.graph_retriever import GraphRetriever
from src.ml.knowledge.hybrid_retriever import HybridRetriever
from src.ml.knowledge.reranker import CrossEncoderReranker
from src.ml.knowledge.retrieval_models import RetrievedChunk
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

        # Retrieval Pipeline
        self.hybrid_retriever = HybridRetriever()
        self.graph_retriever = GraphRetriever()
        self.reranker = CrossEncoderReranker()

    def process_document(
        self,
        file_path: str,
        file_name: str,
        collection_name: str = "enterprise_docs",
    ) -> DocumentUploadResponse:
        """
        Process a document into semantic chunks and store them in Qdrant
        while simultaneously building the Neo4j Knowledge Graph.
        """

        document_id = str(uuid.uuid4())

        metadata = {
            "document_id": document_id,
            "file_name": file_name,
            "uploaded_at": datetime.now().isoformat(),
        }

        # -------------------------------------------------
        # Chunk Document
        # -------------------------------------------------

        nodes = self.embedding_engine.chunk_document(
            file_path=file_path,
            metadata=metadata,
        )

        chunks = [
            node.get_content()
            for node in nodes
        ]

        # -------------------------------------------------
        # Chunk Metadata
        # -------------------------------------------------

        file_type = (
            Path(file_name)
            .suffix
            .lower()
            .replace(".", "")
        )

        chunk_metadata: list[dict] = []

        for index, node in enumerate(nodes):

            chunk_text = node.get_content()

            page_label = str(
                node.metadata.get(
                    "page_label",
                    "1",
                )
            )

            page_number = int(page_label)

            chunk_metadata.append(
                {
                    "document_id": document_id,
                    "file_name": file_name,
                    "file_type": file_type,
                    "page_label": page_label,
                    "page_number": page_number,
                    "chunk_index": index,
                    "chunk_id": (
                        f"{document_id}_chunk_{index:04d}"
                    ),
                    "chunk_length": len(chunk_text),
                    "uploaded_at": metadata["uploaded_at"],
                }
            )

        # -------------------------------------------------
        # Graph Metadata
        # -------------------------------------------------

        graph_chunks: list[dict] = []

        for chunk, meta in zip(
            chunks,
            chunk_metadata,
        ):

            graph_chunks.append(
                {
                    "chunk_id": meta["chunk_id"],
                    "text": chunk,
                    "file_name": meta["file_name"],
                    "page_label": meta["page_label"],
                }
            )

        # -------------------------------------------------
        # Generate Embeddings
        # -------------------------------------------------

        embeddings = (
            self.embedding_engine.generate_embeddings(
                chunks
            )
        )

        # -------------------------------------------------
        # Store in Qdrant
        # -------------------------------------------------

        self.repository.upsert_chunks(
            collection_name=collection_name,
            chunks=chunks,
            embeddings=embeddings,
            metadata=chunk_metadata,
        )

        # -------------------------------------------------
        # Build Neo4j Knowledge Graph
        # -------------------------------------------------

        graph_builder = GraphBuilder()

        try:
            graph_builder.build(graph_chunks)
        finally:
            graph_builder.close()

        # -------------------------------------------------
        # Refresh Hybrid BM25 Index
        # -------------------------------------------------

        self.hybrid_retriever.invalidate_index()

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
        Query the enterprise knowledge base using the complete
        GraphRAG retrieval pipeline.

        Pipeline
        --------
        Hybrid Retrieval
            +
        Graph Retrieval
            ↓
        Candidate Merge
            ↓
        CrossEncoder Reranker
            ↓
        LLM Generation
        """

        total_start = time.perf_counter()

    # -------------------------------------------------
    # Hybrid Retrieval
    # -------------------------------------------------

        hybrid = self.hybrid_retriever.retrieve(
            query=request.query,
            collection_name=request.collection_name,
            candidate_k=settings.rag_candidate_k,
        )

    # -------------------------------------------------
    # Graph Retrieval
    # -------------------------------------------------
        rerank_start = time.perf_counter()

        graph = self.graph_retriever.retrieve(
            query=request.query,
            top_k=max(
                request.top_k * 2,
                10,
            ),
        )

        rerank_ms = round(
            (time.perf_counter() - rerank_start) * 1000,
            2,
        )

        print(f"Graph Retrieval: {rerank_ms} ms")

    # -------------------------------------------------
    # Merge Candidates
    # -------------------------------------------------

        candidate_map: dict[str, RetrievedChunk] = {}

        for chunk in hybrid.points:
            candidate_map[
                chunk.payload["chunk_id"]
            ] = chunk

        for chunk in graph:
            candidate_map.setdefault(
                chunk.payload["chunk_id"],
                chunk,
            )

        candidates = list(candidate_map.values())

    # -------------------------------------------------
    # CrossEncoder Reranking
    # -------------------------------------------------
        rerank_start = time.perf_counter()

        points = self.reranker.rerank(
            query=request.query,
            candidates=candidates,
            top_k=request.top_k,
        )

        rerank_ms = round(
            (time.perf_counter() - rerank_start) * 1000,
            2,
        )

        print(f"Reranker: {rerank_ms} ms")

    # -------------------------------------------------
    # Build Context
    # -------------------------------------------------

        context: list[str] = []

        sources: list[SourceChunk] = []

        for point in points:

            payload = point.payload or {}

            text = str(
                payload.get(
                    "text",
                    "",
                )
            )

            context.append(text)

            sources.append(
                SourceChunk(
                    text=text[:200]
                    + (
                        "..."
                        if len(text) > 200
                        else ""
                    ),
                    score=round(
                        float(point.score),
                        4,
                    ),
                    file_name=str(
                        payload.get(
                            "file_name",
                            "Unknown",
                        )
                    ),
                    page_label=str(
                        payload.get(
                            "page_label",
                            "1",
                        )
                    ),
                    page_number=payload.get(
                        "page_number",
                    ),
                    chunk_index=payload.get(
                        "chunk_index",
                    ),
                    chunk_id=payload.get(
                        "chunk_id",
                    ),
                    file_type=payload.get(
                        "file_type",
                    ),
                    chunk_length=payload.get(
                        "chunk_length",
                    ),
                )
            )

    # -------------------------------------------------
    # Generate Answer
    # -------------------------------------------------

        generation_start = time.perf_counter()

        answer = self.generator.generate_answer(
            query=request.query,
            context=context,
        )

        generation_time_ms = round(
            (
                time.perf_counter()
                - generation_start
            )
            * 1000,
            2,
        )

        total_time_ms = round(
            (
                time.perf_counter()
                - total_start
            )
            * 1000,
            2,
        )

    # -------------------------------------------------
    # Response
    # -------------------------------------------------

        return QueryResponse(
            answer=answer,
            sources=sources,
            metrics=QueryMetrics(
                retrieval_time_ms=hybrid.retrieval_time_ms,
                generation_time_ms=generation_time_ms,
                total_time_ms=total_time_ms,
                chunks_retrieved=len(points),
                average_similarity=hybrid.average_similarity,
                highest_similarity=hybrid.highest_similarity,
            ),
        )