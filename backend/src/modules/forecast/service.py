import logging
import uuid

import pandas as pd
from sqlalchemy.orm import Session

from src.ml.cache.forecast_cache import (
    ForecastCache,
)
from src.ml.features.service import FeatureService
from src.ml.forecasting.evaluator import ForecastEvaluator
from src.ml.forecasting.planner import ForecastPlanner
from src.ml.forecasting.trainer import ForecastTrainer
from src.ml.semantic.service import SemanticService
from src.models.forecast_model import ForecastModel
from src.modules.forecast.predictor import (
    ForecastPredictor,
)
from src.modules.forecast.repository import ForecastRepository

logger = logging.getLogger(__name__)

class ForecastService:
    """
    Forecast service.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.repository = ForecastRepository(db)

        self.trainer = ForecastTrainer()

        self.predictor = ForecastPredictor()

        self.feature_service = FeatureService(db)

        self.planner = ForecastPlanner()

        self.semantic_service = SemanticService(db)

        self.evaluator = ForecastEvaluator()

    async def train(
        self,
        *,
        dataset_version_id: uuid.UUID,
        created_by: uuid.UUID,
        query: str = "forecast revenue",
        date_column: str | None = None,
        target_column: str | None = None,
        aggregation: str | None = None,
    ) -> ForecastModel:
        """
        Train dynamic forecasting model.
        """

        logger.info(
            "Forecast training requested | dataset_version_id=%s",
            dataset_version_id,
        )

        version = (
            self.repository
            .get_dataset_version(
                dataset_version_id,
            )
        )


        if version is None:

            raise ValueError(
                "Dataset version not found."
            )


        try:


            features = (
                self.feature_service
                .build_features(
                    dataset_version_id,
                )
            )


            plan = (
                await self.planner.plan(
                    query=query,
                    columns=list(
                        features.columns,
                    ),
                )
            )


            final_aggregation = (
                aggregation
                or
                plan.aggregation
            )

            semantic = (
                await self.semantic_service.analyze(
                    dataset_version_id,
                )
            )


            sales = semantic.mapping.get(
                "sales",
                {},
            )

            final_date_column = (
                date_column
                or
                plan.date_column
                or
                sales.get("order_date")
            )


            final_target_column = (
                target_column
                or
                plan.target_column
                or
                sales.get("revenue")
            )

            
        # Validate detected metric.
            if (
                final_target_column
                and
                not self._is_numeric_column(
                    features,
                    final_target_column.split(".")[-1],
                )
            ):

                final_target_column = None


            # Generic commerce fallback
            if not final_target_column:

                final_target_column = (
                    self._detect_metric_column(
                        features,
                        [
                            "revenue",
                            "sales",
                            "amount",
                            "total",
                            "price",
                            "value",
                        ],
                    )
                )  

            if not final_date_column:

                raise ValueError(
                    "Unable to detect forecasting date column."
                )


            if not final_target_column:

                # last fallback:
                # forecast volume/count
                for column in features.columns:

                    name = column.lower()

                    if (
                        "order" in name
                        and "id" in name
                    ):

                        final_target_column = column
                        final_aggregation = "count"
                        break


            if not final_target_column:

                raise ValueError(
                    "Unable to detect forecasting metric."
                )
                            
            
            final_date_column = (
                final_date_column
                .split(".")[-1]
            )


            final_target_column = (
                final_target_column
                .split(".")[-1]
            )

            forecast = ForecastModel(

                dataset_id=version.dataset_id,

                name=(
                    f"{final_target_column}-forecast"
                ),

                date_column=final_date_column,

                target_column=final_target_column,

                aggregation=final_aggregation,

                frequency=plan.frequency,

                filters=plan.filters,

                business_question=query,

                artifact_path="",

                created_by=created_by,

            )


            self.repository.create(
                forecast,
            )


            self.repository.commit()


            self.repository.refresh(
                forecast,
            )

            artifact_path = self.trainer.train(
                dataframe=features,
                forecast_id=forecast.id,
                date_column=final_date_column,
                target_column=final_target_column,
                aggregation=final_aggregation or "sum",
                frequency=plan.frequency,
            )

            forecast.artifact_path = artifact_path

# ------------------------------------
# Evaluate model
# ------------------------------------

            evaluation = self.evaluator.evaluate(
                dataframe=features,
                date_column=final_date_column,
                target_column=final_target_column,
                aggregation=final_aggregation or "sum",
                frequency=plan.frequency,
            )

            forecast.performance_score = evaluation["performance_score"]
            forecast.performance_label = evaluation["performance_label"]

            forecast.mae = evaluation["mae"]
            forecast.rmse = evaluation["rmse"]
            forecast.mape = evaluation["mape"]

            self.repository.commit()
            self.repository.refresh(forecast)


            logger.info(
                "Forecast training completed | forecast_id=%s target=%s",
                forecast.id,
                final_target_column,
            )


            return forecast


        except Exception as exc:


            self.repository.rollback()


            logger.exception(
                "Forecast training failed | dataset_version_id=%s",
                dataset_version_id,
            )


            raise exc

    def predict(
        self,
        *,
        forecast_id: uuid.UUID,
        periods: int,
    ):

        logger.info(
            "Forecast prediction requested | forecast_id=%s periods=%d",
            forecast_id,
            periods,
        )

        try:

            forecast = self.repository.get_by_id(
                forecast_id,
            )

            if forecast is None:
                raise ValueError(
                    "Forecast model not found."
                )

            prediction = self.predictor.predict(
                artifact_path=forecast.artifact_path,
                periods=periods,
                frequency=forecast.frequency,
            )

            result = self._build_summary(
                forecast=forecast,
                prediction=prediction,
            )

            logger.info(
                "Forecast prediction completed | forecast_id=%s periods=%d",
                forecast_id,
                periods,
            )

        except Exception:
            logger.exception(
                "Forecast prediction failed | forecast_id=%s",
                forecast_id,
            )
            raise

        return {
            "forecast": prediction,
            **result,
        }
    
    async def auto_forecast(
        self,
        *,
        dataset_version_id: uuid.UUID,
        user_id: uuid.UUID,
        periods: int = 30,
        query: str,
    ):

        logger.info(
            "Auto forecast requested | dataset_version_id=%s",
            dataset_version_id,
        )

        try:
            version = (
                self.repository
                .get_dataset_version(
                    dataset_version_id,
                )
            )

            if version is None:

                raise ValueError(
                    "Dataset version not found."
                )

            cache_key = (
                f"{dataset_version_id}:"
                f"{query}:"
                f"{periods}"
            )

            cached = ForecastCache.get(
                cache_key,
            )

            if cached is not None:
                logger.info(
                    "Forecast cache hit | dataset_version_id=%s",
                    dataset_version_id,
                )
                return cached


        # build features only for planning
            features = (
                self.feature_service
                .build_features(
                    dataset_version_id,
                )
            )


            plan = await self.planner.plan(
                query=query,
                columns=list(
                    features.columns,
                ),
            )

            if (
                plan.target_column is None
                or
                plan.date_column is None
            ):
                raise ValueError(
                    "Unable to detect forecasting columns."
                )

            existing_forecast = (
                self.repository
                .get_existing_forecast(
                    dataset_id=version.dataset_id,
                    target_column=plan.target_column,
                    aggregation=plan.aggregation,
                    frequency=plan.frequency,
                )
            )


            if (
                existing_forecast
                and
                existing_forecast.artifact_path
            ):

                forecast = existing_forecast


            else:

                logger.info(
                    "Training new forecast model"
                )

                forecast = await self.train(
                    dataset_version_id=dataset_version_id,
                    created_by=user_id,
                    query=query,
                )


            predict_result = self.predict(
                forecast_id=forecast.id,
                periods=periods,
            )


            result = {
                "forecast_id": str(forecast.id),
                "forecast_config": {
                    "metric": forecast.target_column,
                    "date_column": forecast.date_column,
                    "aggregation": forecast.aggregation,
                    "frequency": forecast.frequency,
                },
                **predict_result,
            }

            ForecastCache.set(
                cache_key,
                result,
            )

            logger.info(
                "Auto forecast completed | forecast_id=%s",
                forecast.id,
            )

        except Exception:
            logger.exception(
                "Auto forecast failed | dataset_version_id=%s",
                dataset_version_id,
            )
            raise

        return result
    
    def _is_numeric_column(
        self,
        dataframe,
        column: str,
    ) -> bool:
        
        """
        Check whether a column is usable
        as a forecasting metric.
        """

        return (
            column in dataframe.columns
            and
            pd.api.types.is_numeric_dtype(
                dataframe[column]
            )
        )
    
    def _detect_metric_column(
        self,
        dataframe: pd.DataFrame,
        keywords: list[str],
    ) -> str | None:
        """
        Detect forecast metric safely.

        Prevents IDs like:
        payment_id,
        customer_id,
        product_id

        from being selected.
        """

        for keyword in keywords:

            for column in dataframe.columns:

                normalized = column.lower()

                if (
                    keyword in normalized
                    and self._is_numeric_column(
                        dataframe,
                        column,
                    )
                ):
                    return column

        return None

    def _build_summary(
        self,
        *,
        forecast: ForecastModel,
        prediction: list[dict],
    ) -> dict:
        """
        Build business summary and evaluation
        from forecast predictions.
        """

        values = [
            item["prediction"]
            for item in prediction
        ]

        is_count_metric = (
            forecast.aggregation == "count"
        )

        total_value = sum(values)

        average_value = (
            total_value / len(values)
            if values
            else 0
        )

        if is_count_metric:
            total_value = round(total_value)
            average_value = round(average_value)
        else:
            total_value = round(total_value, 2)
            average_value = round(average_value, 2)

        positive_predictions = [
            item
            for item in prediction
            if item["prediction"] > 0
        ]

        if not positive_predictions:
            positive_predictions = prediction

        confidence_ranges = [
            item["upper"] - item["lower"]
            for item in prediction
        ]

        average_uncertainty = round(
            sum(confidence_ranges) / len(confidence_ranges),
            2,
        )

        return {
            "summary": {
                "forecast_days": len(prediction),
                "total_expected_value": total_value,
                "average_daily_value": average_value,
                "highest_period": max(
                    prediction,
                    key=lambda x: x["prediction"],
                ),
                "lowest_expected_period": min(
                    positive_predictions,
                    key=lambda x: x["prediction"],
                ),
                "confidence": {
                    "average_uncertainty_range": average_uncertainty,
                    "interpretation":
                        "Lower uncertainty means more stable forecast.",
                },
            },
            "evaluation": {
                "performance_score": forecast.performance_score,
                "performance_label": forecast.performance_label,
                "mae": forecast.mae,
                "rmse": forecast.rmse,
                "mape": forecast.mape,
            },
        }