class StorageError(Exception):
    """Base storage exception."""


class UploadFailedError(StorageError):
    """Raised when file upload fails."""


class FileNotFoundError(StorageError):
    """Raised when object does not exist."""