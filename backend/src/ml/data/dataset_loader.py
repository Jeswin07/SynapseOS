"""Dataset loading utilities."""

from __future__ import annotations

import io
import uuid

import pandas as pd

from sqlalchemy.orm import Session

from src.core.storage.storage_service import (
    StorageService,
)

from src.modules.data.repository import (
    DatasetRepository,
)


class DatasetLoader:
    """
    Loads dataset versions from object storage.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.repository = DatasetRepository(
            db,
        )

        self.storage = StorageService()


    def load_version(
        self,
        dataset_version_id: uuid.UUID,
    ) -> dict[str, pd.DataFrame]:

        files = (
            self.repository.list_dataset_files(
                dataset_version_id,
            )
        )

        datasets = {}

        for dataset_file in files:

            response = (
                self.storage.download_file(
                    dataset_file.storage_path,
                )
            )

            try:

                file_bytes = response.read()

                dataframe = pd.read_csv(
                    io.BytesIO(
                        file_bytes,
                    )
                )

                datasets[
                    dataset_file.logical_name
                ] = dataframe

            finally:

                response.close()
                
                
        return datasets