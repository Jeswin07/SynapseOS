import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    func,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from src.db.base import Base
from src.models.dataset_enums import DatasetStatus


class DatasetVersion(Base):
    __tablename__ = "dataset_versions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    dataset_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("datasets.id"),
        nullable=False,
        index=True,
    )

    files = relationship(
        "DatasetFile",
        back_populates="version",
        cascade="all, delete-orphan",
    )

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[DatasetStatus] = mapped_column(
        Enum(DatasetStatus),
        default=DatasetStatus.UPLOADING,
        nullable=False,
    )

    uploaded_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    processing_duration_ms: Mapped[int | None] = mapped_column(
        nullable=True,
    )