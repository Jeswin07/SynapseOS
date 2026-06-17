from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.modules.auth.dependencies import (
    get_current_user,
)
from src.modules.ml.schemas import (
    TrainModelRequest,
    TrainModelResponse,
    PredictRequest,
    PredictResponse
)
from src.models.ml_enums import MLAlgorithm
from src.modules.ml.service import MLService

router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning"],
)


@router.post(
    "/train",
    response_model=TrainModelResponse,
    status_code=201,
)
def train_model(
    payload: TrainModelRequest,
    current_user=Depends(
        get_current_user,
    ),
    db: Session = Depends(get_db),
):
    """
    Train a machine learning model.
    """

    try:

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
            metrics=model.metrics,
            message="Model trained successfully.",
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