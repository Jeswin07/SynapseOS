"""Semantic repository."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from src.models.dataset_semantic_model import (
    DatasetSemanticModel,
)


class SemanticRepository:
    """
    Handles semantic model persistence.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db = db


    def get_by_version(
        self,
        dataset_version_id: uuid.UUID,
    ) -> DatasetSemanticModel | None:

        return (
            self.db
            .query(DatasetSemanticModel)
            .filter(
                DatasetSemanticModel.dataset_version_id
                ==
                dataset_version_id,
            )
            .first()
        )


    def create(
        self,
        model: DatasetSemanticModel,
    ) -> None:

        self.db.add(
            model,
        )


    def commit(
        self,
    ) -> None:

        self.db.commit()


    def refresh(
        self,
        model: DatasetSemanticModel,
    ) -> None:

        self.db.refresh(
            model,
        )