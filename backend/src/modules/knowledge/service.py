"""Business logic orchestration for the Knowledge module."""

from __future__ import annotations

import mimetypes
import os
import time
import uuid
from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.storage.storage_service import StorageService
from src.ml.knowledge.embeddings import EmbeddingEngine
from src.ml.knowledge.generator import GroqGenerator
from src.ml.knowledge.graph.graph_builder import GraphBuilder
from src.ml.knowledge.graph.graph_retriever import GraphRetriever
from src.ml.knowledge.hybrid_retriever import HybridRetriever
from src.ml.knowledge.reranker import CrossEncoderReranker
from src.ml.knowledge.retrieval_models import RetrievedChunk
from src.models.knowledge_document import (
    KnowledgeDocument,
    KnowledgeDocumentStatus,
)
from src.modules.knowledge.document_repository import (
    KnowledgeDocumentRepository,
)
from src.modules.knowledge.exceptions import (
    KnowledgeAccessDeniedException,
    KnowledgeDeleteException,
    KnowledgeDocumentNotFoundException,
)
from src.modules.knowledge.qdrant_repository import QdrantRepository
from src.modules.knowledge.schemas import (
    DocumentUploadResponse,
    QueryMetrics,
    QueryRequest,
    QueryResponse,
    SourceChunk,
)


class KnowledgeService:
    """Orchestrates RAG workflows."""

    def __init__(self, db: Session) -> None:
        self.db = db

        # Database
        self.document_repository = KnowledgeDocumentRepository(db)

        # Object Storage
        self.storage = StorageService()

        # AI Components
        self.embedding_engine = EmbeddingEngine()
        self.qdrant_repository = QdrantRepository()
        self.generator = GroqGenerator()

        # Graph
        self.graph_builder = GraphBuilder()

        # Retrieval
        self.hybrid_retriever = HybridRetriever()
        self.graph_retriever = GraphRetriever()
        self.reranker = CrossEncoderReranker()

    def process_document(
        self,
        *,
        tenant_id,
        uploaded_by,
        file_path: str,
        file_name: str,
        collection_name: str = settings.knowledge_collection,
    ) -> DocumentUploadResponse:
        """
        Process a document into semantic chunks and store them in Qdrant
        while simultaneously building the Neo4j Knowledge Graph.
        """

        document_id = str(uuid.uuid4())

        uploaded_at = datetime.now()

        file_type = (
            Path(file_name)
            .suffix
            .lower()
            .replace(".", "")
        )

        metadata = {
            "document_id": document_id,
            "file_name": file_name,
            "uploaded_at": uploaded_at.isoformat(),
        }

        document = KnowledgeDocument(
            tenant_id=tenant_id,
            uploaded_by=uploaded_by,
            filename=file_name,
            file_type=file_type,
            document_id=document_id,
            chunk_count=0,
            status=KnowledgeDocumentStatus.UPLOADING,
        )

        try:

            self.document_repository.create_document(document)

            self.document_repository.flush()

            object_name = (
                f"{tenant_id}/knowledge/"
                f"{document_id}/{file_name}"
            )

            file_size = os.path.getsize(file_path)

            content_type = (
                mimetypes.guess_type(file_name)[0]
                or "application/octet-stream"
            )

            with open(file_path, "rb") as file:

                self.storage.upload_file(
                    object_name=object_name,
                    file=file,
                    file_size=file_size,
                    content_type=content_type,
                )

            document.status = KnowledgeDocumentStatus.PROCESSING

            self.document_repository.commit()

        except Exception:

            self.document_repository.rollback()

            raise

        # -------------------------------------------------
        # Chunk Document
        # -------------------------------------------------
        try:

            nodes = self.embedding_engine.chunk_document(
                file_path=file_path,
                metadata=metadata,
            )

            chunks = [
                node.get_content()
                for node in nodes
            ]

            document.chunk_count = len(chunks)

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

                try:
                    page_number = int(page_label)
                except (TypeError, ValueError):
                    page_number = None

                chunk_metadata.append(
                    {
                        "document_id": document_id,
                        "tenant_id": str(tenant_id),

                        "file_name": file_name,
                        "file_type": file_type,

                        "page_label": page_label,
                        "page_number": page_number,

                        "chunk_index": index,
                        "chunk_id": f"{document_id}_chunk_{index:04d}",
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
                        "document_id": document_id,
                        "tenant_id": str(tenant_id),
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

            self.qdrant_repository.upsert_chunks(
                collection_name=collection_name,
                chunks=chunks,
                embeddings=embeddings,
                metadata=chunk_metadata,
            )

        # -------------------------------------------------
        # Build Neo4j Knowledge Graph
        # -------------------------------------------------

            self.graph_builder.build(graph_chunks)

        # -------------------------------------------------
        # Refresh Hybrid BM25 Index
        # -------------------------------------------------

            self.hybrid_retriever.invalidate_index()

            document.status = KnowledgeDocumentStatus.READY

            self.document_repository.commit()

            self.document_repository.refresh(document)
        
        except Exception:

            self.document_repository.rollback()

            document.status = KnowledgeDocumentStatus.FAILED

            try:
                self.qdrant_repository.delete_document(
                    collection_name=collection_name,
                    document_id=document_id,
                )
            except Exception:
                pass

            try:
                self.graph_builder.delete_document(document_id)
            except Exception:
                pass

            self.document_repository.commit()

            raise

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
            payload = chunk.payload or {}

            chunk_id = payload.get("chunk_id")

            if chunk_id is None:
                continue

            candidate_map[chunk_id] = chunk

        for chunk in graph:

            payload = chunk.payload or {}

            chunk_id = payload.get("chunk_id")

            if chunk_id is None:
                continue

            candidate_map.setdefault(
                chunk_id,
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

    
    def answer(
        self,
        query: str,
        collection_name: str = settings.knowledge_collection,
        top_k: int | None = None,
        ) -> QueryResponse:
        """
        Convenience method for AI agents.

        Keeps the Agent layer independent from API schemas.
        """

        request = QueryRequest(
            query=query,
            collection_name=collection_name,
            top_k=top_k or settings.rag_top_k,
        )

        return self.query_knowledge_base(request)
    
    def list_documents(
        self,
        *,
        tenant_id,
    ) -> list[KnowledgeDocument]:
        """
        Retrieve all uploaded knowledge documents for a tenant.

        Args:
            tenant_id: Tenant UUID.

        Returns:
            List of knowledge documents ordered by newest first.
        """

        return self.document_repository.list_documents(
            tenant_id=tenant_id,
        )

    def get_document(
        self,
        *,
        tenant_id,
        document_id: str,
    ) -> KnowledgeDocument:
        """
        Retrieve a knowledge document belonging to a tenant.

        Args:
            tenant_id: Tenant UUID.
            document_id: External document ID.

        Returns:
            KnowledgeDocument.

        Raises:
            ValueError: If the document does not exist or does not belong
                to the tenant.
        """

        document = self.document_repository.get_document_by_document_id(
            document_id=document_id,
        )

        if document is None:
            raise KnowledgeDocumentNotFoundException(
                document_id,
            )

        if document.tenant_id != tenant_id:
            raise KnowledgeAccessDeniedException()

        return document
    
    def delete_document(
        self,
        *,
        tenant_id,
        document_id: str,
        collection_name: str = settings.knowledge_collection,
    ) -> None:
        """
        Delete a knowledge document and all associated resources.

        Deletes:
            - PostgreSQL metadata
            - Qdrant vectors
            - MinIO object
            - Neo4j graph (if enabled)

        Args:
            tenant_id:
                Tenant UUID.

            document_id:
                External document identifier.

            collection_name:
                Qdrant collection.
        """

        document = self.get_document(
            tenant_id=tenant_id,
            document_id=document_id,
        )

        object_name = (
            f"{tenant_id}/knowledge/"
            f"{document.document_id}/{document.filename}"
        )

        try:

        # -----------------------------------------
        # Delete vectors
        # -----------------------------------------

            document_id_str = str(document.document_id)

            self.qdrant_repository.delete_document(
                collection_name=collection_name,
                document_id=document_id_str,
            )

        # -----------------------------------------
        # Delete original file
        # -----------------------------------------

            self.storage.delete_file(
                object_name=object_name,
            )

        # -----------------------------------------
        # Delete graph
        # -----------------------------------------

            self.graph_builder.delete_document(
                document_id_str,
            )

        # -----------------------------------------
        # Delete metadata
        # -----------------------------------------

            self.document_repository.delete_document(
                document,
            )

            self.document_repository.commit()

        # -----------------------------------------
        # Refresh Hybrid Index
        # -----------------------------------------

            self.hybrid_retriever.invalidate_index()

        except Exception as exc:

            self.document_repository.rollback()

            raise KnowledgeDeleteException(
                str(exc),
            ) from exc