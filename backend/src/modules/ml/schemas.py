from uuid import UUID

from pydantic import BaseModel, Field
from src.models.ml_enums import MLAlgorithm


class TrainModelRequest(BaseModel):
    """
    Request to train a machine learning model.
    """

    dataset_id: UUID

    algorithm: str = Field(
        examples=["linear_regression"],
    )

    target_column: str

    time_column: str


class TrainModelResponse(BaseModel):
    """
    Response returned after training.
    """

    model_id: UUID

    algorithm: MLAlgorithm = MLAlgorithm.AUTO

    metrics: dict

    message: str


class PredictRequest(BaseModel):
    """
    Prediction request.
    """

    model_id: UUID

    data: list[dict]


class PredictResponse(BaseModel):
    """
    Prediction response.
    """

    predictions: list[float]