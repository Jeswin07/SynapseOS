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
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.modules.auth.dependencies import get_current_user
from src.modules.knowledge.schemas import (
    DeleteDocumentResponse,
    DocumentUploadResponse,
    KnowledgeDocumentListResponse,
    KnowledgeDocumentResponse,
    QueryRequest,
    QueryResponse,
)
from src.modules.knowledge.service import KnowledgeService
from src.modules.knowledge.exceptions import (
    KnowledgeAccessDeniedException,
    KnowledgeDeleteException,
    KnowledgeDocumentNotFoundException,
)

router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge Intelligence"],
)


@router.post(
    "/ingest",
    response_model=DocumentUploadResponse,
)
async def ingest_document(
    file: UploadFile = File(...),
    collection_name: str = Form("enterprise_docs"),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DocumentUploadResponse:
    """
    Upload and index a document into the knowledge base.
    """

    service = KnowledgeService(db)

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
            tenant_id=current_user.tenant_id,
            uploaded_by=current_user.id,
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
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> QueryResponse:
    """
    Query the enterprise knowledge base.
    """

    service = KnowledgeService(db)

    try:
        return service.query_knowledge_base(request)

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Query failed: {exc}",
        ) from exc


@router.get(
    "/documents",
    response_model=KnowledgeDocumentListResponse,
)
def list_documents(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> KnowledgeDocumentListResponse:
    """
    List all uploaded knowledge documents for the current tenant.
    """

    service = KnowledgeService(db)

    documents = service.list_documents(
        tenant_id=current_user.tenant_id,
    )

    return KnowledgeDocumentListResponse(
        documents=[
            KnowledgeDocumentResponse.model_validate(document)
            for document in documents
        ]
    )

@router.get(
    "/documents/{document_id}",
    response_model=KnowledgeDocumentResponse,
)
def get_document(
    document_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> KnowledgeDocumentResponse:
    """
    Retrieve a knowledge document by its external document ID.
    """

    service = KnowledgeService(db)

    try:
        document = service.get_document(
            tenant_id=current_user.tenant_id,
            document_id=document_id,
        )

        return KnowledgeDocumentResponse.model_validate(document)

    except KnowledgeDocumentNotFoundException as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except KnowledgeAccessDeniedException as exc:
        raise HTTPException(
            status_code=403,
            detail=str(exc),
        ) from exc


@router.delete(
    "/documents/{document_id}",
    response_model=DeleteDocumentResponse,
)
def delete_document(
    document_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DeleteDocumentResponse:
    """
    Delete a knowledge document and all associated resources.
    """

    service = KnowledgeService(db)

    try:
        service.delete_document(
            tenant_id=current_user.tenant_id,
            document_id=document_id,
        )

        return DeleteDocumentResponse(
            message="Document deleted successfully.",
        )

    except KnowledgeDocumentNotFoundException as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except KnowledgeAccessDeniedException as exc:
        raise HTTPException(
            status_code=403,
            detail=str(exc),
        ) from exc

    except KnowledgeDeleteException as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc