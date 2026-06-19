from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.models.ml_enums import MLAlgorithm
from src.modules.auth.dependencies import (
    get_current_user,
)
from src.modules.ml.schemas import (
    AutoMLModelResult,
    AutoMLResponse,
    ExplainRequest,
    ExplainResponse,
    PredictRequest,
    PredictResponse,
    TrainModelRequest,
    TrainModelResponse,
)
from src.modules.ml.service import MLService

router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning"],
)


@router.post(
    "/train",
    response_model=TrainModelResponse,
    status_code=status.HTTP_201_CREATED,
)
def train_model(
    payload: TrainModelRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Train a single machine learning model.
    """

    try:

        if payload.algorithm is MLAlgorithm.AUTO:
            raise HTTPException(
                status_code=400,
                detail="Use /ml/train/auto for AutoML training.",
            )

        service = MLService(db)

        model = service.train_model(
            dataset_id=payload.dataset_id,
            created_by=current_user.id,
            algorithm=payload.algorithm,
            target_column=payload.target_column,
            time_column=payload.time_column,
        )

        return TrainModelResponse(
            model_id=model.id,
            algorithm=MLAlgorithm(model.algorithm),
            metrics=model.metrics["metrics"],
            message="Model trained successfully.",
        )

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post(
    "/train/auto",
    response_model=AutoMLResponse,
    status_code=status.HTTP_201_CREATED,
)
def train_auto_model(
    payload: TrainModelRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Train all supported algorithms and return the best model.
    """

    try:

        service = MLService(db)

        result = service.train_auto(
            dataset_id=payload.dataset_id,
            created_by=current_user.id,
            target_column=payload.target_column,
            time_column=payload.time_column,
        )

        return AutoMLResponse(
            training_group=result["training_group"],
            winner=MLAlgorithm(result["winner"].algorithm),
            models=[
                AutoMLModelResult(
                    algorithm=MLAlgorithm(model.algorithm),
                    model_id=model.id,
                    rmse=model.metrics["metrics"]["rmse"],
                    mae=model.metrics["metrics"]["mae"],
                    mse=model.metrics["metrics"]["mse"],
                    r2=model.metrics["metrics"]["r2"],
                    training_time_seconds=model.metrics["training"]["time_seconds"],
                    is_best=model.is_best,
                    rows=model.metrics["dataset"]["rows"],
                    features=model.metrics["dataset"]["features"]
                )
                for model in result["models"]
            ],
        )

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

@router.post(   
    "/predict",
    response_model=PredictResponse,
)
def predict(
    payload: PredictRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    service = MLService(db)

    predictions = service.predict(
        model_id=payload.model_id,
        data=payload.data,
    )

    return PredictResponse(
        predictions=predictions,
    )

@router.post(
    "/explain",
    response_model=ExplainResponse,
)
def explain_prediction(
    payload: ExplainRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Explain a prediction using SHAP.
    """

    service = MLService(db)

    result = service.explain(
        model_id=payload.model_id,
        data=payload.data,
        sample_index=payload.sample_index,
    )

    return ExplainResponse(**result)