from io import BytesIO

import polars as pl

from src.core.config import settings
from src.core.storage.minio_client import client


class DatasetLoader:
    """
    Loads datasets from object storage.
    """

    def load_csv(
        self,
        storage_path: str,
    ) -> pl.DataFrame:
        """
        Load a CSV dataset from MinIO.

        Args:
            storage_path: Object storage path.

        Returns:
            Polars DataFrame.
        """

        response = client.get_object(
            bucket_name=settings.minio_bucket_name,
            object_name=storage_path,
        )

        try:

            data = response.read()

        finally:

            response.close()
            response.release_conn()

        return pl.read_csv(
            BytesIO(data),
        )