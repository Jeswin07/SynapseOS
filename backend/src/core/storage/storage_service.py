from io import BytesIO
from typing import BinaryIO

from minio.error import S3Error

from src.core.config import settings
from src.core.storage.exceptions import (
    UploadFailedError,
)
from src.core.storage.minio_client import client
from src.shared.logging import logger


class StorageService:
    """Service for object storage operations."""

    def upload_file(
        self,
        *,
        object_name: str,
        file: BinaryIO,
        file_size: int,
        content_type: str,
    ) -> None:
        """
        Upload a file to object storage.

        Args:
            object_name: Object storage path.
            file: File stream.
            file_size: File size in bytes.
            content_type: MIME type.

        Raises:
            UploadFailedError: If upload fails.
        """

        try:
            client.put_object(
                bucket_name=settings.minio_bucket_name,
                object_name=object_name,
                data=file,
                length=file_size,
                content_type=content_type,
            )

            logger.info(
                "File uploaded successfully.",
                extra={
                    "object_name": object_name,
                },
            )

        except S3Error as exc:
            logger.exception("File upload failed.")

            raise UploadFailedError(
                str(exc),
            ) from exc
        
    def ensure_bucket_exists(self) -> None:
        """
        Create bucket if it does not exist.
        """

        if not client.bucket_exists(
            settings.minio_bucket_name,
        ):
            client.make_bucket(
                settings.minio_bucket_name,
            )

    def download_file(
        self,
        object_name: str,
    ) -> BytesIO:
        """
        Download an object from MinIO.
        """

        response = client.get_object(
            settings.minio_bucket_name,
            object_name,
        )

        data = BytesIO(
            response.read()
        )

        response.close()
        response.release_conn()

        data.seek(0)

        return data