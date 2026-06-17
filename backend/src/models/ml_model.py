import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class MLModel(Base):
    __tablename__ = "ml_models"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    dataset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("datasets.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    algorithm: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    target_column: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    time_column: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    metrics: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    artifact_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    created_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    training_group: Mapped[uuid.UUID] = mapped_column(
        nullable=False,
        index=True,
    )

    is_best: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


class MLAlgorithm(StrEnum):

    LINEAR_REGRESSION = "linear_regression"

    XGBOOST = "xgboost"

    PROPHET = "prophet"

    LIGHTGBM = "lightgbm"