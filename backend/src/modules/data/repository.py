"""
Repository layer for dataset persistence operations.
"""

import uuid

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.dataset import Dataset
from src.models.dataset_profile import DatasetProfile
from src.models.dataset_version import DatasetVersion


class DatasetRepository:
    """
    Repository for dataset persistence operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        """
        Initialize the repository.

        Args:
            db: SQLAlchemy database session.
        """
        self.db = db

    # -------------------------------------------------------------------------
    # Dataset
    # -------------------------------------------------------------------------

    def create_dataset(
        self,
        dataset: Dataset,
    ) -> Dataset:
        """
        Persist a dataset.

        Args:
            dataset: Dataset instance.

        Returns:
            Persisted dataset.
        """
        self.db.add(dataset)

        return dataset

    def get_dataset_by_id(
        self,
        dataset_id: uuid.UUID,
    ) -> Dataset | None:
        """
        Retrieve dataset by ID.

        Args:
            dataset_id: Dataset UUID.

        Returns:
            Dataset if found, otherwise None.
        """
        return (
            self.db.query(Dataset)
            .filter(
                Dataset.id == dataset_id,
            )
            .first()
        )

    def get_dataset_by_id_and_tenant(
        self,
        dataset_id: uuid.UUID,
        tenant_id: uuid.UUID,
    ) -> Dataset | None:
        """
        Retrieve dataset belonging to a tenant.

        Args:
            dataset_id: Dataset UUID.
            tenant_id: Tenant UUID.

        Returns:
            Dataset if found.
        """
        return (
            self.db.query(Dataset)
            .filter(
                Dataset.id == dataset_id,
                Dataset.tenant_id == tenant_id,
                Dataset.is_active.is_(True),
            )
            .first()
        )

    def exists_by_name(
        self,
        tenant_id: uuid.UUID,
        name: str,
    ) -> bool:
        """
        Check whether a dataset with the given name already exists.

        Args:
            tenant_id: Tenant UUID.
            name: Dataset name.

        Returns:
            True if dataset exists.
        """
        return (
            self.db.query(Dataset)
            .filter(
                Dataset.tenant_id == tenant_id,
                Dataset.name == name,
                Dataset.is_active.is_(True),
            )
            .first()
            is not None
        )

    def list_datasets(
        self,
        tenant_id: uuid.UUID,
    ) -> list[Dataset]:
        """
        Retrieve all datasets for a tenant.

        Args:
            tenant_id: Tenant UUID.

        Returns:
            List of datasets.
        """
        return (
            self.db.query(Dataset)
            .filter(
                Dataset.tenant_id == tenant_id,
                Dataset.is_active.is_(True),
            )
            .order_by(
                Dataset.created_at.desc(),
            )
            .all()
        )

    # -------------------------------------------------------------------------
    # Dataset Version
    # -------------------------------------------------------------------------

    def create_dataset_version(
        self,
        version: DatasetVersion,
    ) -> DatasetVersion:
        """
        Persist a dataset version.

        Args:
            version: DatasetVersion instance.

        Returns:
            Persisted dataset version.
        """
        self.db.add(version)

        return version

    def get_next_version(
        self,
        dataset_id: uuid.UUID,
    ) -> int:
        """
        Get the next version number.

        Args:
            dataset_id: Dataset UUID.

        Returns:
            Next version number.
        """
        latest = (
            self.db.query(
                func.max(DatasetVersion.version)
            )
            .filter(
                DatasetVersion.dataset_id == dataset_id,
            )
            .scalar()
        )

        return (latest or 0) + 1

    def list_versions(
        self,
        dataset_id: uuid.UUID,
    ) -> list[DatasetVersion]:
        """
        Retrieve all versions of a dataset.

        Args:
            dataset_id: Dataset UUID.

        Returns:
            List of dataset versions.
        """
        return (
            self.db.query(DatasetVersion)
            .filter(
                DatasetVersion.dataset_id == dataset_id,
            )
            .order_by(
                DatasetVersion.version.desc(),
            )
            .all()
        )

    # -------------------------------------------------------------------------
    # Dataset Profile
    # -------------------------------------------------------------------------

    def create_dataset_profile(
        self,
        profile: DatasetProfile,
    ) -> DatasetProfile:
        """
        Persist dataset profile.

        Args:
            profile: DatasetProfile instance.

        Returns:
            Persisted dataset profile.
        """
        self.db.add(profile)

        return profile

    def get_dataset_profile(
        self,
        dataset_version_id: uuid.UUID,
    ) -> DatasetProfile | None:
        """
        Retrieve profile for a dataset version.

        Args:
            dataset_version_id: DatasetVersion UUID.

        Returns:
            DatasetProfile if found.
        """
        return (
            self.db.query(DatasetProfile)
            .filter(
                DatasetProfile.dataset_version_id
                == dataset_version_id,
            )
            .first()
        )

    # -------------------------------------------------------------------------
    # Transaction
    # -------------------------------------------------------------------------

    def commit(self) -> None:
        """Commit current transaction."""
        self.db.commit()

    def rollback(self) -> None:
        """Rollback current transaction."""
        self.db.rollback()

    def refresh(
        self,
        instance: object,
    ) -> None:
        """
        Refresh ORM instance.

        Args:
            instance: SQLAlchemy ORM instance.
        """
        self.db.refresh(instance)