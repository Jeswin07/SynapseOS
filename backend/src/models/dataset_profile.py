"""Dataset profile model."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.db.base import Base


class DatasetProfile(Base):
    """
    Stores profiling information for a dataset file.
    """

    __tablename__ = "dataset_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    dataset_file_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "dataset_files.id",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    profile: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    quality_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    file = relationship(
        "DatasetFile",
        back_populates="profile",
    )