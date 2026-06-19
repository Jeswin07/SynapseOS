from uuid import UUID

from pydantic import BaseModel


class TrainForecastRequest(BaseModel):

    dataset_id: UUID

    date_column: str

    target_column: str


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