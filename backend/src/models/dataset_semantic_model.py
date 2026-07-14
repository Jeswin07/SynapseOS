"""Dataset semantic model."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.db.base import Base


class DatasetSemanticModel(Base):
    """
    Stores AI generated business understanding
    of a dataset version.

    Example:
    revenue -> payment_value
    customer -> customer_unique_id
    delivery -> order_delivered_customer_date
    """

    __tablename__ = "dataset_semantic_models"


    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )


    dataset_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "dataset_versions.id",
        ),
        nullable=False,
        unique=True,
        index=True,
    )


    mapping: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )