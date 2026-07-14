"""Dataset file model."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


class DatasetFile(Base):
    """
    Represents a physical file inside a dataset version.

    Example:
        Dataset:
            Olist

        Version:
            January snapshot

        Files:
            orders.csv
            customers.csv
            payments.csv
    """

    __tablename__ = "dataset_files"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    dataset_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("dataset_versions.id"),
        nullable=False,
        index=True,
    )

    logical_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    storage_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    checksum: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    rows_count: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
    )

    columns_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    schema: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    version = relationship(
        "DatasetVersion",
        back_populates="files",
    )


    profile = relationship(
        "DatasetProfile",
        back_populates="file",
        uselist=False,
        cascade="all, delete-orphan",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )