from uuid import UUID

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


class ForecastPoint(BaseModel):

    date: str

    prediction: float

    lower: float

    upper: float


class ForecastPredictResponse(BaseModel):

    forecast: list[ForecastPoint]