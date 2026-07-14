"""Semantic intelligence service."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from src.ml.features.service import (
    FeatureService,
)
from src.ml.semantic.mapper import (
    SemanticMapper,
)
from src.ml.semantic.profiler import (
    SemanticProfiler,
)
from src.ml.semantic.repository import (
    SemanticRepository,
)
from src.models.dataset_semantic_model import (
    DatasetSemanticModel,
)


class SemanticService:
    """
    Creates and retrieves dataset
    business understanding.
    """


    def __init__(
        self,
        db: Session,
    ) -> None:

        self.repository = SemanticRepository(
            db,
        )

        self.profiler = SemanticProfiler()

        self.mapper = SemanticMapper()

        self.feature_service = FeatureService(
            db,
        )


    async def analyze(
        self,
        dataset_version_id: uuid.UUID,
    ) -> DatasetSemanticModel:


        existing = (
            self.repository
            .get_by_version(
                dataset_version_id,
            )
        )


        if existing:

            return existing


        dataframe = (
            self.feature_service
            .build_features(
                dataset_version_id,
            )
        )


        profile = self.profiler.profile(
            {
                "features": dataframe,
            }
        )


        mapping = await self.mapper.map(
            profile,
        )


        semantic = DatasetSemanticModel(
            dataset_version_id=dataset_version_id,
            mapping=mapping.model_dump(),
        )


        self.repository.create(
            semantic,
        )

        self.repository.commit()

        self.repository.refresh(
            semantic,
        )


        return semantic