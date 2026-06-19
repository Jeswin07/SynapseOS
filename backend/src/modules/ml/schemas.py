from uuid import UUID

from pydantic import BaseModel, Field

from src.models.ml_enums import MLAlgorithm


class TrainModelRequest(BaseModel):
    """
    Request to train a machine learning model.
    """

    dataset_id: UUID

    algorithm: MLAlgorithm = Field(
        examples=[MLAlgorithm.LINEAR_REGRESSION],
    )

    target_column: str

    time_column: str


class TrainModelResponse(BaseModel):
    """
    Response returned after training.
    """

    model_id: UUID

    algorithm: MLAlgorithm

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


class AutoMLModelResult(BaseModel):

    algorithm: MLAlgorithm

    model_id: UUID

    rmse: float

    mae: float

    mse: float

    r2: float

    training_time_seconds: float

    is_best: bool

    rows: int

    features: int


class AutoMLResponse(BaseModel):
    training_group: UUID

    winner: MLAlgorithm

    models: list[AutoMLModelResult]


class FeatureImportance(BaseModel):
    feature: str

    value: str | float | int | None

    importance: float

    absolute_importance: float


class ExplainRequest(BaseModel):
    """
    Explain a prediction.
    """

    model_id: UUID

    data: list[dict]

    sample_index: int = 0


class ExplainResponse(BaseModel):
    """
    SHAP explanation response.
    """

    prediction: float

    base_value: float

    features: list[FeatureImportance]