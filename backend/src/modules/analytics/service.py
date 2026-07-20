"""Business analytics service."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from src.ml.analytics.commerce import CommerceAnalyticsEngine
from src.ml.cache.analytics_cache import AnalyticsCache
from src.ml.core.filtering.schemas import DatasetFilters
from src.ml.core.filtering.service import DatasetFilterService
from src.ml.features.service import FeatureService
from src.ml.core.filtering.options import DatasetFilterOptions


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

        # Only use cache when there are no filters.
        if filters is None:

            cache_key = str(dataset_version_id)

            cached = AnalyticsCache.get(cache_key)

            if cached is not None:
                return cached

        features = self.feature_service.build_features(
            dataset_version_id=dataset_version_id,
        )

        filtered = self.filter_service.apply(
            dataframe=features,
            filters=filters,
        )

        print(len(features))
        print(len(filtered))

        result = self.engine.analyze(filtered)

        if filters is None:

            AnalyticsCache.set(
                str(dataset_version_id),
                result,
            )

        print(filters)

        return result

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

        return options.build(features)