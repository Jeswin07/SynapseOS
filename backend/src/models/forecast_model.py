import uuid
from datetime import datetime

from sqlalchemy import (
    JSON,
    DateTime,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.db.base import Base


class ForecastModel(Base):
    __tablename__ = "forecast_models"


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
        String(255),
        nullable=False,
    )


    date_column: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )


    target_column: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )


    aggregation: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="sum",
    )


    frequency: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="D",
    )


    forecast_horizon: Mapped[int] = mapped_column(
        nullable=False,
        default=30,
    )


    filters: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )


    business_question: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


    artifact_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        default="",
    )


    created_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )