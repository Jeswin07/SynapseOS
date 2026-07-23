"""Prediction application service."""

from __future__ import annotations

import logging
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

logger = logging.getLogger(__name__)

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

        try:

            logger.info(
                "Prediction requested | dataset_version_id=%s prediction_type=%s",
                dataset_version_id,
                prediction_type,
            )

            cache_key = (
                f"{dataset_version_id}:"
                f"{prediction_type}"
            )

            cached = PredictionCache.get(
                cache_key,
            )

            if cached is not None:
                logger.info(
                    "Prediction cache hit | dataset_version_id=%s prediction_type=%s",
                    dataset_version_id,
                    prediction_type,
                )
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

            logger.info(
                "Prediction completed | dataset_version_id=%s prediction_type=%s",
                dataset_version_id,
                prediction_type,
            )

        except Exception:
            logger.exception(
                "Prediction failed | dataset_version_id=%s prediction_type=%s",
                dataset_version_id,
                prediction_type,
            )
            raise

        return result


    def history(
        self,
        created_by: UUID,
    ):
        """
        Get prediction history.
        """

        logger.info(
            "Prediction history requested | user_id=%s",
            created_by,
        )

        try:
            return self.repository.list(
                created_by,
            )
        
        except Exception:
            logger.exception(
                "Prediction history failed | user_id=%s",
                created_by,
            )
            raise