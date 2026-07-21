"""Prediction application service."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from src.ml.cache.prediction_cache import (
    PredictionCache,
)
from src.ml.features.service import (
    FeatureService,
)
from src.ml.prediction.schemas import (
    PredictionType,
)
from src.ml.prediction.service import (
    PredictionEngine,
)
from src.modules.prediction.repository import (
    PredictionRepository,
)


class PredictionService:
    """
    Prediction application layer.

    Connects:
    - Feature engine
    - ML prediction engine
    - Database persistence
    """


    def __init__(
        self,
        db: Session,
    ) -> None:

        self.features = FeatureService(
            db,
        )

        self.engine = PredictionEngine()

        self.repository = PredictionRepository(
            db,
        )


    def predict(
        self,
        *,
        dataset_version_id: UUID,
        created_by: UUID,
        prediction_type: str,
        save: bool = True,
    ):
        """
        Execute prediction workflow.
        """

        cache_key = (
            f"{dataset_version_id}:"
            f"{prediction_type}"
        )

        cached = PredictionCache.get(
            cache_key,
        )

        if cached is not None:
            return cached

        data = self.features.build_features(
            dataset_version_id,
        )


        result = self.engine.predict(
            data=data,
            prediction_type=PredictionType(
                prediction_type,
            ),
        )


        if save:

            self.repository.create(
                dataset_version_id=dataset_version_id,
                created_by=created_by,
                prediction_type=prediction_type,
                result=result.model_dump(
                    mode="json",
                ),
            )

        PredictionCache.set(
            cache_key,
            result,
        )

        return result


    def history(
        self,
        created_by: UUID,
    ):
        """
        Get prediction history.
        """

        return self.repository.list(
            created_by,
        )