"""Dataset version resolution."""

from __future__ import annotations

import uuid

from src.models.dataset_version import DatasetVersion
from src.modules.data.repository import (
    DatasetRepository,
)


class DatasetVersionResolver:
    """
    Resolves dataset versions for ML pipelines.
    """

    def __init__(
        self,
        repository: DatasetRepository,
    ) -> None:

        self.repository = repository


    def resolve(
        self,
        *,
        dataset_id: uuid.UUID | None = None,
        version_id: uuid.UUID | None = None,
        version_ids: list[uuid.UUID] | None = None,
        mode: str = "single",
    ) -> list[DatasetVersion]:


        if mode == "single":

            if version_id is None:
                raise ValueError(
                    "version_id is required."
                )

            version = (
                self.repository.get_dataset_version(
                    version_id,
                )
            )

            if version is None:
                raise ValueError(
                    "Dataset version not found."
                )

            return [
                version,
            ]


        if mode == "latest":

            if dataset_id is None:
                raise ValueError(
                    "dataset_id is required."
                )

            version = (
                self.repository.get_latest_version(
                    dataset_id,
                )
            )

            if version is None:
                raise ValueError(
                    "Dataset version not found."
                )

            return [
                version,
            ]


        if mode == "all":

            if dataset_id is None:
                raise ValueError(
                    "dataset_id is required."
                )

            return (
                self.repository.get_dataset_versions(
                    dataset_id,
                )
            )


        if mode == "selected":

            if not version_ids:
                raise ValueError(
                    "version_ids required."
                )

            versions: list[DatasetVersion] = []

            for item in version_ids:

                version = (
                    self.repository.get_dataset_version(
                        item,
                    )
                )

                if version is None:
                    raise ValueError(
                        "Dataset version not found."
                    )

                versions.append(
                    version,
                )


            return versions


        raise ValueError(
            "Invalid version mode."
        )