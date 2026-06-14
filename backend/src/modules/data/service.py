import uuid

from sqlalchemy.orm import Session

from src.core.storage.storage_service import StorageService
from src.modules.data.repository import DatasetRepository
from src.models.dataset import Dataset
from src.shared.exceptions.dataset import (
    DatasetException,
)
from src.models.dataset_profile import DatasetProfile
from src.shared.logging import logger
from fastapi import UploadFile

from src.models.dataset_enums import (
    BusinessDomain,
    DatasetType,
)
from src.models.dataset_version import DatasetVersion

from src.core.storage.path_generator import (
    generate_dataset_object_path,
)

from src.shared.utils.checksum import (
    calculate_sha256,
)
from src.modules.data.profiling.profiler import DatasetProfiler


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
        file: UploadFile,
    ) -> DatasetVersion:
        """
        Upload a new dataset version.
        """

        try:

            dataset = self.repository.get_dataset_by_id_and_tenant(
                dataset_id=dataset_id,
                tenant_id=tenant_id,
            )

            if dataset is None:
                raise DatasetException(
                    "Dataset not found."
                )

            version = self.repository.get_next_version(
                dataset_id,
            )

            checksum = calculate_sha256(
                file.file,
            )

            if file.filename is None:
                raise ValueError("Filename is required")

            filename = file.filename

            object_path = generate_dataset_object_path(
                tenant_id=tenant_id,
                dataset_id=dataset.id,
                version=version,
                filename=filename,
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
                content_type=file.content_type
                or "application/octet-stream",
            )

            file.file.seek(0)

            file_bytes = file.file.read()

            profiler = DatasetProfiler()

            profile = profiler.profile(
                file_bytes,
            )

            dataset_version = DatasetVersion(
                dataset_id=dataset.id,
                version=version,
                storage_path=object_path,
                original_filename=file.filename,
                mime_type=file.content_type
                or "application/octet-stream",
                file_size=file_size,
                checksum=checksum,
                uploaded_by=uploaded_by,
                )

            self.repository.create_dataset_version(
                dataset_version,
            )

            dataset_profile = DatasetProfile(
                dataset_version_id=dataset_version.id,
                row_count=profile["row_count"],
                column_count=profile["column_count"],
                duplicate_rows=profile["duplicate_rows"],
                column_metadata=profile["dtypes"],
                null_counts=profile["null_count"],
            )

            self.repository.create_dataset_profile(
                dataset_profile,
            )

            self.repository.commit()

            self.repository.refresh(
                dataset_version,
            )

            logger.info(
                "Dataset version uploaded.",
                extra={
                    "dataset_id": str(dataset.id),
                    "version": version,
                },
            )

            return dataset_version

        except Exception:

            self.repository.rollback()

            raise