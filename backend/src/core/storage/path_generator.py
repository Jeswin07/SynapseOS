import uuid
from pathlib import Path


def generate_dataset_object_path(
    tenant_id: uuid.UUID,
    dataset_id: uuid.UUID,
    version: int,
    filename: str,
) -> str:
    """
    Generate object storage path.
    """

    extension = Path(filename).suffix

    return (
        f"datasets/"
        f"{tenant_id}/"
        f"{dataset_id}/"
        f"v{version}/"
        f"raw{extension}"
    )