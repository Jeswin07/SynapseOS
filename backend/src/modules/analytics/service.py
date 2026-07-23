"""Business analytics service."""

from __future__ import annotations

import logging
import uuid

from sqlalchemy.orm import Session

from src.ml.analytics.commerce import CommerceAnalyticsEngine
from src.ml.cache.analytics_cache import AnalyticsCache
from src.ml.core.filtering.options import DatasetFilterOptions
from src.ml.core.filtering.schemas import DatasetFilters
from src.ml.core.filtering.service import DatasetFilterService
from src.ml.features.service import FeatureService

logger = logging.getLogger(__name__)

class AnalyticsService:
    """
    Generates business intelligence analytics.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.feature_service = FeatureService(db)

        self.filter_service = DatasetFilterService()

        self.engine = CommerceAnalyticsEngine()

    def analyze(
        self,
        dataset_version_id: uuid.UUID,
        filters: DatasetFilters | None = None,
    ) -> dict:
        """
        Generate analytics from dataset features.
        """

        logger.info(
            "Analytics requested | dataset_version_id=%s has_filters=%s",
            dataset_version_id,
            filters is not None,
        )

        try:
        # Only use cache when there are no filters.
            if filters is None:

                cache_key = str(dataset_version_id)

                cached = AnalyticsCache.get(cache_key)

                if cached is not None:

                    logger.info(
                        "Analytics cache hit | dataset_version_id=%s",
                        dataset_version_id,
                    )

                    return cached

            logger.info(
                "Analytics cache miss | dataset_version_id=%s",
                dataset_version_id,
            )

            logger.info(
                "Generating analytics features | dataset_version_id=%s",
                dataset_version_id,
            )

            features = self.feature_service.build_features(
                dataset_version_id=dataset_version_id,
            )

            logger.info(
                "Features generated | rows=%d columns=%d",
                len(features),
                len(features.columns),
            )

            filtered = self.filter_service.apply(
                dataframe=features,
                filters=filters,
            )

            logger.info(
                "Filtering completed | rows=%d",
                len(filtered),
            )

            result = self.engine.analyze(filtered)

            if filters is None:

                AnalyticsCache.set(
                    str(dataset_version_id),
                    result,
                )

            logger.info(
                "Analytics generation completed"
            )
            return result
        except Exception:
            logger.exception(
                "Analytics generation failed | dataset_version_id=%s",
                dataset_version_id,
            )
            raise

    def get_filter_options(
        self,
        dataset_version_id: uuid.UUID,
    ) -> dict:
        """
        Build available filter options for a dataset.
        """

        features = self.feature_service.build_features(
            dataset_version_id=dataset_version_id,
        )

        options = DatasetFilterOptions()

        logger.info(
            "Filter options generated"
        )

        return options.build(features)