"""Prediction database model."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    JSON,
    DateTime,
    ForeignKey,
    String,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.db.base import Base


class PredictionRun(Base):
    """
    Stores ML prediction executions.
    """

    __tablename__ = "prediction_runs"


    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )


    dataset_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "dataset_versions.id",
        ),
        nullable=False,
        index=True,
    )


    prediction_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )


    result: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )


    created_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "users.id",
        ),
        nullable=False,
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )