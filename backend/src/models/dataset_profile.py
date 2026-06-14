import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Float,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.db.base import Base


class DatasetProfile(Base):
    __tablename__ = "dataset_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    dataset_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("dataset_versions.id"),
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

    profile_version: Mapped[int] = mapped_column(
        default=1,
        nullable=False,
    )