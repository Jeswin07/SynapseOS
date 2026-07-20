from uuid import UUID
from typing import Any
from pydantic import BaseModel


class TrainForecastRequest(BaseModel):

    dataset_version_id: UUID

    date_column: str | None = None

    target_column: str | None = None

    query: str = "forecast revenue"


class TrainForecastResponse(BaseModel):

    forecast_id: UUID

    message: str

class ForecastPredictRequest(BaseModel):

    forecast_id: UUID

    periods: int = 30



# ---------------------------------------
# Prediction
# ---------------------------------------

class ForecastPoint(BaseModel):
    date: str
    prediction: float
    lower: float
    upper: float


class ForecastEvaluation(BaseModel):
    performance_score: int
    performance_label: str
    mae: float
    rmse: float
    mape: float


class ForecastSummary(BaseModel):
    forecast_days: int
    total_expected_value: float
    average_daily_value: float

    highest_period: dict[str, Any]
    lowest_expected_period: dict[str, Any]

    confidence: dict[str, Any]


class ForecastPredictResponse(BaseModel):
    forecast: list[ForecastPoint]
    summary: ForecastSummary
    evaluation: ForecastEvaluation