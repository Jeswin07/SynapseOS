"""FastAPI endpoints for Knowledge Intelligence."""

from __future__ import annotations

import os
import shutil
import tempfile

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)

from src.modules.knowledge.schemas import (
    DocumentUploadResponse,
    QueryRequest,
    QueryResponse,
)
from src.modules.knowledge.service import KnowledgeService

router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge Intelligence"],
)

knowledge_service = KnowledgeService()


def get_knowledge_service() -> KnowledgeService:
    """Return singleton KnowledgeService."""
    return knowledge_service


@router.post(
    "/ingest",
    response_model=DocumentUploadResponse,
)
async def ingest_document(
    file: UploadFile = File(...),
    collection_name: str = Form("enterprise_docs"),
    service: KnowledgeService = Depends(get_knowledge_service),
) -> DocumentUploadResponse:
    """
    Upload and index a document into the knowledge base.
    """

    filename = file.filename or "document.pdf"

    allowed_extensions = (
        ".pdf",
        ".txt",
        ".md",
        ".csv",
    )

    if not filename.lower().endswith(allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail=f"Supported file types: {allowed_extensions}",
        )

    temp_dir = tempfile.mkdtemp()

    temp_file = os.path.join(
        temp_dir,
        filename,
    )

    try:
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        return service.process_document(
            file_path=temp_file,
            file_name=filename,
            collection_name=collection_name,
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {exc}",
        ) from exc

    finally:
        shutil.rmtree(
            temp_dir,
            ignore_errors=True,
        )


@router.post(
    "/query",
    response_model=QueryResponse,
)
async def query_documents(
    request: QueryRequest,
    service: KnowledgeService = Depends(
        get_knowledge_service,
    ),
) -> QueryResponse:
    """
    Query the enterprise knowledge base.
    """

    try:
        return service.query_knowledge_base(request)

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Query failed: {exc}",
        ) from exc