from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.modules.auth.dependencies import (
    get_current_user,
)
from src.modules.data.schemas import (
    DatasetCreateRequest,
    DatasetCreateResponse,
    DatasetVersionResponse,
)
from src.modules.data.service import DatasetService
from src.shared.exceptions.dataset import (
    DatasetException,
)

router = APIRouter(
    prefix="/datasets",
    tags=["Datasets"],
)


@router.post(
    "",
    response_model=DatasetCreateResponse,
    status_code=201,
)
def create_dataset(
    payload: DatasetCreateRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new dataset.
    """

    service = DatasetService(db)

    try:

        dataset = service.create_dataset(
            tenant_id=current_user.tenant_id,
            created_by=current_user.id,
            name=payload.name,
            description=payload.description,
            dataset_type=payload.dataset_type,
            business_domain=payload.business_domain,
            tags=payload.tags,
        )

        return DatasetCreateResponse(
            dataset_id=dataset.id,
            message="Dataset created successfully.",
        )

    except DatasetException as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post(
    "/{dataset_id}/versions",
    response_model=DatasetVersionResponse,
    status_code=201,
)
async def upload_dataset_version(
    dataset_id: UUID,
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Upload a new version of an existing dataset.
    """

    service = DatasetService(db)

    try:

        version = await service.upload_dataset_version(
            dataset_id=dataset_id,
            tenant_id=current_user.tenant_id,
            uploaded_by=current_user.id,
            file=file,
        )

        return DatasetVersionResponse(
            version_id=version.id,
            version=version.version,
            message="Dataset version uploaded successfully.",
        )

    except DatasetException as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get("")
def list_datasets(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    List all datasets belonging to the authenticated tenant.
    """

    service = DatasetService(db)

    return service.list_datasets(
        tenant_id=current_user.tenant_id,
    )


@router.get("/{dataset_id}")
def get_dataset(
    dataset_id: UUID,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve a dataset by its ID.
    """

    service = DatasetService(db)

    try:

        dataset = service.get_dataset(
            dataset_id=dataset_id,
        )

        if dataset.tenant_id != current_user.tenant_id:
            raise HTTPException(
                status_code=403,
                detail="Access denied.",
            )

        return dataset

    except DatasetException as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )