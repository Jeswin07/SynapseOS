"""FastAPI endpoints for Knowledge Intelligence."""

import os
import shutil
import tempfile
import traceback

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from src.modules.knowledge.schemas import (
    DocumentUploadResponse,
    QueryRequest,
    QueryResponse,
)
from src.modules.knowledge.service import KnowledgeService

router = APIRouter(prefix="/knowledge", tags=["Knowledge Intelligence"])


def get_knowledge_service() -> KnowledgeService:
    """Dependency injection for the Knowledge Service."""
    return KnowledgeService()


@router.post("/ingest", response_model=DocumentUploadResponse)
async def ingest_document(
    file: UploadFile = File(...),
    collection_name: str = Form("enterprise_docs"),
    service: KnowledgeService = Depends(get_knowledge_service),
) -> DocumentUploadResponse:
    """Ingests a file (PDF, CSV, TXT), chunks it, and vectorizes it."""
    filename: str = file.filename or "unnamed_document.pdf"
    allowed_exts = (".txt", ".md", ".csv", ".pdf")

    if not filename.lower().endswith(allowed_exts):
        raise HTTPException(
            status_code=400,
            detail=f"Only {allowed_exts} files are supported.",
        )

    # Save UploadFile to a temporary disk location for LlamaIndex parsing
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, filename)

    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        response = service.process_document(
            file_path=temp_file_path,
            file_name=filename,
            collection_name=collection_name,
        )
        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process document: {str(e)}",
        )
    finally:
        # Ensure cleanup of the temporary file to prevent memory leaks
        shutil.rmtree(temp_dir, ignore_errors=True)


@router.post("/query", response_model=QueryResponse)
async def query_documents(
    request: QueryRequest,
    service: KnowledgeService = Depends(get_knowledge_service),
) -> QueryResponse:
    """Queries the enterprise knowledge base and generates an answer."""
    try:
        return service.query_knowledge_base(request)
    except Exception as e:
        traceback.print_exc()
        raise