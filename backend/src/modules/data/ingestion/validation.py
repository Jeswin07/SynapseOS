from fastapi import HTTPException

ALLOWED_EXTENSIONS = {
    ".csv",
    ".xlsx",
}

MAX_FILE_SIZE = 100 * 1024 * 1024


class DatasetValidator:
    """Dataset upload validation."""

    @staticmethod
    def validate_extension(
        filename: str,
    ) -> None:

        if not any(
            filename.endswith(ext)
            for ext in ALLOWED_EXTENSIONS
        ):
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type.",
            )