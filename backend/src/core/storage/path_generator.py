import uuid


def generate_dataset_object_path(
    *,
    tenant_id: uuid.UUID,
    dataset_id: uuid.UUID,
    version: int,
    filename: str,
) -> str:
    """
    Generate object storage path.
    """

    return (
        f"datasets/"
        f"{tenant_id}/"
        f"{dataset_id}/"
        f"v{version}/"
        f"{filename}"
    )

def generate_knowledge_object_path(
    *,
    tenant_id: uuid.UUID,
    document_id: uuid.UUID,
    filename: str,
) -> str:
    return (
        f"knowledge/"
        f"{tenant_id}/"
        f"{document_id}/"
        f"{filename}"
    )