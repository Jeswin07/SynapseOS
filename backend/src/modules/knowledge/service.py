"""Business logic orchestration for the Knowledge module."""

import time
import uuid

from qdrant_client.models import ScoredPoint
from src.ml.knowledge.retriever import Retriever
from src.ml.knowledge.embeddings import EmbeddingEngine
from src.ml.knowledge.generator import GroqGenerator
from src.modules.knowledge.repository import QdrantRepository
from src.modules.knowledge.schemas import (
    DocumentUploadResponse,
    QueryRequest,
    QueryResponse,
    SourceChunk,
)


class KnowledgeService:
    """Orchestrates RAG workflows: parsing, embedding, storing, and querying."""

    def __init__(self) -> None:
        """Initializes the required ML engines and data repositories."""
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
        """Chunks a document from disk, embeds it, and saves to Qdrant."""
        document_id = str(uuid.uuid4())
        metadata = {"file_name": file_name, "document_id": document_id}

        # 1. Chunk the document using LlamaIndex
        nodes = self.embedding_engine.chunk_document(
            file_path=file_path,
            metadata=metadata,
        )
        chunks = [str(node.get_content()) for node in nodes]

        # 2. Extract page numbers and metadata for tracking
        chunk_meta = [
            {
                "file_name": file_name,
                "document_id": document_id,
                "page_label": str(node.metadata.get("page_label", "1")),
            }
            for node in nodes
        ]

        # 3. Generate Embeddings & Upsert
        embeddings = self.embedding_engine.generate_embeddings(chunks)

        self.repository.upsert_chunks(
            collection_name=collection_name,
            chunks=chunks,
            embeddings=embeddings,
            metadata=chunk_meta,
        )

        return DocumentUploadResponse(
            message="Document successfully processed and vectorized.",
            document_id=document_id,
            chunks_processed=len(chunks),
            collection_name=collection_name,
        )

    def query_knowledge_base(self, request: QueryRequest) -> QueryResponse:
        """Embeds a query, searches Qdrant, and generates an LLM response."""
        start = time.time()

        results = self.retriever.retrieve(
            query=request.query,
            collection_name=request.collection_name,
            top_k=request.top_k,
        )

        context_texts: list[str] = []
        sources: list[SourceChunk] = []

        for result in results:
            payload = result.payload or {}
            text = str(payload.get("text", ""))
            
            context_texts.append(text)
            sources.append(
                SourceChunk(
                    text=text[:200] + "...",
                    score=float(result.score),
                    page_label=str(payload.get("page_label", "1")),
                    file_name=str(payload.get("file_name", "Unknown")),
                )
            )

        answer = self.generator.generate_answer(
            query=request.query,
            context=context_texts,
        )

        proc_time = round((time.time() - start) * 1000, 2)

        return QueryResponse(
            answer=answer,
            sources=sources,
            processing_time_ms=proc_time,
            chunks_retrieved=len(sources),
        )