import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session

from src.core.storage.path_generator import (
    generate_dataset_object_path,
)
from src.core.storage.storage_service import StorageService
from src.models.dataset import Dataset
from src.models.dataset_enums import (
    BusinessDomain,
    DatasetType,
)
from src.models.dataset_file import DatasetFile
from src.models.dataset_profile import DatasetProfile
from src.models.dataset_version import DatasetVersion
from src.modules.data.logical_detector import (
    LogicalNameDetector,
)
from src.modules.data.profiling.profiler import DatasetProfiler
from src.modules.data.repository import DatasetRepository
from src.shared.exceptions.dataset import (
    DatasetException,
)
from src.shared.logging import logger
from src.shared.utils.checksum import (
    calculate_sha256,
)
from src.ml.cache.feature_cache import (
    FeatureCache,
)


class DatasetService:
    """
    Service responsible for dataset business operations.

    This service orchestrates dataset creation, versioning,
    storage, and profiling while delegating persistence to the
    repository layer and file storage to the storage service.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        """
        Initialize DatasetService.

        Args:
            db: SQLAlchemy database session.
        """
        self.repository = DatasetRepository(db)
        self.storage = StorageService()

    def upload_dataset(
        self,
        *args,
        **kwargs,
    ):
        """
        Upload a new dataset.

        Workflow:
            1. Validate upload
            2. Create dataset
            3. Upload file to object storage
            4. Create dataset version
            5. Commit transaction
            6. Trigger background profiling

        Raises:
            NotImplementedError: Upload pipeline is implemented
            in the next sprint.
        """

        logger.info(
            "Dataset upload requested."
        )

        raise NotImplementedError(
            "Dataset upload is not implemented yet."
        )

    def list_datasets(
        self,
        tenant_id: uuid.UUID,
    )-> list[Dataset]:
        """
        Retrieve all datasets for a tenant.

        Args:
            tenant_id: Tenant UUID.

        Returns:
            List of datasets.
        """

        logger.info(
            "Fetching datasets.",
            extra={
                "tenant_id": str(tenant_id),
            },
        )

        return self.repository.list_datasets(
            tenant_id,
        )

    def get_dataset(
        self,
        dataset_id: uuid.UUID,
    ) -> Dataset:
        """
        Retrieve a dataset by its ID.

        Args:
            dataset_id: Dataset UUID.

        Returns:
            Dataset instance.

        Raises:
            DatasetException:
                If the dataset does not exist.
        """

        dataset = (
            self.repository.get_dataset_by_id(
                dataset_id,
            )
        )

        if dataset is None:
            logger.warning(
                "Dataset not found.",
                extra={
                    "dataset_id": str(dataset_id),
                },
            )

            raise DatasetException(
                "Dataset not found."
            )

        logger.info(
            "Dataset retrieved.",
            extra={
                "dataset_id": str(dataset_id),
            },
        )

        return dataset
    
    def create_dataset(
        self,
        *,
        tenant_id: uuid.UUID,
        created_by: uuid.UUID,
        name: str,
        description: str | None,
        dataset_type:DatasetType,
        business_domain:BusinessDomain,
        tags: list[str] | None,
    ):
        """
        Create a new dataset.

        Args:
            tenant_id: Tenant UUID.
            created_by: User UUID.
            name: Dataset name.
            description: Dataset description.
            dataset_type: Dataset type.
            business_domain: Business domain.
            tags: Dataset tags.

        Returns:
            Newly created dataset.
        """

        logger.info(
            "Creating dataset.",
            extra={
                "tenant_id": str(tenant_id),
                "dataset_name": name,
            },
        )

        if self.repository.exists_by_name(
            tenant_id,
            name,
        ):
            raise DatasetException(
                "Dataset already exists."
            )

        dataset = Dataset(
            tenant_id=tenant_id,
            created_by=created_by,
            name=name,
            description=description,
            dataset_type=dataset_type,
            business_domain=business_domain,
            tags=tags,
        )

        self.repository.create_dataset(
            dataset,
        )

        self.repository.commit()

        self.repository.refresh(dataset)

        logger.info(
            "Dataset created successfully.",
            extra={
                "dataset_id": str(dataset.id),
            },
        )

        return dataset
    
    async def upload_dataset_version(
        self,
        *,
        dataset_id: uuid.UUID,
        tenant_id: uuid.UUID,
        uploaded_by: uuid.UUID,
        files: list[UploadFile],
    ) -> DatasetVersion:
        """
        Upload a new dataset version containing multiple files.
        """

        try:

            dataset = (
                self.repository.get_dataset_by_id_and_tenant(
                    dataset_id=dataset_id,
                    tenant_id=tenant_id,
                )
            )

            if dataset is None:
                raise DatasetException(
                    "Dataset not found."
                )

            version_number = (
                self.repository.get_next_version(
                    dataset_id,
                )
            )

            dataset_version = DatasetVersion(
                dataset_id=dataset.id,
                version=version_number,
                uploaded_by=uploaded_by,
            )

            self.repository.create_dataset_version(
                dataset_version,
            )

            self.repository.db.flush()

            profiler = DatasetProfiler()

            for file in files:

                if file.filename is None:
                    raise DatasetException(
                        "Filename missing."
                    )

                checksum = calculate_sha256(
                    file.file,
                )

                object_path = (
                    generate_dataset_object_path(
                        tenant_id=tenant_id,
                        dataset_id=dataset.id,
                        version=version_number,
                        filename=file.filename,
                    )
                )

                file.file.seek(0)

                file.file.seek(
                    0,
                    2,
                )

                file_size = file.file.tell()

                file.file.seek(0)

                self.storage.upload_file(
                    object_name=object_path,
                    file=file.file,
                    file_size=file_size,
                    content_type=(
                        file.content_type
                        or "application/octet-stream"
                    ),
                )

                file.file.seek(0)

                file_bytes = file.file.read()

                profile = profiler.profile(
                    file_bytes,
                )

                logical_name = LogicalNameDetector.detect(
                    file.filename,
                )

                dataset_file = DatasetFile(
                    dataset_version_id=dataset_version.id,
                    logical_name=logical_name,
                    original_filename=file.filename,
                    storage_path=object_path,
                    mime_type=(
                        file.content_type
                        or "application/octet-stream"
                    ),
                    file_size=file_size,
                    checksum=checksum,
                    rows_count=profile["row_count"],
                    columns_count=profile["column_count"],
                    schema={
                        "columns": profile["columns"],
                        "dtypes": profile["dtypes"],
                    },
                )

                self.repository.create_dataset_file(
                    dataset_file,
                )

                self.repository.db.flush()

                dataset_profile = DatasetProfile(
                    dataset_file_id=dataset_file.id,
                    profile=profile,
                    quality_score=None,
                )

                self.repository.create_dataset_profile(
                    dataset_profile,
                )

            self.repository.commit()
            FeatureCache.clear()

            self.repository.refresh(
                dataset_version,
            )

            logger.info(
                "Dataset version uploaded.",
                extra={
                    "dataset_id": str(dataset.id),
                    "version": version_number,
                    "files": len(files),
                },
            )

            return dataset_version

        except Exception:

            self.repository.rollback()

            raise

    def get_dataset_versions(
        self,
        dataset_id: uuid.UUID,
    ):
        """
        Retrieve dataset version history.
        """

        dataset = self.repository.get_dataset_by_id(
            dataset_id,
        )

        if dataset is None:
            raise DatasetException(
                "Dataset not found."
            )

        return self.repository.get_dataset_versions(
            dataset_id,
        )
    

    def download_dataset_file(
        self,
        dataset_file_id: uuid.UUID,
    ):
        """
        Download a specific dataset file.
        """

        dataset_file = (
            self.repository.get_dataset_file_by_id(
                dataset_file_id,
            )
        )

        if dataset_file is None:
            raise DatasetException(
                "Dataset file not found."
            )

        return (
            self.storage.download_file(
                dataset_file.storage_path,
            ),
            dataset_file.original_filename,
        )
    

    def delete_dataset(
        self,
        dataset_id: uuid.UUID,
        tenant_id: uuid.UUID,
    ) -> None:

        dataset = (
            self.repository.get_dataset_by_id_and_tenant(
                dataset_id,
                tenant_id,
            )
        )

        if dataset is None:
            raise DatasetException(
                "Dataset not found."
            )

        self.repository.delete_dataset(
            dataset,
        )

        self.repository.commit()

    
    def get_dataset_files(
        self,
        dataset_version_id: uuid.UUID,
    ):

        return (
            self.repository.list_dataset_files(
                dataset_version_id,
            )
        )