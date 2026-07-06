from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.models.dataset_enums import (
    BusinessDomain,
    DatasetType,
)


class DatasetCreateRequest(BaseModel):
    """Request model for creating a dataset."""

    name: str = Field(
        min_length=3,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

    dataset_type: DatasetType

    business_domain: BusinessDomain

    tags: list[str] | None = None


class DatasetCreateResponse(BaseModel):
    """Response model after dataset creation."""

    dataset_id: UUID

    message: str

class DatasetVersionResponse(BaseModel):
    """Dataset version response."""

    version_id: UUID

    version: int

    message: str

class DatasetResponse(BaseModel):
    """Dataset response."""

    id: UUID
    name: str
    description: str | None
    dataset_type: DatasetType
    business_domain: BusinessDomain
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }

class DatasetDetailResponse(DatasetResponse):
    """Dataset detail response."""

    tags: list[str] | None

class DatasetVersionItem(BaseModel):
    """
    Dataset version response.
    """

    id: UUID

    version: int

    status: str

    created_at: datetime


    model_config = {
        "from_attributes": True,
    }

class DatasetFileResponse(BaseModel):
    """
    Dataset file inside a dataset version.
    """

    id: UUID

    logical_name: str

    original_filename: str

    rows_count: int | None

    columns_count: int | None

    created_at: datetime


    model_config = {
        "from_attributes": True,
    }